
import asyncio
from datetime import datetime
from typing import Dict, List, Optional

from loguru import logger

from app.db import db
from app.llm import llm
from app.models import PlenarySession, TopicAnalysis, Tweet

class TopicMonitor:
    """Service for monitoring topics in plenary sessions and tweets."""

    def __init__(self):
        logger.info("Topic monitor initialized")

    async def get_relevant_content(self, topics: List[str], limit: int = 10) -> Dict:
        """Get content relevant to the provided topics."""
        # Get analyzed sessions and tweets from database
        sessions = db.get_plenary_sessions(analyzed=True)
        tweets = db.get_tweets(analyzed=True)
        
        # Get topic analyses
        analyses = db.get_topic_analyses()
        
        # Map content IDs to their analyses
        content_topics = {}
        for analysis in analyses:
            content_topics[analysis.content_id] = analysis.topics
        
        # Filter sessions by topic relevance
        relevant_sessions = []
        for session in sessions:
            session_topics = content_topics.get(session.id, [])
            if any(topic in session_topics for topic in topics):
                relevant_sessions.append({
                    "id": session.id,
                    "title": session.title,
                    "date": session.date,
                    "description": session.content[:150] + "..." if len(session.content) > 150 else session.content,
                    "topics": session_topics,
                    "type": "parliament"
                })
        
        # Filter tweets by topic relevance
        relevant_tweets = []
        for tweet in tweets:
            tweet_topics = content_topics.get(tweet.id, [])
            if any(topic in tweet_topics for topic in topics):
                relevant_tweets.append({
                    "id": tweet.id,
                    "author": tweet.user_handle,
                    "content": tweet.content,
                    "date": tweet.date,
                    "topics": tweet_topics,
                    "type": "tweet"
                })
        
        # Sort by date (newest first) and limit results
        all_content = sorted(
            relevant_sessions + relevant_tweets,
            key=lambda x: x["date"],
            reverse=True
        )[:limit]
        
        return {
            "content": all_content,
            "total": len(all_content)
        }

    async def get_priority_alerts(self, topics: List[str], limit: int = 3) -> List[Dict]:
        """Get high priority alerts for the specified topics."""
        # In a real implementation, this would use more sophisticated logic
        # to determine what constitutes a "high priority" alert
        
        relevant_content = await self.get_relevant_content(topics)
        
        # For now, we'll just mark parliamentary content as potential alerts
        alerts = []
        for item in relevant_content["content"]:
            if item["type"] == "parliament":
                # Use LLM to determine if this is high priority
                summary = f"Title: {item['title']}\nDescription: {item['description']}"
                analysis = llm.analyze_topics(summary)
                
                # Simple heuristic: if sentiment is negative or keywords suggest urgency
                keywords = analysis.get("keywords", [])
                urgent_words = ["urgent", "critical", "immediate", "deadline", "vote", "debate"]
                
                is_urgent = (
                    analysis.get("sentiment") == "negative" or
                    any(word in " ".join(keywords).lower() for word in urgent_words)
                )
                
                if is_urgent:
                    alerts.append({
                        **item,
                        "priority": "high",
                        "reason": "Upcoming legislative action that may impact your interests"
                    })
        
        return alerts[:limit]


# Singleton topic monitor
monitor = TopicMonitor()
