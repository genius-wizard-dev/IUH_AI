from dotenv import load_dotenv
import os

# Load environment variables once
load_dotenv()

# Common environment variables
MONGO_URI = os.environ["MONGO_URI"]
MONGO_DB_NAME = os.environ["MONGO_DB_NAME"]
MONGO_COLLECTION_NAME = os.environ["MONGO_COLLECTION_NAME"]

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]

SERPER_API_KEY = os.environ["SERPER_API_KEY"]

FIRE_CRAWL_API_KEY = os.environ["FIRE_CRAWL_API_KEY"]

PERPLEXITY_API_KEY = os.environ["PERPLEXITY_API_KEY"]

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
# System configurations
max_workers = min(4, os.cpu_count() or 1)

# Add any other environment variables you use frequently
