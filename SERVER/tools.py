from langchain_community.utilities import GoogleSerperAPIWrapper
from concurrent.futures import ThreadPoolExecutor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from firecrawl import FirecrawlApp
from langchain.schema import Document
from stores import RedisStore
from typing import List
import re
from logger import setup_logger
from config import SERPER_API_KEY, FIRE_CRAWL_API_KEY

logger = setup_logger(__name__)

class SearchTool:
  def __init__(self):
    self.__search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY, gl="vn", hl="vi", k=3)
    logger.info("SearchTool initialized")

  def search(self, queries: List[str]) -> List[Document]:
      try:
          logger.info(f"Starting search for {len(queries)} queries: {queries}")
          # Thực hiện tìm kiếm song song
          with ThreadPoolExecutor() as executor:
              logger.debug("Executing parallel searches")
              results = list(executor.map(lambda q: self.__search.results(q), queries))

          logger.info(f"Search completed, processing {len(results)} result sets")

          if not results:
              logger.warning("No search results found")
              return []

          result_clean = []
          seen_links = set()
          not_crawl_prefixes = ["https://www.youtube.com/", "https://youtube.com/", "https://youtu.be/", "https://www.facebook.com/"]

          logger.debug("Filtering search results")
          for i, item in enumerate(results):
              organic_items = item.get("organic", [])
              logger.debug(f"Processing result set {i+1}/{len(results)} with {len(organic_items)} organic items")

              for organic_item in organic_items:
                  link = organic_item["link"]

                  # Kiểm tra xem liên kết có phải là Facebook hoặc YouTube không
                  is_not_crawl = any(link.startswith(prefix) for prefix in not_crawl_prefixes)

                  # Nếu không phải Facebook/YouTube và chưa thấy link này trước đó
                  if not is_not_crawl and link not in seen_links:
                      seen_links.add(link)
                      result_clean.append({
                          "title": organic_item["title"],
                          "snippet": organic_item["snippet"],
                          "link": link
                      })

          logger.info(f"Filtered results: {len(result_clean)} unique non-Facebook links")

          result_documents: List[Document] = []
          logger.debug("Converting to Document objects")
          for item in result_clean:
              result_documents.append(Document(page_content=item["snippet"], metadata={"title": item["title"], "link": item["link"]}))

          logger.info(f"Returning {len(result_documents)} document objects")
          return result_documents

      except Exception as e:
          # Xử lý lỗi nếu cần
          logger.error(f"Error occurred during search: {e}", exc_info=True)
          raise e


class FireCrawlTool:
  def __init__(self):
    self.__firecrawl = FirecrawlApp(api_key=FIRE_CRAWL_API_KEY)
    self.__redis_store = RedisStore()
    logger.info("FireCrawlTool initialized")

  def scrape(self, urls: List[str]) -> List[Document]:
      """
      Scrape content from a list of URLs and split into smaller documents.

      Args:
          urls: List of URLs to scrape

      Returns:
          List of Document objects with cleaned content and metadata
      """
      try:
          text_splitter = RecursiveCharacterTextSplitter(
              chunk_size=10000,  # ~3000 words (assuming avg word is 4 chars)
              chunk_overlap=500,
              length_function=len,
              separators=["\n\n", "\n", ". ", " ", ""]
          )
          if not urls:
              logger.warning("No URLs provided for scraping")
              return []

          # Check if URLs are already in Redis
          docs_result = []
          redis_data = []
          for url in urls:
              data =  self.__redis_store.get_string(url)
              if data != "":
                doc = Document(page_content=data, metadata={"url": url})
                redis_data.append(doc)
                urls.remove(url)

          for item in redis_data:
              chunks = text_splitter.split_text(item.page_content)
              metadata = {**item.metadata}

              for i, chunk in enumerate(chunks):
                  chunk_metadata = {
                      **metadata,
                    "chunk": i + 1,
                    "total_chunks": len(chunks)
                  }
                  docs_result.append(Document(
                      page_content=chunk,
                      metadata=chunk_metadata
                  ))

          if len(urls) == 0:
              logger.info("All URLs already exist in Redis, returning cached documents")
              return docs_result

          scrape_results = self.__firecrawl.batch_scrape_urls(
              urls,
              params={
                  'formats': ['markdown'],
                  'excludeTags': [
                      'script', 'img', 'a', 'button', 'br', '.contact-title',
                      '.footer', '.header', 'table', 'nav', 'iframe', 'meta'
                  ]
              }
          )

          data_extracts = scrape_results.get("data", [])

          for item in data_extracts:
              if item.get("metadata", {}).get('statusCode') == 200 and "markdown" in item:
                  page_content = item['markdown'].strip()
                  page_content = self._clean_text(page_content)
                  self.__redis_store.set_string(item.get("metadata", {}).get('url'), page_content)
                  if len(page_content) < 100:
                      continue
                  chunks = text_splitter.split_text(page_content)

                  metadata = {**item.get("metadata", {})}

                  for i, chunk in enumerate(chunks):
                      # Add chunk information to metadata
                      chunk_metadata = {
                          **metadata,
                          "chunk": i + 1,
                          "total_chunks": len(chunks)
                      }

                      docs_result.append(Document(
                          page_content=chunk,
                          metadata=chunk_metadata
                      ))

          logger.info(f"Scraped and split content into {len(docs_result)} document chunks from {len(data_extracts)} URLs")
          return docs_result

      except Exception as e:
          logger.error(f"Error occurred during scraping: {e}", exc_info=True)
          raise e

  def _clean_text(self, text: str) -> str:
      """
      Clean scraped text by removing unwanted characters and normalizing whitespace.

      Args:
          text: Raw text to clean

      Returns:
          Cleaned text
      """
      # Replace newlines, breaks, and other special characters
      text = text.replace("\n", " ").replace("<br>", "").replace("\r", "")
      text = text.replace("\t", " ").replace("\xa0", "").replace("truncated", "")
      text = text.replace("–", "").replace("©", "").replace("/ ", "")

      # Remove special characters
      text = re.sub(r'[*|\><():;.,\_\\#+=~`\'"{}\[\]\^&$-]', '', text)

      # Normalize whitespace
      while "  " in text:
          text = text.replace("  ", " ")

      return text




