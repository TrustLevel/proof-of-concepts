from typing import List, Optional

from entity_recognition import NamedEntity
from pydantic import BaseModel


class RawArticle(BaseModel):
    title: str
    url: str
    isodate: str
    author: str
    publisher: str
    content: Optional[str] = None


class ProcessedArticle(RawArticle):
    title: str
    url: str
    content: str 
    named_entities: List[NamedEntity]
    isodate: str
    author: str
    publisher: str
    trustlevel: float