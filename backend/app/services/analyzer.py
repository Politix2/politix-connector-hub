from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from app.db import db
from app.llm import llm
from app.models import PlenarySession, TopicAnalysis, Tweet


class ContentAnalyzer:
    """Service for analyzing content using LLM."""

    def __init__(self):
        logger.info("Content analyzer initialized")

    async def analyze_plenary_session(
        self, session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Analyze a plenary session protocol using the LLM."""
        # Get sessions from database
        sessions = db.get_plenary_sessions()
        session = next((s for s in sessions if s.id == session_id), None)

        if not session:
            logger.error(f"Plenary session with ID {session_id} not found")
            return None

        logger.info(f"Analyzing plenary session: {session.title}")

        # Use the LLM to analyze the session content
        analysis_result = llm.analyze_topics(session.content)

        # Update the session with the analysis result
        success = db.update_plenary_session_analysis(
            session_id=session_id, analyzed=True, analysis_result=analysis_result
        )

        if success:
            # Save the topic analysis separately
            topic_analysis = TopicAnalysis(
                content_id=session_id,
                content_type="plenary_session",
                topics=analysis_result.get("topics", []),
                sentiment=analysis_result.get("sentiment"),
                keywords=analysis_result.get("keywords", []),
            )
            db.insert_topic_analysis(topic_analysis)

            logger.info(f"Successfully analyzed plenary session {session_id}")
            return analysis_result
        else:
            logger.error(f"Failed to update analysis for plenary session {session_id}")
            return None

    async def analyze_tweet(self, tweet_id: str) -> Optional[Dict[str, Any]]:
        """Analyze a tweet using the LLM."""
        # Get tweets from database
        tweets = db.get_tweets()
        tweet = next((t for t in tweets if t.id == tweet_id), None)

        if not tweet:
            logger.error(f"Tweet with ID {tweet_id} not found")
            return None

        logger.info(f"Analyzing tweet from: {tweet.user_handle}")

        # Use the LLM to analyze the tweet content
        analysis_result = llm.analyze_topics(tweet.content)

        # Update the tweet with the analysis result
        success = db.update_tweet_analysis(
            tweet_id=tweet_id, analyzed=True, analysis_result=analysis_result
        )

        if success:
            # Save the topic analysis separately
            topic_analysis = TopicAnalysis(
                content_id=tweet_id,
                content_type="tweet",
                topics=analysis_result.get("topics", []),
                sentiment=analysis_result.get("sentiment"),
                keywords=analysis_result.get("keywords", []),
            )
            db.insert_topic_analysis(topic_analysis)

            logger.info(f"Successfully analyzed tweet {tweet_id}")
            return analysis_result
        else:
            logger.error(f"Failed to update analysis for tweet {tweet_id}")
            return None

    async def run_analysis(self) -> Dict[str, int]:
        """Run analysis on all unanalyzed content."""
        # Get unanalyzed sessions and tweets
        unanalyzed_sessions = db.get_plenary_sessions(analyzed=False)
        unanalyzed_tweets = db.get_tweets(analyzed=False)

        analyzed_sessions_count = 0
        analyzed_tweets_count = 0

        # Analyze sessions
        for session in unanalyzed_sessions:
            result = await self.analyze_plenary_session(session.id)
            if result:
                analyzed_sessions_count += 1

        # Analyze tweets
        for tweet in unanalyzed_tweets:
            result = await self.analyze_tweet(tweet.id)
            if result:
                analyzed_tweets_count += 1

        return {
            "analyzed_sessions": analyzed_sessions_count,
            "analyzed_tweets": analyzed_tweets_count,
        }

    async def compare_content(
        self, content_id1: str, content_type1: str, content_id2: str, content_type2: str
    ) -> Optional[Dict[str, Any]]:
        """Compare two content items to find topic similarities and differences."""
        # Get the content items
        content1_text = await self._get_content_text(content_id1, content_type1)
        content2_text = await self._get_content_text(content_id2, content_type2)

        if not content1_text or not content2_text:
            return None

        # Use LLM to compare the topics
        comparison_result = llm.compare_topics(content1_text, content2_text)
        return comparison_result

    async def _get_content_text(
        self, content_id: str, content_type: str
    ) -> Optional[str]:
        """Get the text content of a session or tweet."""
        if content_type == "plenary_session":
            sessions = db.get_plenary_sessions()
            session = next((s for s in sessions if s.id == content_id), None)
            return session.content if session else None
        elif content_type == "tweet":
            tweets = db.get_tweets()
            tweet = next((t for t in tweets if t.id == content_id), None)
            return tweet.content if tweet else None
        else:
            logger.error(f"Invalid content type: {content_type}")
            return None


# Singleton content analyzer
analyzer = ContentAnalyzer()
