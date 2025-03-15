import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from app.config import SUPABASE_KEY, SUPABASE_URL
from app.models import (
    PlenarySession,
    Topic,
    TopicAnalysis,
    TopicMention,
    TopicSubscription,
    Tweet,
    User,
)
from supabase import Client, create_client


class Database:
    """Database client for Supabase."""

    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized")

    # User operations
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        response = self.client.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            return User(**response.data[0])
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        response = self.client.table("users").select("*").eq("email", email).execute()
        if response.data:
            return User(**response.data[0])
        return None

    def insert_user(self, user: User) -> User:
        """Insert a new user."""
        user_dict = user.dict(exclude={"id"})
        # Convert datetime objects to ISO format strings
        for key, value in user_dict.items():
            if isinstance(value, datetime):
                user_dict[key] = value.isoformat()

        response = self.client.table("users").insert(user_dict).execute()
        if response.data:
            return User(**response.data[0])
        logger.error(f"Failed to insert user: {response.error}")
        return user

    def update_user(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Update user data."""
        # Convert any datetime objects to ISO format strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()

        response = self.client.table("users").update(data).eq("id", user_id).execute()
        return bool(response.data)

    def update_user_last_login(self, user_id: str) -> bool:
        """Update user's last login time."""
        return self.update_user(user_id, {"last_login": datetime.utcnow().isoformat()})

    # Topic operations
    def get_topics(
        self, user_id: Optional[str] = None, is_public: Optional[bool] = None
    ) -> List[Topic]:
        """Get topics with optional filtering by user and public status."""
        query = self.client.table("topics").select("*")

        if user_id:
            query = query.eq("user_id", user_id)

        if is_public is not None:
            query = query.eq("is_public", is_public)

        response = query.execute()
        return [Topic(**item) for item in response.data]

    def get_topic(self, topic_id: str) -> Optional[Topic]:
        """Get a topic by ID."""
        response = self.client.table("topics").select("*").eq("id", topic_id).execute()
        if response.data:
            return Topic(**response.data[0])
        return None

    def insert_topic(self, topic: Topic) -> Topic:
        """Insert a new topic."""
        topic_dict = topic.dict(exclude={"id"})
        # Convert datetime objects to ISO format strings
        for key, value in topic_dict.items():
            if isinstance(value, datetime):
                topic_dict[key] = value.isoformat()

        response = self.client.table("topics").insert(topic_dict).execute()
        if response.data:
            return Topic(**response.data[0])
        logger.error(f"Failed to insert topic: {response.error}")
        return topic

    def update_topic(self, topic_id: str, data: Dict[str, Any]) -> bool:
        """Update topic data."""
        # Add updated_at timestamp
        data["updated_at"] = datetime.utcnow().isoformat()

        # Convert any datetime objects to ISO format strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()

        response = self.client.table("topics").update(data).eq("id", topic_id).execute()
        return bool(response.data)

    def delete_topic(self, topic_id: str) -> bool:
        """Delete a topic."""
        response = self.client.table("topics").delete().eq("id", topic_id).execute()
        return bool(response.data)

    def get_topic_with_mentions_count(self, topic_id: str) -> Optional[Dict[str, Any]]:
        """Get a topic with its mention count."""
        # This would typically be a join, but we'll do it in two queries for simplicity
        topic = self.get_topic(topic_id)
        if not topic:
            return None

        count_response = (
            self.client.table("topic_mentions")
            .select("id", "count")
            .eq("topic_id", topic_id)
            .execute()
        )
        mention_count = len(count_response.data) if count_response.data else 0

        topic_dict = topic.dict()
        topic_dict["mentions_count"] = mention_count
        return topic_dict

    # Topic subscription operations
    def get_user_subscriptions(self, user_id: str) -> List[TopicSubscription]:
        """Get all topic subscriptions for a user."""
        response = (
            self.client.table("topic_subscriptions")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return [TopicSubscription(**item) for item in response.data]

    def get_topic_subscribers(self, topic_id: str) -> List[TopicSubscription]:
        """Get all users subscribed to a topic."""
        response = (
            self.client.table("topic_subscriptions")
            .select("*")
            .eq("topic_id", topic_id)
            .execute()
        )
        return [TopicSubscription(**item) for item in response.data]

    def is_user_subscribed(self, user_id: str, topic_id: str) -> bool:
        """Check if a user is subscribed to a topic."""
        response = (
            self.client.table("topic_subscriptions")
            .select("id")
            .eq("user_id", user_id)
            .eq("topic_id", topic_id)
            .execute()
        )
        return bool(response.data)

    def subscribe_to_topic(
        self, user_id: str, topic_id: str
    ) -> Optional[TopicSubscription]:
        """Subscribe a user to a topic."""
        subscription_data = {
            "user_id": user_id,
            "topic_id": topic_id,
            "created_at": datetime.utcnow().isoformat(),
        }

        try:
            response = (
                self.client.table("topic_subscriptions")
                .insert(subscription_data)
                .execute()
            )
            if response.data:
                return TopicSubscription(**response.data[0])
            return None
        except Exception as e:
            logger.error(f"Failed to subscribe to topic: {e}")
            return None

    def unsubscribe_from_topic(self, user_id: str, topic_id: str) -> bool:
        """Unsubscribe a user from a topic."""
        response = (
            self.client.table("topic_subscriptions")
            .delete()
            .eq("user_id", user_id)
            .eq("topic_id", topic_id)
            .execute()
        )
        return bool(response.data)

    # Topic mention operations
    def get_topic_mentions(
        self,
        topic_id: Optional[str] = None,
        user_id: Optional[str] = None,
        is_notified: Optional[bool] = None,
    ) -> List[TopicMention]:
        """Get topic mentions with optional filtering."""
        query = self.client.table("topic_mentions").select("*")

        if topic_id:
            query = query.eq("topic_id", topic_id)

        if user_id:
            # This requires a join with topics table to filter by user_id
            # We'll simplify and assume the caller handles this filtering
            pass

        if is_notified is not None:
            query = query.eq("is_notified", is_notified)

        response = query.execute()
        return [TopicMention(**item) for item in response.data]

    def insert_topic_mention(self, mention: TopicMention) -> TopicMention:
        """Insert a new topic mention."""
        mention_dict = mention.dict(exclude={"id"})
        # Convert datetime objects to ISO format strings
        for key, value in mention_dict.items():
            if isinstance(value, datetime):
                mention_dict[key] = value.isoformat()

        response = self.client.table("topic_mentions").insert(mention_dict).execute()
        if response.data:
            return TopicMention(**response.data[0])
        logger.error(f"Failed to insert topic mention: {response.error}")
        return mention

    def mark_mention_as_notified(self, mention_id: str) -> bool:
        """Mark a topic mention as notified."""
        response = (
            self.client.table("topic_mentions")
            .update({"is_notified": True})
            .eq("id", mention_id)
            .execute()
        )
        return bool(response.data)

    def get_mentions_with_content(
        self,
        topic_id: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Get topic mentions with their associated content details."""
        # This would typically be a complex join, but we'll simulate it with multiple queries
        mentions = self.get_topic_mentions(topic_id=topic_id, is_notified=None)

        result = []
        for mention in mentions[:limit]:
            # Get topic info
            topic = self.get_topic(mention.topic_id)

            # Skip if we're filtering by user_id and this mention doesn't match
            if user_id and topic and topic.user_id != user_id:
                continue

            # Get content based on content_type
            content_title = None
            content_preview = ""

            if mention.content_type == "plenary_session":
                sessions = self.get_plenary_sessions()
                session = next(
                    (s for s in sessions if s.id == mention.content_id), None
                )
                if session:
                    content_title = session.title
                    content_preview = (
                        session.content[:200] + "..."
                        if len(session.content) > 200
                        else session.content
                    )
            elif mention.content_type == "tweet":
                tweets = self.get_tweets()
                tweet = next((t for t in tweets if t.id == mention.content_id), None)
                if tweet:
                    content_title = f"Tweet by {tweet.user_handle}"
                    content_preview = tweet.content

            # Create result with all the info
            result.append(
                {
                    "id": mention.id,
                    "topic_id": mention.topic_id,
                    "topic_name": topic.name if topic else "Unknown Topic",
                    "content_id": mention.content_id,
                    "content_type": mention.content_type,
                    "content_title": content_title,
                    "content_preview": content_preview,
                    "mention_context": mention.mention_context,
                    "detected_at": mention.detected_at,
                }
            )

        return result

    # Existing methods for plenary sessions and tweets
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
