from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from app.db import db
from app.models import (
    PlenarySession,
    Topic,
    TopicAnalysis,
    TopicMention,
    Tweet,
)
from app.services import llm


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

            # Check for user-defined topics in the content
            await self.detect_user_topics(
                content_id=session_id,
                content_type="plenary_session",
                content_text=session.content,
                title=session.title,
                analyzed_topics=analysis_result.get("topics", []),
                analyzed_keywords=analysis_result.get("keywords", []),
            )

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

            # Check for user-defined topics in the content
            await self.detect_user_topics(
                content_id=tweet_id,
                content_type="tweet",
                content_text=tweet.content,
                title=f"Tweet by {tweet.user_handle}",
                analyzed_topics=analysis_result.get("topics", []),
                analyzed_keywords=analysis_result.get("keywords", []),
            )

            logger.info(f"Successfully analyzed tweet {tweet_id}")
            return analysis_result
        else:
            logger.error(f"Failed to update analysis for tweet {tweet_id}")
            return None

    async def detect_user_topics(
        self,
        content_id: str,
        content_type: str,
        content_text: str,
        title: str,
        analyzed_topics: List[str] = None,
        analyzed_keywords: List[str] = None,
    ) -> List[TopicMention]:
        """
        Detect mentions of user-defined topics in content.

        Args:
            content_id: ID of the content being analyzed
            content_type: "plenary_session" or "tweet"
            content_text: The text content to analyze
            title: Title or identifier for the content
            analyzed_topics: Topics already extracted by LLM analysis
            analyzed_keywords: Keywords already extracted by LLM analysis

        Returns:
            List of topic mentions detected
        """
        logger.info(f"Detecting user-defined topics in {content_type} {content_id}")

        content_lower = content_text.lower()
        mentions = []

        # Get all user-defined topics
        topics = db.get_topics()

        for topic in topics:
            # Check if any of the topic's keywords are in the content
            found_keywords = []
            for keyword in topic.keywords:
                if keyword.lower() in content_lower:
                    found_keywords.append(keyword)

            # Check if the topic name itself is in the content
            if topic.name.lower() in content_lower:
                found_keywords.append(topic.name)

            # Check if LLM detected any matching topics or keywords
            if analyzed_topics:
                for analyzed_topic in analyzed_topics:
                    if analyzed_topic.lower() == topic.name.lower() or any(
                        keyword.lower() in analyzed_topic.lower()
                        for keyword in topic.keywords
                    ):
                        found_keywords.append(analyzed_topic)

            if analyzed_keywords:
                for analyzed_keyword in analyzed_keywords:
                    if analyzed_keyword.lower() == topic.name.lower() or any(
                        keyword.lower() in analyzed_keyword.lower()
                        for keyword in topic.keywords
                    ):
                        found_keywords.append(analyzed_keyword)

            # If there's a match, create a topic mention
            if found_keywords:
                # Create a context snippet showing where the topic was mentioned
                context = self.extract_context(content_text, found_keywords[0], 150)

                # Create topic mention
                mention = TopicMention(
                    topic_id=topic.id,
                    content_id=content_id,
                    content_type=content_type,
                    mention_context=context,
                    detected_at=datetime.utcnow(),
                    is_notified=False,
                )

                saved_mention = db.insert_topic_mention(mention)
                if saved_mention:
                    mentions.append(saved_mention)
                    logger.info(
                        f"Detected topic '{topic.name}' in {content_type} '{title}'"
                    )

        return mentions

    def extract_context(self, text: str, keyword: str, context_size: int = 150) -> str:
        """Extract a context snippet around a keyword match."""
        keyword_lower = keyword.lower()
        text_lower = text.lower()

        # Find the position of the keyword
        position = text_lower.find(keyword_lower)
        if position == -1:
            return ""

        # Calculate the snippet boundaries
        start = max(0, position - context_size // 2)
        end = min(len(text), position + len(keyword) + context_size // 2)

        # Extract the snippet
        snippet = text[start:end]

        # Add ellipses if the snippet doesn't start/end at text boundaries
        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."

        return snippet

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
