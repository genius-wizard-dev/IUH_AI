import logging
from langchain_core.messages import (
    SystemMessage,
    BaseMessage,
    HumanMessage,
)
import re
from concurrent.futures import ThreadPoolExecutor
from langchain.schema import Document
from models import OpenAIModel, GoogleModel, PerplexityModel
from stores import MongoStore, UpstashStore
from tools import SearchTool, FireCrawlTool
from entities import Message, Entry
from datetime import datetime
from state import ContextAnalysis, Node, Summary, MainState
from prompts import prompt_route, prompt_context, prompt_store_queries, prompt_grader_doc_instruct, prompt_search_queries, prompt_grader_search_instruct, prompt_search_summary, prompt_generate_search_answer, prompt_basic_generate
from typing import Union, List, Dict
import json
import urllib3
from logger import setup_logger
from config import max_workers

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = setup_logger(__name__)

class Nodes:

  def __init__(self):
    self.__mongo_store = MongoStore()
    # self.__vector_store = PineconeStore()
    self.__vector_store = UpstashStore()
    self.__search_tool = SearchTool()
    self.__google_model = GoogleModel().model()
    self.__openai_model_json = OpenAIModel().model_json()
    self.__perplexity_model = PerplexityModel().model()
    self._fire_crawl_tool = FireCrawlTool()

  @staticmethod
  def __content_json( message: BaseMessage) -> Union[dict, str]:
      content = re.sub(r"```json|```", "", str(message.content)).strip()
      try:
          return json.loads(content)
      except json.JSONDecodeError as e:
          logger.error(f"Error parsing JSON: {e}")
          return content

  def __grade_document(self, doc: Document, context: ContextAnalysis, prompt: str) -> dict:
    try:
        result: BaseMessage = self.__openai_model_json.invoke([
            SystemMessage(content=prompt.format(
                doc=doc.page_content,
                intent=context.intent,
                type=context.type,
                scope=context.scope,
                expected_output=context.expected_output,
                actions=context.actions
            ))
        ])
        result_dict: Union[dict, str] = self.__content_json(result)
        logger.info(f"Grading result for doc: {result_dict}")

        if isinstance(result_dict, dict):
            # Trường hợp đúng định dạng trực tiếp
            if "score" in result_dict and "explanation" in result_dict:
                score = result_dict.get("score", 0)
                explanation = result_dict.get("explanation", "No explanation provided")
            # Trường hợp lồng trong "results"
            elif "results" in result_dict and isinstance(result_dict["results"], list) and len(result_dict["results"]) > 0:
                nested_result = result_dict["results"][0]
                score = nested_result.get("score", 0)
                explanation = nested_result.get("explanation", "No explanation provided")
            else:
                logger.warning(f"Invalid grading format: {result_dict}")
                return {"score": 0, "explanation": "Error: Invalid response format"}

            # Đảm bảo score là số nguyên
            try:
                score = int(score)
            except (ValueError, TypeError):
                logger.error(f"Invalid score value: {score}, defaulting to 0")
                score = 0
            return {"score": score, "explanation": explanation}
        else:
            logger.warning(f"Non-dict grading result: {result_dict}")
            return {"score": 0, "explanation": "Error: Invalid response format"}

    except Exception as e:
        logger.error(f"Error processing doc {doc.metadata.get('link', 'unknown')}: {str(e)}")
        return {"score": 0, "explanation": f"Error: {str(e)}"}


  def __grade_documents_multi_thread(self, documents: List[Document], context: ContextAnalysis, prompt: str) -> List[dict]:
    grader = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:  # Điều chỉnh số workers nếu cần
        futures = [
            executor.submit(self.__grade_document, doc, context, prompt)
            for doc in documents
        ]
        grader = [future.result() for future in futures]
    return grader


  def route(self, state: MainState) -> MainState:
    """
    Routes the given state based on the response from the OpenAI model.

    Args:
      state (BasicState): The current state containing the question to be routed.

    Returns:
      BasicState: The updated state with the next state set based on the routing logic.
    """
    logging.info("Routing question")
    try:
      state.in_node = "Đang chọn nguồn xử lý câu hỏi"
      reasoning: BaseMessage = self.__openai_model_json.invoke([HumanMessage(content=prompt_route.format(history=state.history, question=state.question))])
      routing: Union[dict, str] = self.__content_json(reasoning)
      # logger.info(f"Routing result: {routing}")
      if isinstance(routing, dict):
        if routing.get("route") in ["context", "generate"]:
          state.next_state = routing.get("route", "error")
          return state
      state.next_state = "error"
      return state
    except Exception as e:
      logger.error(f"Error routing question: {e}")
      state.next_state = "error"
      return state

  def context(self, state: MainState) -> MainState:
      """
      Generates a context state based on the provided BasicState.

      This method takes a BasicState object, converts it to a ContextState object,
      and attempts to generate reasoning using an OpenAI model. The reasoning is
      then analyzed and used to update the context state.

      Args:
        state (BasicState): The initial state containing the question and other relevant data.

      Returns:
        ContextState: The updated context state with the context and next state information.

      Raises:
        Exception: If there is an error during the context generation process, the next state is set to "error".
      """
      logger.info("Analysis context")
      try:
          state.in_node = "Đang phân tích câu hỏi của bạn"
          reasoning: BaseMessage = self.__openai_model_json.invoke([HumanMessage(content=prompt_context.format(question=state.question))])
          context_anlysis: Union[dict, str] = self.__content_json(reasoning)
          # logger.info(f"Context analysis result: {context_anlysis}")
          if isinstance(context_anlysis, dict):
              state.context_anlysis = ContextAnalysis(**context_anlysis)
              state.next_state = "store"
              return state
          state.next_state = "error"
          return state
      except Exception as e:
          logger.error(f"Error getting context: {e}")
          state.next_state = "error"
          return state

  def store(self, state: MainState) -> MainState:
    """
    Stores the given state and determines the next state based on the results of a reasoning query.

    Args:
      state (ContextState): The current context state to be stored.

    Returns:
      StoreState: The updated store state with the next state determined.

    The function performs the following steps:
    1. Converts the given state to a StoreState object.
    2. Invokes a reasoning query using the OpenAI model with a formatted prompt.
    3. Parses the response to extract queries.
    4. Searches for documents using the extracted queries.
    5. Updates the store state with the search results and determines the next state:
       - If documents are found, sets the next state to "grade".
       - If no documents are found and search is enabled, sets the next state to "search".
       - Otherwise, sets the next state to "generate".
    6. Handles any exceptions by printing an error message and setting the next state to "error".
    """
    logging.info("Retriever documents")
    state.from_node = Node.STORE
    try:
        state.in_node = "Đang tìm kiếm dữ liệu từ kho dữ liệu"
        if state.context_anlysis is None:
            state.next_state = "error"
            return state
        prompt = prompt_store_queries.format(
            intent=state.context_anlysis.intent,
            type=state.context_anlysis.type,
            scope=state.context_anlysis.scope,
            expected_output=state.context_anlysis.expected_output,
            actions=state.context_anlysis.actions
        )
        reasoning_queries = self.__openai_model_json.invoke([HumanMessage(content=prompt)])
        queries_dict = self.__content_json(reasoning_queries)
        if not isinstance(queries_dict, dict):
            state.next_state = "error"
            return state
        queries = queries_dict.get("queries", [])
        if queries:
            results = self.__vector_store.search(queries)
            if results:
                state.documents = results
                state.next_state = "grade"
                state.prompt = prompt_grader_doc_instruct
            elif state.is_search:
                state.next_state = "search"
            else:
                state.next_state = "no_data"
        else:
            state.next_state = "no_queries" if not state.is_search else "search"
        return state

    except Exception as e:
        logger.error(f"Error getting store: {e}")
        state.next_state = "error"
        return state

  def grade(self, state: MainState) -> MainState:
    try:
        if state.from_node == Node.STORE:
            logger.info("Grading documents from store")
            state.in_node = "Đang đánh giá dữ liệu từ kho dữ liệu"
            documents_to_grade = state.documents
            next_success_state = "summarize"
            next_failure_state = "search" if state.is_search else "no_data"
        elif state.from_node == Node.SEARCH:
            logger.info("Grading web search results")
            state.in_node = "Đang đánh giá dữ liệu từ tìm kiếm"
            documents_to_grade = state.search_results
            next_success_state = "extract"
            next_failure_state = "no_data"
        else:
            # Handle unexpected from_node value
            logger.warning(f"Unexpected from_node: {state.from_node}")
            state.next_state = "error"
            return state

        # Skip processing if context analysis is missing
        if state.context_anlysis is None:
            state.next_state = "error"
            return state

        # Grade documents using multi-threading
        graded_docs = self.__grade_documents_multi_thread(
            documents_to_grade,
            state.context_anlysis,
            state.prompt
        )

        # Filter relevant documents
        relevant_docs: List[Document] = []
        for item, doc in zip(graded_docs, documents_to_grade):
            if isinstance(item, dict) and "score" in item:
                score = int(item["score"])
                if score >= 8:
                    doc.metadata["score"] = score
                    relevant_docs.append(doc)
            else:
                logger.warning(f"Invalid graded item: {item}")

        # Log relevant document count
        logger.info(f"Found {len(relevant_docs)} documents with score >= 8")

        # Set next state based on results
        if relevant_docs:
            if state.from_node == Node.STORE:
                state.documents = relevant_docs
            else:  # Node.SEARCH
                state.search_results = relevant_docs
            state.next_state = next_success_state
        else:
            state.next_state = next_failure_state

        return state

    except Exception as e:
        logger.error(f"Error grading documents: {str(e)}")
        state.next_state = "error"
        return state


  def search(self, state: MainState) -> MainState:
    state.from_node = Node.SEARCH
    logging.info("Web search")

    try:
        if state.context_anlysis is None:
            state.next_state = "error"
            return state
        state.in_node = "Đang tìm kiếm dữ liệu từ web"
        prompt = prompt_search_queries.format(
            intent=state.context_anlysis.intent,
            type=state.context_anlysis.type,
            scope=state.context_anlysis.scope,
            expected_output=state.context_anlysis.expected_output,
            actions=state.context_anlysis.actions
        )
        reasoning_response = self.__google_model.invoke([HumanMessage(content=prompt)])
        queries_dict = self.__content_json(reasoning_response)
        state.next_state = "error"
        if isinstance(queries_dict, dict):
            queries = queries_dict.get("queries", [])
            logger.info(f"Queries: {queries}")
            if queries:
                results = self.__search_tool.search(queries)
                if results:
                    state.search_results = results
                    state.prompt = prompt_grader_search_instruct
                    state.next_state = "grade"
                    logger.info(f"Search results: {len(state.search_results)} documents found")
                else:
                    logger.info("No search results found")
            else:
                logger.info("No queries generated")
        else:
            logger.warning(f"Invalid queries response format: {type(queries_dict)}")
        return state

    except Exception as e:
        logger.error(f"Error getting search: {e}")
        state.next_state = "error"
        return state


  # @staticmethod
  # def __clean_content(content: str) -> str:
  #   """Làm sạch nội dung văn bản."""
  #   return content.replace("\n", "").replace("  ", "").replace("   ", "").replace("    ", "")

  # @staticmethod
  # def __split_content(content: str, max_length: int = 4000) -> List[str]:
  #   """Chia nhỏ nội dung văn bản nếu vượt quá max_length ký tự."""
  #   if len(content) <= max_length:
  #       return [content]
  #   return textwrap.wrap(content, width=max_length, break_long_words=False)


  # @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
  # def __process_link(self, link: str) -> List[dict]:
  #   """Xử lý từng link, chia nhỏ nội dung nếu cần."""
  #   try:
  #       loader = WebBaseLoader([link], requests_kwargs={"verify": False})
  #       docs = loader.load()
  #       doc = docs[0]
  #       cleaned_content = self.__clean_content(doc.page_content)
  #       content_chunks = self.__split_content(cleaned_content, max_length=4000)
  #       return [
  #           {
  #               "page_content": chunk,
  #               "metadata": {"title": doc.metadata.get("title", ""), "link": link, "chunk_id": i}
  #           }
  #           for i, chunk in enumerate(content_chunks)
  #       ]
  #   except Exception as e:
  #       logger.error(f"Error processing link {link}: {str(e)}")
  #       return [{"page_content": "", "metadata": {"title": "", "link": link, "chunk_id": 0}}]


  # def __load_links_parallel(self, links: List[str], max_workers: int = 4) -> List[Document]:
  #   """Tải dữ liệu song song từ các link và trả về danh sách Document."""
  #   with ThreadPoolExecutor(max_workers=max_workers) as executor:
  #       futures = [executor.submit(self.__process_link, link) for link in links]
  #       results = [future.result() for future in futures]
  #   documents = []
  #   for result_chunks in results:
  #       for chunk in result_chunks:
  #           documents.append(Document(
  #               page_content=chunk["page_content"],
  #               metadata=chunk["metadata"]
  #           ))
  #   return documents

  def extract_data_search(self, state: MainState) -> MainState:
      """Extracts and enriches data from search results."""
      logger.info("Extracting data from search results")

      try:
          state.in_node = "Đang trích xuất dữ liệu từ tìm kiếm"
          if not state.search_results:
              logger.warning("No search results to extract data from")
              state.next_state = "no_data"
              return state

          links = list({
              item.metadata["link"]
              for item in state.search_results
              if "link" in item.metadata
          })

          if not links:
              logger.warning("No valid links found in search results")
              state.next_state = "no_data"
              return state

          logger.info(f"Attempting to scrape {len(links)} unique links")

          extra_data = self._fire_crawl_tool.scrape(links)

          if extra_data:
              state.search_results = extra_data
              logger.info(f"Successfully extracted {len(extra_data)} documents from search results")
              state.next_state = "summarize"
          else:
              logger.warning("No data could be extracted from the links")
              state.next_state = "no_data"

          return state

      except Exception as e:
          logger.error(f"Error during data extraction: {str(e)}")
          state.next_state = "error"
          return state


  def __summarize_document(self, doc: Document, intent: str, expected_output: str) -> Dict:
    """
    Tóm tắt một document với prompt_search_summary.

    Args:
        doc: Document object containing page content and metadata
        intent: User intent for summarization context
        expected_output: Expected output format description

    Returns:
        Dictionary with summary information or error details
    """
    try:
        # Prepare source information
        source = doc.metadata.get("url", "vector_store")

        # Invoke model with formatted prompt
        reasoning = self.__google_model.invoke([
            HumanMessage(content=prompt_search_summary.format(
                intent=intent,
                expected_output=expected_output,
                content=doc.page_content,
                source=source
            ))
        ])

        # Parse and validate response
        summary_dict = self.__content_json(reasoning)

        if not isinstance(summary_dict, dict):
            logger.warning(f"Invalid summary format for document from {source}")
            return {"error": "Invalid summary format", "useful_info": "No"}

        return summary_dict

    except Exception as e:
        logger.error(f"Error summarizing document: {str(e)}", exc_info=True)
        return {"error": str(e), "useful_info": "No"}

  def summarize(self, state: MainState) -> MainState:
      """
      Summarize all documents and search results in the state.

      Args:
          state: Current MainState object

      Returns:
          Updated MainState with summary or error state
      """
      logger.info("Summarizing documents")

      try:
          state.in_node = "Đang tổng hợp dữ liệu"

          # Normalize collections to lists
          documents = self._normalize_to_list(state.documents)
          search_results = self._normalize_to_list(state.search_results)
          all_documents = documents + search_results

          # Early return if no documents
          if not all_documents:
              logger.info("No documents to summarize")
              state.next_state = "no_data"
              return state

          # Early return if no context analysis
          if state.context_anlysis is None:
              logger.info("Missing context analysis")
              state.next_state = "error"
              return state

          # Extract required context
          intent = state.context_anlysis.intent
          expected_output = state.context_anlysis.expected_output

          # Process documents in parallel with timeout protection
          try:
              with ThreadPoolExecutor(max_workers=max_workers) as executor:
                  # Submit all tasks
                  futures = [
                      executor.submit(self.__summarize_document, doc, intent, expected_output)
                      for doc in all_documents
                  ]

                  # Collect results with timeout handling
                  summaries = []
                  for future in futures:
                      try:
                          result = future.result(timeout=60)  # 60 second timeout
                          summaries.append(result)
                      except TimeoutError:
                          logger.warning("Document summarization timed out")
                          summaries.append({"error": "Timeout", "useful_info": "No"})
                      except Exception as e:
                          logger.error(f"Error processing document: {str(e)}")
                          summaries.append({"error": str(e), "useful_info": "No"})
          except Exception as e:
              logger.error(f"Error in parallel processing: {str(e)}", exc_info=True)
              state.next_state = "error"
              return state

          # Filter for useful summaries
          useful_summaries = [
              s for s in summaries
              if isinstance(s, dict) and s.get("useful_info") == "Yes"
          ]

          if not useful_summaries:
              logger.info("No useful summaries found")
              state.next_state = "no_data"
              return state

          # Consolidate all useful summaries
          state.summary = self._consolidate_summaries(useful_summaries)

          logger.info(f"Consolidated summary created from {len(useful_summaries)} documents")
          state.next_state = "generate"

          return state

      except Exception as e:
          logger.error(f"Error in summarize method: {str(e)}", exc_info=True)
          state.next_state = "error"
          return state

  def _normalize_to_list(self, data):
      if isinstance(data, list):
          return data
      elif data:
          return [data]
      return []

  def _consolidate_summaries(self, useful_summaries: List[Dict]) -> Summary:
      """
      Consolidate multiple summary dictionaries into a single Summary object.

      Args:
          useful_summaries: List of dictionaries with summary information

      Returns:
          Consolidated Summary object
      """
      # Initialize consolidated summary
      consolidated = Summary(
          summary="",
          data_source=[],
          useful_info="Yes",
          additional_info="",
          missing_info="",
          data_quality="Unknown"
      )

      # Track all sources to remove duplicates later
      all_sources = []

      # Process each summary
      for summary in useful_summaries:
          # Add summary text with separator
          if summary.get("summary"):
              consolidated.summary += summary["summary"] + "\n\n"

          # Collect sources
          sources = summary.get("data_source", [])
          if isinstance(sources, list):
              all_sources.extend(sources)
          elif sources:  # Handle single source as string
              all_sources.append(sources)

          # Collect additional information
          if summary.get("additional_info"):
              consolidated.additional_info += summary["additional_info"] + "\n"

          # Collect missing information
          if summary.get("missing_info"):
              consolidated.missing_info += summary["missing_info"] + "\n"

          # Update data quality if better information available
          if summary.get("data_quality") and summary["data_quality"] != "Unknown":
              consolidated.data_quality = summary["data_quality"]

      # Clean up and deduplicate
      consolidated.summary = consolidated.summary.strip()
      consolidated.data_source = list(dict.fromkeys(all_sources))  # Remove duplicates while preserving order
      consolidated.additional_info = consolidated.additional_info.strip()
      consolidated.missing_info = consolidated.missing_info.strip()

      return consolidated

  def generate_basic(self, state: MainState) -> MainState:
    logger.info("Generating basic output")
    try:
      state.in_node = "Đang tạo câu trả lời"
      output: BaseMessage = self.__google_model.invoke([HumanMessage(content=prompt_basic_generate.format(history=state.history, question=state.question))])
      state.output = str(output.content)
      message: Message = Message(chat_id=state.chat_id, user_name=state.user_name, entry=Entry(question=state.question, answer=state.output, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
      self.__mongo_store.save_message(message)
      # logger.info(f"Message saved: {message}")
      state.next_state = "END"
      return state
    except Exception as e:
      logger.error(f"Error generating output: {e}")
      return state

  def generate_from_docs(self, state: MainState) -> MainState:
    """
    Generate an answer from summarized documents based on context analysis.

    Args:
        state: Current MainState object containing context analysis and summary

    Returns:
        Updated MainState with generated output
    """
    logger.info("Generating output from documents")

    try:
        state.in_node = "Đang tạo câu trả lời"

        # Validate required data is present
        if state.context_anlysis is None:
            logger.warning("Missing context analysis, cannot generate answer")
            state.next_state = "error"
            return state

        if state.summary is None:
            logger.warning("Missing document summary, cannot generate answer")
            state.next_state = "error"
            return state

        # Extract needed fields from state with defaults for safety
        intent = getattr(state.context_anlysis, 'intent', '')
        expected_output = getattr(state.context_anlysis, 'expected_output', '')
        actions = getattr(state.context_anlysis, 'actions', '')

        summary_text = getattr(state.summary, 'summary', '')
        sources = getattr(state.summary, 'data_source', [])
        additional_info = getattr(state.summary, 'additional_info', '')

        # Format the prompt with extracted information
        formatted_prompt = prompt_generate_search_answer.format(
            intent=intent,
            expected_output=expected_output,
            actions=actions,
            summary=summary_text,
            source=sources,
            additional_info=additional_info
        )

        # Generate the answer with timeout protection
        try:
            output: BaseMessage = self.__google_model.invoke(
                [HumanMessage(content=formatted_prompt)],
                timeout=120  # 2 minute timeout
            )
            state.output = str(output.content)
        except TimeoutError:
            logger.error("Model response timed out when generating answer")
            state.output = "Xin lỗi, hệ thống đang gặp sự cố. Vui lòng thử lại sau."
            state.next_state = "error"
            return state

        # Save the conversation to database
        try:
            message = Message(
                chat_id=state.chat_id,
                user_name=state.user_name,
                entry=Entry(
                    question=state.question,
                    answer=state.output,
                    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )
            self.__mongo_store.save_message(message)
            logger.info(f"Message saved for chat_id: {state.chat_id}")
        except Exception as db_error:
            # Continue even if database save fails
            logger.error(f"Failed to save message to database: {str(db_error)}", exc_info=True)

        # Set next state and return
        state.next_state = "END"
        return state

    except Exception as e:
        logger.error(f"Error in generate_from_docs: {str(e)}", exc_info=True)
        state.output = "Xin lỗi, đã xảy ra lỗi khi xử lý yêu cầu của bạn."
        state.next_state = "END"
        return state

  def error_node(self, state: MainState) -> MainState:
    """
    Handles error states in the workflow.

    Args:
        state: Current MainState object

    Returns:
        Updated MainState with error handling
    """
    logger.error("An error occurred in the workflow")
    state.output = "Xin lỗi, đã xảy ra lỗi trong quá trình xử lý yêu cầu của bạn."
    state.in_node = "Đã xảy ra lỗi"
    state.next_state = "END"
    return state
