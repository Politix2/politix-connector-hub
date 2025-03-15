import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx
from dateutil import parser as date_parser
from loguru import logger

from app.db import db
from app.models import PlenarySession, Tweet


class DataCollector:
    """Service for collecting data from various sources."""

    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        logger.info("Data collector initialized")

    async def collect_plenary_sessions(
        self, from_timestamp: Optional[datetime] = None
    ) -> List[PlenarySession]:
        """
        Collect plenary session protocols from a source.

        In a real implementation, this would connect to an official API or scrape a website.
        For this example, we'll simulate by creating dummy data.
        """
        logger.info(f"Collecting plenary sessions from {from_timestamp}")

        # In a real implementation, you would:
        # 1. Connect to an API or scrape a website
        # 2. Parse the data
        # 3. Insert into the database

        # For this example, we'll create a dummy session
        if not from_timestamp:
            from_timestamp = datetime.utcnow() - timedelta(days=30)

        # Simulate fetching data
        dummy_sessions = [
            PlenarySession(
                title="Discussion on Climate Policy",
                date=datetime.utcnow() - timedelta(days=5),
                content="This session discussed various climate policy initiatives...",
                source_url="https://example.com/plenary/12345",
            ),
            PlenarySession(
                title="Budget Debates 2023",
                date=datetime.utcnow() - timedelta(days=3),
                content="The parliament debated the proposed budget for 2023...",
                source_url="https://example.com/plenary/12346",
            ),
        ]

        # Filter to only include sessions after from_timestamp
        new_sessions = [s for s in dummy_sessions if s.date > from_timestamp]

        # Insert into database
        inserted_sessions = []
        for session in new_sessions:
            inserted_session = db.insert_plenary_session(session)
            inserted_sessions.append(inserted_session)
            logger.info(f"Inserted plenary session: {inserted_session.title}")

        return inserted_sessions

    async def collect_tweets(
        self, from_timestamp: Optional[datetime] = None
    ) -> List[Tweet]:
        """
        Collect tweets from Twitter API.

        In a real implementation, this would use the Twitter API.
        For this example, we'll simulate by creating dummy data.
        """
        logger.info(f"Collecting tweets from {from_timestamp}")

        # In a real implementation, you would:
        # 1. Connect to the Twitter API
        # 2. Search for relevant tweets
        # 3. Insert into the database

        # For this example, we'll create dummy tweets
        if not from_timestamp:
            from_timestamp = datetime.utcnow() - timedelta(days=30)

        # Simulate fetching data
        dummy_tweets = [
            Tweet(
                tweet_id="123456789",
                user_handle="@politician1",
                user_name="Politician One",
                content="We need stronger climate policies now! #ClimateAction",
                posted_at=datetime.utcnow() - timedelta(days=4, hours=2),
            ),
            Tweet(
                tweet_id="987654321",
                user_handle="@politician2",
                user_name="Politician Two",
                content="The proposed budget needs revision. We cannot accept these cuts to healthcare. #Budget2023",
                posted_at=datetime.utcnow() - timedelta(days=2, hours=8),
            ),
        ]

        # Filter to only include tweets after from_timestamp
        new_tweets = [t for t in dummy_tweets if t.posted_at > from_timestamp]

        # Insert into database
        inserted_tweets = []
        for tweet in new_tweets:
            inserted_tweet = db.insert_tweet(tweet)
            inserted_tweets.append(inserted_tweet)
            logger.info(f"Inserted tweet from {inserted_tweet.user_handle}")

        return inserted_tweets

    async def run_collection(self) -> Dict[str, int]:
        """Run the data collection process for all sources."""
        # Get the latest timestamps for each content type
        latest_session_timestamp = db.get_latest_collection_timestamp("plenary_session")
        latest_tweet_timestamp = db.get_latest_collection_timestamp("tweet")

        # Collect new data
        new_sessions = await self.collect_plenary_sessions(latest_session_timestamp)
        new_tweets = await self.collect_tweets(latest_tweet_timestamp)

        return {"new_sessions": len(new_sessions), "new_tweets": len(new_tweets)}


# Singleton data collector
collector = DataCollector()
