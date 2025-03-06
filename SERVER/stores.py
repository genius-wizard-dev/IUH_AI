# from langchain_pinecone import PineconeVectorStore
from langchain_community.vectorstores.upstash import UpstashVectorStore
from concurrent.futures import ThreadPoolExecutor
from redis import Redis
from langchain.schema import Document
from typing import List
from pymongo import MongoClient
from models import OpenAIModel
from entities import Message
from logger import setup_logger
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME, REDIS_PORT, REDIS_HOST, REDIS_PASSWORD

logger = setup_logger(__name__)

class MongoStore:
  def __init__(self):
    logger.info("Initializing MongoStore")
    self.__client = MongoClient(MONGO_URI)
    self.__db = self.__client[MONGO_DB_NAME]
    self.__collection = self.__db[MONGO_COLLECTION_NAME]
    logger.info(f"MongoStore initialized with collection: {MONGO_COLLECTION_NAME}")

  def save_message(self, message: Message) -> bool:
    try:
      logger.info(f"Saving message for chat_id: {message.chat_id}, user: {message.user_name}")

      self.__collection.update_one(
              {"chat_id": message.chat_id, "name": message.user_name},
              {"$push": {"history": message.entry.model_dump()}},
              upsert=True
          )

      logger.info(f"Message saved successfully for chat_id: {message.chat_id}")
      return True
    except Exception as e:
      logger.error(f"Error saving message to MongoDB: {e}")
      raise e

  def get_history(self, chat_id: str) -> List[Message]:
    try:
      logger.info(f"Retrieving history for chat_id: {chat_id}")
      messages = self.__collection.find({"chat_id": chat_id})
      result = [Message(**message) for message in messages]
      logger.info(f"Retrieved {len(result)} messages for chat_id: {chat_id}")
      return result
    except Exception as e:
      logger.error(f"Error retrieving history from MongoDB: {e}")
      raise e

# class PineconeStore:
#   def __init__(self):
#     logger.info("Initializing PineconeStore")
#     self.__client = Pinecone(api_key=PINECONE_API_KEY)
#     self.__index = self.__client.Index(PINECONE_INDEX_NAME)
#     logger.info(f"Connected to Pinecone index: {PINECONE_INDEX_NAME}")
#     self.__store = PineconeVectorStore(self.__index, OpenAIModel().model_embedding())
#     self.__retriever = self.__store.as_retriever(search_kwargs={"k": 3})
#     logger.info("PineconeStore initialized successfully")

#   def search(self, queries: List[str]) -> List[Document]:
#     try:
#       logger.info(f"Searching Pinecone with {len(queries)} queries")
#       with ThreadPoolExecutor() as executor:
#         docs = list(executor.map(lambda q: self.__retriever.invoke(q), queries))
#       result = list({doc.id: doc for sublist in docs for doc in sublist}.values())
#       logger.info(f"Search complete, found {len(result)} unique documents")
#       return result
#     except Exception as e:
#       logger.error(f"Error retrieving search results from Pinecone: {e}")
#       raise e

class UpstashStore:
  def __init__(self):
    logger.info("Initializing UpstashStore")
    self.__store = UpstashVectorStore(embedding=OpenAIModel().model_embedding())
    self.__retriever = self.__store.as_retriever(search_kwargs={"k": 3})
    logger.info("UpstashStore initialized successfully")

  def search(self, queries: List[str]) -> List[Document]:
    try:
      logger.info(f"Searching UpstashStore with {len(queries)} queries")
      with ThreadPoolExecutor() as executor:
        docs = list(executor.map(lambda q: self.__retriever.invoke(q), queries))
      result = list({doc.id: doc for sublist in docs for doc in sublist}.values())
      logger.info(f"Search complete, found {len(result)} unique documents")
      return result
    except Exception as e:
      logger.error(f"Error retrieving search results from UpstashStore: {e}")
      raise e


class RedisStore:
  def __init__(self):
    logger.info("Initializing RedisUpstashStore")
    self.__store = Redis(
      host=REDIS_HOST,
      port=REDIS_PORT,
      password=REDIS_PASSWORD,
      ssl=True
    )
    logger.info("RedisUpstashStore initialized successfully")

  def get_string(self, key: str) -> str:
    try:
      logger.info(f"Retrieving string from Redis for key: {key}")
      value = self.__store.get(key)
      if value is None:
        logger.warning(f"No value found for key: {key}")
        return ""
      logger.info(f"Retrieved value for key: {key}")
      return value.decode('utf-8')
    except Exception as e:
      logger.error(f"Error retrieving string from Redis: {e}")
      raise e

  def set_string(self, key: str, value: str) -> bool:
    try:
      logger.info(f"Setting string in Redis for key: {key}")
      self.__store.set(key, value)
      logger.info(f"String set successfully for key: {key}")
      return True
    except Exception as e:
      logger.error(f"Error setting string in Redis: {e}")
      raise e
