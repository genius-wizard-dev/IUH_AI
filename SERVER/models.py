from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models.perplexity import ChatPerplexity
from config import PERPLEXITY_API_KEY
from dotenv import load_dotenv
load_dotenv()

class OpenAIModel:
  def __init__(self):
    self.__model = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")
    self.__model_json = ChatOpenAI(temperature=0.0, model="gpt-4o-mini", model_kwargs={"response_format": {"type": "json_object"}})
    self.__model_embedding = OpenAIEmbeddings(model="text-embedding-3-small")

  def model(self):
    return self.__model

  def model_json(self):
    return self.__model_json

  def model_embedding(self):
    return self.__model_embedding


class GoogleModel:
  def __init__(self):
    self.__model = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.0-flash")

  def model(self):
    return self.__model


class PerplexityModel:
  def __init__(self):
    self.__model = ChatPerplexity(model="sonar", timeout=30, api_key=PERPLEXITY_API_KEY)

  def model(self):
    return self.__model
