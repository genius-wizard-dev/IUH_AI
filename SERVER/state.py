from typing import List, Optional,Dict
from pydantic import BaseModel
from langchain.schema import Document
from enum import Enum

class Node(Enum):
    SEARCH = "SEARCH"
    STORE = "STORE"

class ContextAnalysis(BaseModel):
    intent: str
    type: str
    scope: str
    expected_output: str
    actions: str

class Summary(BaseModel):
    summary: str
    data_source: List[str]
    useful_info: str
    additional_info: str
    missing_info: str
    data_quality: str

class MainState(BaseModel):
    chat_id: str
    user_name: str
    question: str
    next_state: str
    history: List[Dict[str, str]]
    is_search: bool
    in_node: Optional[str] = None
    context_anlysis: Optional[ContextAnalysis]
    documents: List[Document]
    search_results: List[Document]
    from_node: Node | None
    prompt: str
    summary: Optional[Summary]
    output: str




