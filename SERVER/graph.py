from langgraph.graph import StateGraph, END
from nodes import Nodes
from langgraph.checkpoint.memory import MemorySaver
from state import MainState
from langchain_core.runnables.config import RunnableConfig
from typing import Dict, Any, AsyncGenerator

class Graph:
    """
    Implements the processing graph for handling questions and generating responses.
    """

    def __init__(self):
        self.__nodes = Nodes()
        self.__graph = StateGraph(MainState)
        self.__graph.add_node("route", self.__nodes.route)
        self.__graph.add_node("context", self.__nodes.context)
        self.__graph.add_node("search", self.__nodes.search)
        self.__graph.add_node("store", self.__nodes.store)
        self.__graph.add_node("summarize", self.__nodes.summarize)
        self.__graph.add_node("grade", self.__nodes.grade)
        self.__graph.add_node("generate_basic", self.__nodes.generate_basic)
        self.__graph.add_node("generate_from_docs", self.__nodes.generate_from_docs)
        self.__graph.add_node("extract", self.__nodes.extract_data_search)
        self.__graph.add_node("error", self.__nodes.error_node)

        self.__graph.set_entry_point("route")
        self.__graph.add_conditional_edges(
            "route",
            lambda state: state.next_state,
            {
                "context": "context",
                "generate": "generate_basic",
                "error": "error",
            }
        )
        self.__graph.add_conditional_edges(
          "context",
          lambda state: state.next_state,
          {
            # "search": "search",
            "store": "store",
            "error": "error",
          }
        )
        self.__graph.add_conditional_edges(
            "store",
            lambda state: state.next_state,
            {
                "grade": "grade",
                "search": "search",
                "error": "error",
                "no_data": "generate_basic",
                "no_queries": "generate_basic",
            }
        )

        self.__graph.add_conditional_edges(
          "search",
          lambda state: state.next_state,
            {
                "grade": "grade",
                "error": "error"
            }
        )

        self.__graph.add_conditional_edges(
          "grade",
          lambda state: state.next_state,
            {
                "summarize": "summarize",
                "search": "search",
                "no_data": "generate_basic",
                "extract": "extract",
                "error": "error",
            }
        )
        self.__graph.add_conditional_edges(
          "extract",
          lambda state: state.next_state,
            {
                "summarize": "summarize",
                "no_data": "generate_basic",
                "error": "error",
            }
        )

        self.__graph.add_conditional_edges(
          "summarize",
          lambda state: state.next_state,
          {
            "no_data": "generate_basic",
            "error": "error",
            "generate": "generate_from_docs"
          }
        )
        self.__graph.add_edge("generate_from_docs", END)
        self.__graph.add_edge("generate_basic", END)
        self.__graph.add_edge("error", END)
        self.__memory = MemorySaver()
        self.__build = self.__graph.compile(checkpointer=self.__memory)

    def get_flow(self):
        return self.__build.get_graph().draw_mermaid()

    async def run(self, question: str, chat_id: str, user_name: str, is_search: bool = False) -> AsyncGenerator[Dict[str, Any], None]:
        state = MainState(
            chat_id=chat_id,
            user_name=user_name,
            question=question,
            next_state="route",
            history=[],
            is_search=is_search,
            in_node="Xử lý câu hỏi từ người dùng",
            context_anlysis=None,
            documents=[],
            search_results=[],
            from_node=None,
            prompt="",
            summary=None,
            output="",
        )
        config: RunnableConfig = RunnableConfig(configurable={"thread_id": chat_id})

        # Lặp qua các sự kiện từ astream và yield từng sự kiện
        async for event in self.__build.astream(state, config=config, stream_mode="values"):
            yield event


