from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.db import db
from app.models import (
    AnalysisRequest,
    AnalysisResponse,
    PlenarySession,
    TopicAnalysis,
    Tweet,
)
from app.services.analyzer import analyzer
from app.services.collector import collector

# API Router
router = APIRouter(prefix="/api", tags=["api"])


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


# Endpoints
@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


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
