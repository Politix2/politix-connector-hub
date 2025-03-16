from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import UUID4, BaseModel

from app.db import db
from app.models import (
    AnalysisRequest,
    AnalysisResponse,
    PlenarySession,
    Topic,
    TopicAnalysis,
    TopicCreate,
    TopicMention,
    TopicMentionResponse,
    TopicResponse,
    TopicSubscription,
    TopicUpdate,
    Tweet,
    User,
)
from app.services.analyzer import analyzer
from app.services.collector import collector
from app.services.topic_analyzer import TopicAnalyzer

# API Router
router = APIRouter(prefix="/api", tags=["api"])
topic_analyzer = TopicAnalyzer()


# Additional request/response models
class CollectionRequest(BaseModel):
    """Request to run a data collection job."""

    from_date: Optional[datetime] = None


class CollectionResponse(BaseModel):
    """Response from a data collection job."""

    new_sessions: int
    new_tweets: int


class ComparisonRequest(BaseModel):
    """Request to compare two content items."""

    content_id1: str
    content_type1: str  # "plenary_session" or "tweet"
    content_id2: str
    content_type2: str  # "plenary_session" or "tweet"


class ComparisonResponse(BaseModel):
    """Response from a content comparison."""

    common_topics: List[str]
    unique_to_first: List[str]
    unique_to_second: List[str]
    summary: str


class UserResponse(BaseModel):
    """Response model for user information."""

    id: str
    email: str
    name: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None


class SubscriptionResponse(BaseModel):
    """Response for topic subscription."""

    id: str
    user_id: str
    topic_id: str
    topic_name: str
    created_at: datetime


# Models for analysis
class AnalysisResponse(BaseModel):
    id: str
    topic_id: str
    summary: str
    sentiment: str
    analyzed_at: datetime

    class Config:
        orm_mode = True


class TopicAnalysisRequest(BaseModel):
    topic_id: str


class UserTopicsAnalysisRequest(BaseModel):
    """Request to analyze all topics for a user."""

    user_id: str
    analyze_existing: bool = (
        False  # Whether to analyze topics that already have analyses
    )


class UserTopicsAnalysisResponse(BaseModel):
    """Response from analyzing all topics for a user."""

    success: bool
    message: str
    topics_analyzed: int
    topics_skipped: int
    topics_failed: int
    results: List[Dict[str, Any]]


# Endpoints
@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# User endpoints


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get a user by ID."""
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Topic endpoints
@router.post("/topics", response_model=Topic, status_code=status.HTTP_201_CREATED)
async def create_topic(topic: TopicCreate):
    """Create a new topic for tracking."""
    # Create the topic
    topic = Topic(
        name=topic.name,
        description=topic.description,
        keywords=topic.keywords,
        is_public=topic.is_public,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    created_topic = db.insert_topic(topic)

    # Return with counts
    topic_dict = created_topic.dict()
    topic_dict["mentions_count"] = 0  # New topic, no mentions yet
    return Topic(**topic_dict)


@router.get("/topics", response_model=List[Topic])
async def get_topics():
    """Get all public topics."""
    topics = db.get_topics(is_public=True)
    return topics


@router.get("/topics/{topic_id}", response_model=Topic)
async def get_topic(topic_id: str):
    """Get a topic by ID."""
    topic = db.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put("/topics/{topic_id}", response_model=TopicResponse)
async def update_topic(topic_id: str, topic_data: TopicUpdate):
    """Update a topic."""
    # Verify topic exists
    topic = db.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Prepare update data, only including fields that were provided
    update_data = {}
    if topic_data.name is not None:
        update_data["name"] = topic_data.name
    if topic_data.description is not None:
        update_data["description"] = topic_data.description
    if topic_data.keywords is not None:
        update_data["keywords"] = topic_data.keywords
    if topic_data.is_public is not None:
        update_data["is_public"] = topic_data.is_public

    # Update the topic
    success = db.update_topic(topic_id, update_data)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update topic")

    # Return the updated topic
    topic_with_count = db.get_topic_with_mentions_count(topic_id)
    return TopicResponse(**topic_with_count)


@router.delete("/topics/{topic_id}")
async def delete_topic(topic_id: str):
    """Delete a topic."""
    # Verify topic exists
    topic = db.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Delete the topic
    success = db.delete_topic(topic_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete topic")

    return {"message": "Topic deleted successfully"}


# Topic subscription endpoints
@router.post("/topics/{topic_id}/subscribe", response_model=SubscriptionResponse)
async def subscribe_to_topic(topic_id: str, user_id: str):
    """Subscribe a user to a topic."""
    # Verify user and topic exist
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    topic = db.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Check if already subscribed
    if db.is_user_subscribed(user_id, topic_id):
        raise HTTPException(
            status_code=400, detail="User is already subscribed to this topic"
        )

    # Create subscription
    subscription = db.subscribe_to_topic(user_id, topic_id)
    if not subscription:
        raise HTTPException(status_code=500, detail="Failed to create subscription")

    # Return with topic name for convenience
    return {
        "id": subscription.id,
        "user_id": subscription.user_id,
        "topic_id": subscription.topic_id,
        "topic_name": topic.name,
        "created_at": subscription.created_at,
    }


@router.delete("/topics/{topic_id}/unsubscribe")
async def unsubscribe_from_topic(topic_id: str, user_id: str):
    """Unsubscribe a user from a topic."""
    # Verify user and topic exist
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    topic = db.get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Check if subscribed
    if not db.is_user_subscribed(user_id, topic_id):
        raise HTTPException(
            status_code=400, detail="User is not subscribed to this topic"
        )

    # Delete subscription
    success = db.unsubscribe_from_topic(user_id, topic_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete subscription")

    return {"message": "Unsubscribed successfully"}


@router.get("/users/{user_id}/subscriptions", response_model=List[SubscriptionResponse])
async def get_user_subscriptions(user_id: str):
    """Get all topics a user is subscribed to."""
    # Verify user exists
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get subscriptions
    subscriptions = db.get_user_subscriptions(user_id)

    # Get topic names for each subscription
    result = []
    for subscription in subscriptions:
        topic = db.get_topic(subscription.topic_id)
        if topic:
            result.append(
                {
                    "id": subscription.id,
                    "user_id": subscription.user_id,
                    "topic_id": subscription.topic_id,
                    "topic_name": topic.name,
                    "created_at": subscription.created_at,
                }
            )

    return result


# Topic mentions endpoints
@router.get("/mentions", response_model=List[TopicMentionResponse])
async def get_topic_mentions(
    topic_id: Optional[str] = None, user_id: Optional[str] = None
):
    """Get mentions of topics with optional filtering."""
    # This will join mentions with their content details
    mentions = db.get_mentions_with_content(topic_id=topic_id, user_id=user_id)
    return mentions


@router.get("/users/{user_id}/mentions", response_model=List[TopicMentionResponse])
async def get_user_topic_mentions(user_id: str):
    """Get all mentions of topics created or subscribed to by a user."""
    # Verify user exists
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get mentions for this user's topics
    mentions = db.get_mentions_with_content(user_id=user_id)
    return mentions


# Existing endpoints
@router.get("/plenary-sessions", response_model=List[PlenarySession])
async def get_plenary_sessions(
    from_date: Optional[datetime] = None, analyzed: Optional[bool] = None
):
    """Get plenary sessions with optional filtering."""
    sessions = db.get_plenary_sessions(from_date=from_date, analyzed=analyzed)
    return sessions


@router.get("/plenary-sessions/{session_id}", response_model=PlenarySession)
async def get_plenary_session(session_id: str):
    """Get a specific plenary session by ID."""
    sessions = db.get_plenary_sessions()
    session = next((s for s in sessions if s.id == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Plenary session not found")
    return session


@router.get("/tweets", response_model=List[Tweet])
async def get_tweets(
    from_date: Optional[datetime] = None, analyzed: Optional[bool] = None
):
    """Get tweets with optional filtering."""
    tweets = db.get_tweets(from_date=from_date, analyzed=analyzed)
    return tweets


@router.get("/tweets/{tweet_id}", response_model=Tweet)
async def get_tweet(tweet_id: str):
    """Get a specific tweet by ID."""
    tweets = db.get_tweets()
    tweet = next((t for t in tweets if t.id == tweet_id), None)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_content(request: AnalysisRequest):
    """Analyze content for topics and sentiment."""
    if request.content_type == "plenary_session":
        result = await analyzer.analyze_plenary_session(request.content_id)
        if not result:
            raise HTTPException(
                status_code=404, detail="Plenary session not found or analysis failed"
            )
    elif request.content_type == "tweet":
        result = await analyzer.analyze_tweet(request.content_id)
        if not result:
            raise HTTPException(
                status_code=404, detail="Tweet not found or analysis failed"
            )
    else:
        raise HTTPException(status_code=400, detail="Invalid content type")

    return AnalysisResponse(
        content_id=request.content_id,
        content_type=request.content_type,
        topics=result.get("topics", []),
        sentiment=result.get("sentiment"),
        keywords=result.get("keywords", []),
    )


@router.post("/compare", response_model=ComparisonResponse)
async def compare_content(request: ComparisonRequest):
    """Compare two content items for topic similarities and differences."""
    result = await analyzer.compare_content(
        request.content_id1,
        request.content_type1,
        request.content_id2,
        request.content_type2,
    )

    if not result:
        raise HTTPException(
            status_code=404, detail="Content not found or comparison failed"
        )

    return ComparisonResponse(
        common_topics=result.get("common_topics", []),
        unique_to_first=result.get("unique_to_text1", []),
        unique_to_second=result.get("unique_to_text2", []),
        summary=result.get("summary", ""),
    )


@router.post("/collect", response_model=CollectionResponse)
async def collect_data(request: CollectionRequest = None):
    """Manually trigger data collection."""
    from_date = None
    if request and request.from_date:
        from_date = request.from_date

    result = await collector.run_collection()
    return CollectionResponse(
        new_sessions=result["new_sessions"], new_tweets=result["new_tweets"]
    )


# Analysis routes
@router.post("/analyses", response_model=AnalysisResponse)
async def analyze_topic(request: TopicAnalysisRequest):
    """
    Analyze a topic using the LLM analyzer.

    This endpoint will:
    1. Fetch plenary sessions and tweets from the database
    2. Use an LLM to find and extract content relevant to the topic
    3. Analyze and summarize the content
    4. Store the result in the database
    """
    try:
        result = topic_analyzer.analyze_topic(request.topic_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to analyze topic",
            )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing topic: {str(e)}",
        )


@router.get("/topics/{topic_id}/analyses", response_model=List[AnalysisResponse])
async def get_topic_analyses(topic_id: str):
    """Get all analyses for a specific topic."""
    try:
        analyses = topic_analyzer.get_analyses_for_topic(topic_id)
        return analyses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving analyses: {str(e)}",
        )


@router.post("/user-topics-analysis", response_model=UserTopicsAnalysisResponse)
async def analyze_user_topics(request: UserTopicsAnalysisRequest):
    """Analyze all topics for a specific user."""
    try:
        result = topic_analyzer.analyze_all_user_topics(
            request.user_id, not request.analyze_existing
        )
        return UserTopicsAnalysisResponse(
            success=True,
            message="Topics analyzed successfully",
            topics_analyzed=result["topics_analyzed"],
            topics_skipped=result["topics_skipped"],
            topics_failed=result["topics_failed"],
            results=result["results"],
        )
    except Exception as e:
        return UserTopicsAnalysisResponse(
            success=False,
            message=f"Error analyzing topics: {str(e)}",
            topics_analyzed=0,
            topics_skipped=0,
            topics_failed=0,
            results=[],
        )
