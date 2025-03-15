from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PlenarySession(BaseModel):
    """Model for storing plenary session protocols."""

    id: Optional[str] = None
    title: str
    date: datetime
    content: str
    source_url: Optional[str] = None
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    analyzed: bool = False
    analysis_result: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class Tweet(BaseModel):
    """Model for storing tweets."""

    id: Optional[str] = None
    tweet_id: str
    user_handle: str
    user_name: Optional[str] = None
    content: str
    posted_at: datetime
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    analyzed: bool = False
    analysis_result: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class TopicAnalysis(BaseModel):
    """Model for topic analysis results."""

    id: Optional[str] = None
    content_id: str
    content_type: str  # "plenary_session" or "tweet"
    topics: List[str]
    sentiment: Optional[str] = None
    keywords: Optional[List[str]] = None
    analysis_date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class AnalysisRequest(BaseModel):
    """Model for requesting analysis of content."""

    content_id: str
    content_type: str  # "plenary_session" or "tweet"


class AnalysisResponse(BaseModel):
    """Model for returning analysis results."""

    content_id: str
    content_type: str
    topics: List[str]
    sentiment: Optional[str] = None
    keywords: Optional[List[str]] = None
