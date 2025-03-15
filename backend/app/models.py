from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class User(BaseModel):
    """Model for application users."""

    id: Optional[str] = None
    email: str
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class Topic(BaseModel):
    """Model for topics that users want to track."""

    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    keywords: List[str]
    user_id: str
    is_public: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class TopicSubscription(BaseModel):
    """Model for user subscriptions to topics."""

    id: Optional[str] = None
    user_id: str
    topic_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class TopicMention(BaseModel):
    """Model for tracking when topics are mentioned in content."""

    id: Optional[str] = None
    topic_id: str
    content_id: str
    content_type: str  # "plenary_session" or "tweet"
    mention_context: Optional[str] = None
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    is_notified: bool = False

    class Config:
        from_attributes = True


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


# Request/Response models for Topics
class TopicCreate(BaseModel):
    """Model for creating a new topic."""

    name: str
    description: Optional[str] = None
    keywords: List[str]
    is_public: bool = False


class TopicUpdate(BaseModel):
    """Model for updating an existing topic."""

    name: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[List[str]] = None
    is_public: Optional[bool] = None


class TopicResponse(BaseModel):
    """Model for topic response with additional counts."""

    id: str
    name: str
    description: Optional[str] = None
    keywords: List[str]
    user_id: str
    is_public: bool
    created_at: datetime
    updated_at: datetime
    mentions_count: Optional[int] = None


# Request/Response models for Topic Mentions
class TopicMentionResponse(BaseModel):
    """Model for topic mention with associated content."""

    id: str
    topic_id: str
    topic_name: str
    content_id: str
    content_type: str
    content_title: Optional[str] = None
    content_preview: str
    mention_context: Optional[str] = None
    detected_at: datetime
