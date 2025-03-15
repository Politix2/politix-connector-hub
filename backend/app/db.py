import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from loguru import logger
from supabase import Client, create_client

from app.config import SUPABASE_KEY, SUPABASE_URL
from app.models import PlenarySession, TopicAnalysis, Tweet


class Database:
    """Database client for Supabase."""

    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized")

    def get_plenary_sessions(
        self, from_date: Optional[datetime] = None, analyzed: Optional[bool] = None
    ) -> List[PlenarySession]:
        """Get plenary sessions from database, optionally filtered by date and/or analysis status."""
        query = self.client.table("plenary_sessions")

        if from_date:
            query = query.gte("date", from_date.isoformat())

        if analyzed is not None:
            query = query.eq("analyzed", analyzed)

        response = query.select("*").execute()
        return [PlenarySession(**item) for item in response.data]

    def get_tweets(
        self, from_date: Optional[datetime] = None, analyzed: Optional[bool] = None
    ) -> List[Tweet]:
        """Get tweets from database, optionally filtered by date and/or analysis status."""
        query = self.client.table("tweets")

        if from_date:
            query = query.gte("posted_at", from_date.isoformat())

        if analyzed is not None:
            query = query.eq("analyzed", analyzed)

        response = query.select("*").execute()
        return [Tweet(**item) for item in response.data]

    def insert_plenary_session(self, session: PlenarySession) -> PlenarySession:
        """Insert a new plenary session into the database."""
        session_dict = session.dict(exclude={"id"})
        # Convert datetime objects to ISO format strings
        for key, value in session_dict.items():
            if isinstance(value, datetime):
                session_dict[key] = value.isoformat()
            elif isinstance(value, dict):
                session_dict[key] = json.dumps(value)

        response = self.client.table("plenary_sessions").insert(session_dict).execute()
        if response.data:
            return PlenarySession(**response.data[0])
        logger.error(f"Failed to insert plenary session: {response.error}")
        return session

    def insert_tweet(self, tweet: Tweet) -> Tweet:
        """Insert a new tweet into the database."""
        tweet_dict = tweet.dict(exclude={"id"})
        # Convert datetime objects to ISO format strings
        for key, value in tweet_dict.items():
            if isinstance(value, datetime):
                tweet_dict[key] = value.isoformat()
            elif isinstance(value, dict):
                tweet_dict[key] = json.dumps(value)

        response = self.client.table("tweets").insert(tweet_dict).execute()
        if response.data:
            return Tweet(**response.data[0])
        logger.error(f"Failed to insert tweet: {response.error}")
        return tweet

    def update_plenary_session_analysis(
        self, session_id: str, analyzed: bool, analysis_result: Dict[str, Any]
    ) -> bool:
        """Update the analysis result for a plenary session."""
        response = (
            self.client.table("plenary_sessions")
            .update(
                {"analyzed": analyzed, "analysis_result": json.dumps(analysis_result)}
            )
            .eq("id", session_id)
            .execute()
        )

        return bool(response.data)

    def update_tweet_analysis(
        self, tweet_id: str, analyzed: bool, analysis_result: Dict[str, Any]
    ) -> bool:
        """Update the analysis result for a tweet."""
        response = (
            self.client.table("tweets")
            .update(
                {"analyzed": analyzed, "analysis_result": json.dumps(analysis_result)}
            )
            .eq("id", tweet_id)
            .execute()
        )

        return bool(response.data)

    def insert_topic_analysis(self, analysis: TopicAnalysis) -> TopicAnalysis:
        """Insert a new topic analysis into the database."""
        analysis_dict = analysis.dict(exclude={"id"})
        # Convert datetime objects to ISO format strings
        for key, value in analysis_dict.items():
            if isinstance(value, datetime):
                analysis_dict[key] = value.isoformat()

        response = self.client.table("topic_analyses").insert(analysis_dict).execute()
        if response.data:
            return TopicAnalysis(**response.data[0])
        logger.error(f"Failed to insert topic analysis: {response.error}")
        return analysis

    def get_latest_collection_timestamp(self, content_type: str) -> Optional[datetime]:
        """Get the timestamp of the most recently collected item of the given type."""
        table = "plenary_sessions" if content_type == "plenary_session" else "tweets"
        timestamp_field = "date" if content_type == "plenary_session" else "posted_at"

        response = (
            self.client.table(table)
            .select(timestamp_field)
            .order(timestamp_field, desc=True)
            .limit(1)
            .execute()
        )

        if response.data and response.data[0]:
            timestamp_str = response.data[0][timestamp_field]
            return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

        return None


# Singleton database client
db = Database()
