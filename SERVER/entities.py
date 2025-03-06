from pydantic import Field, BaseModel
from typing import Optional, Any

class Entry(BaseModel):
    question: str = Field(..., description="Question asked by the user")
    answer: str = Field(..., description="Answer provided by the assistant")
    time: str = Field(..., description="Time of the message")

class Message(BaseModel):
    chat_id: str = Field(..., description="Unique identifier for the chat")
    user_name: str = Field(..., description="Name of the user")
    entry: Entry



class EventGraph(BaseModel):
    """
    Class representing an event in the graph processing pipeline.
    Contains information about the current state, next state, and output data.
    """
    in_node: str
    next_state: str
    is_search: bool = False
    user_name: Optional[str] = None
    chat_id: Optional[str] = None
    output: Any = Field(default="")  # Set a default empty string to ensure this field always exists
