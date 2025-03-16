#!/usr/bin/env python3
"""
Topic analyzer service for extracting relevant content from plenary sessions and tweets.
This service uses an LLM to find, extract, and summarize content related to specific topics.
"""

import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import dotenv
from dotenv import load_dotenv
from loguru import logger

from supabase import create_client

# Import Mistral client
try:
    from mistralai.client import MistralClient

    logger.info("Successfully imported Mistral client")
except ImportError as e:
    logger.error(f"Failed to import Mistral client: {e}")
    sys.exit(1)

dotenv.load_dotenv()

# Configure Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Configure Mistral client
mistral_api_key = os.getenv("MISTRAL_API_KEY")
mistral_client = MistralClient(api_key=mistral_api_key)


class TopicAnalyzer:
    """Service for analyzing plenary sessions and tweets for relevant topic content."""

    def __init__(self):
        """Initialize the topic analyzer service."""
        self.model_name = "mistral-large-latest"
        self.max_tokens = 4096
        self.temperature = 0.1  # Low temperature for more focused, analytical responses

    def fetch_topic_details(self, topic_id: str) -> Dict[str, Any]:
        """Fetch details about a specific topic."""
        response = supabase.table("topics").select("*").eq("id", topic_id).execute()

        if not response.data:
            raise ValueError(f"Topic with ID {topic_id} not found")

        return response.data[0]

    def fetch_plenary_sessions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch plenary sessions from the database."""
        response = supabase.table("plenary_sessions").select("*").limit(limit).execute()
        return response.data

    def fetch_tweets(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch tweets from the database."""
        response = supabase.table("tweets").select("*").limit(limit).execute()
        return response.data

    def create_analysis_prompt(
        self,
        topic: Dict[str, Any],
        sessions: List[Dict[str, Any]],
        tweets: List[Dict[str, Any]],
    ) -> str:
        """
        Create a prompt for the LLM to analyze content related to a specific topic.
        """
        # Format the topic information
        topic_info = f"Topic: {topic['name']}\nDescription: {topic['description'] or 'N/A'}\nKeywords: {', '.join(topic['keywords'])}\n\n"

        # Format plenary sessions
        sessions_text = "--- PLENARY SESSIONS ---\n"
        for i, session in enumerate(sessions):
            sessions_text += (
                f"[Session {i + 1}] {session['title']} ({session['date']})\n"
            )
            sessions_text += f"Content: {session['content'][:1000]}...\n\n"

        # Format tweets
        tweets_text = "--- TWEETS ---\n"
        for i, tweet in enumerate(tweets):
            tweets_text += (
                f"[Tweet {i + 1}] @{tweet['user_handle']} ({tweet['posted_at']})\n"
            )
            tweets_text += f"Content: {tweet['content']}\n\n"

        # Create the instruction prompt
        instruction = f"""
You are a political analyst assistant tasked with finding and analyzing content related to specific political topics.

TASK:
1. Find and extract ALL relevant text from the plenary sessions and tweets that is connected to the given topic.
2. Identify the most significant or recent discussion about this topic from the provided content.
3. Analyze what political opinions, positions, and sentiments are expressed about this topic.
4. Summarize the overall discourse around this topic.
5. Provide context about why this topic is politically significant based on the content.

IMPORTANT: Your response must be ONLY valid JSON. Do not include any explanations, markdown formatting, code blocks, or additional text. Your entire response should be parseable by json.loads().

Format your response STRICTLY as a JSON object with the following keys:
- "date": Format as "Month Day, Year" based on when the most significant discussion occurred
- "title": A concise title for the most important insight or discussion found
- "source": The specific source (e.g., "Parliamentary Committee on AI Safety" or similar relevant body)
- "priority": Use only one of these values: "urgent", "important", "routine", or "informational" 
- "description": A concise summary of the key insight or discussion (1-2 sentences)
- "details": More detailed information about the discussion and requirements
- "topics": A list of strings representing all topics discussed in relation to the main topic
- "relevant_extracts": List of found relevant text segments with source IDs
- "sentiment": Use only one of these values: "positive", "negative", "neutral", or "mixed"

Example of the expected response format:
{{
  "date": "March 15, 2024",
  "title": "Parliamentary Debate on Migration Policy",
  "source": "European Parliament Plenary Session",
  "priority": "important",
  "description": "MEPs debated new proposals for strengthening the EU migration framework with divergent opinions on border security versus humanitarian concerns.",
  "details": "The plenary session featured extensive discussion on the Migration and Asylum Pact, with conservative members emphasizing border security while progressive members focused on humanitarian protections.",
  "topics": ["migration", "asylum policy", "border security", "humanitarian aid"],
  "relevant_extracts": ["Session 1: MEPs emphasized the need for a balanced approach...", "Tweet 3: @MEP_Smith argues that humanitarian concerns must be prioritized..."],
  "sentiment": "mixed"
}}

{topic_info}

THE CONTENT TO ANALYZE:

{sessions_text}

{tweets_text}
"""
        return instruction

    def analyze_topic(self, topic_id: str) -> Dict[str, Any]:
        """
        Analyze content related to a specific topic and store the result.
        """
        # Fetch data
        topic = self.fetch_topic_details(topic_id)
        sessions = self.fetch_plenary_sessions()
        tweets = self.fetch_tweets()

        # Create prompt
        prompt = self.create_analysis_prompt(topic, sessions, tweets)

        # Call LLM
        logger.info(f"Analyzing topic: {topic['name']}")

        # Use ChatMessage for Mistral client 0.0.7
        from mistralai.models.chat_completion import ChatMessage

        response = mistral_client.chat(
            model=self.model_name,
            messages=[ChatMessage(role="user", content=prompt)],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        analysis_text = response.choices[0].message.content

        # Process the response (assuming it's properly formatted JSON)
        import json
        import re

        # Clean up the response text to handle potential formatting issues
        cleaned_text = analysis_text.strip()

        # Remove markdown code blocks if present
        if cleaned_text.startswith("```json") and cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[7:-3].strip()
        elif cleaned_text.startswith("```") and cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[3:-3].strip()

        # Remove any leading/trailing text that's not part of the JSON
        json_start = cleaned_text.find("{")
        json_end = cleaned_text.rfind("}")
        if json_start != -1 and json_end != -1:
            cleaned_text = cleaned_text[json_start : json_end + 1]

        try:
            analysis_data = json.loads(cleaned_text)

            # Log successful JSON parsing
            logger.info("Successfully parsed JSON response from LLM")

            # Ensure required fields are present with default values if missing
            required_fields = {
                "date": datetime.now().strftime("%B %d, %Y"),
                "title": f"Analysis of {topic['name']}",
                "source": "Automatic Topic Analysis",
                "priority": "routine",
                "description": "No specific description provided by analysis",
                "details": "No detailed information provided by analysis",
                "topics": topic["keywords"] if "keywords" in topic else ["general"],
                "sentiment": "neutral",  # Default sentiment
            }

            # Add any missing required fields to the analysis data
            for field, default_value in required_fields.items():
                if field not in analysis_data:
                    analysis_data[field] = default_value
                    logger.warning(
                        f"Missing required field '{field}' in LLM response, using default"
                    )

        except json.JSONDecodeError as e:
            # If JSON parsing fails, create a structured response with the raw text
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            logger.debug(f"Raw response: {analysis_text}")
            current_date = datetime.now().strftime("%B %d, %Y")
            analysis_data = {
                "date": current_date,
                "title": f"Analysis of {topic['name']}",
                "source": "Automatic Topic Analysis",
                "priority": "routine",
                "description": "Analysis output could not be properly formatted",
                "details": f"Error parsing LLM output: {e}. First 500 characters: {analysis_text[:500]}...",
                "topics": topic["keywords"] if "keywords" in topic else ["general"],
                "sentiment": "neutral",  # Default sentiment
                "raw_response": analysis_text,
            }

        # Get a content_id and content_type from one of the sessions or tweets
        content_id = None
        content_type = None

        if sessions:
            # Use the first session's ID as content_id
            content_id = sessions[0]["id"]
            content_type = "plenary_session"
        elif tweets:
            # If no sessions, use the first tweet's ID as content_id
            content_id = tweets[0]["id"]
            content_type = "tweet"
        else:
            # If no sessions or tweets, log an error and use placeholders
            logger.error("No sessions or tweets found to associate with this analysis")
            # Create a placeholder UUID for content_id
            import uuid

            content_id = str(uuid.uuid4())
            content_type = "generated"  # Generic type for generated content

        # Ensure sentiment is one of the valid values
        valid_sentiments = ["positive", "negative", "neutral", "mixed"]
        sentiment = analysis_data.get("sentiment", "neutral")
        if sentiment not in valid_sentiments:
            logger.warning(
                f"Invalid sentiment value '{sentiment}', defaulting to 'neutral'"
            )
            sentiment = "neutral"  # Default to neutral if invalid

        # Extract topics from analysis data or use keywords
        topics = analysis_data.get("topics", [])
        if not topics:
            topics = (
                topic["keywords"]
                if "keywords" in topic and topic["keywords"]
                else ["general"]
            )

        # Store result in database
        analysis_record = {
            "topic_id": topic_id,
            "content_id": content_id,
            "content_type": content_type,
            "analysis_data": analysis_data,
            "relevant_extracts": analysis_data.get("relevant_extracts", []),
            "summary": analysis_data.get("description", "No description available"),
            "sentiment": sentiment,
            "topics": topics,  # Add topics as separate field
            "analyzed_at": datetime.now().isoformat(),
        }

        # Add debug output for the raw response
        print("\n=== RAW LLM RESPONSE ===")
        print(analysis_text)
        print("\n=== CLEANED AND PARSED RESULT ===")
        import pprint

        pprint.pprint(analysis_data)

        # Store in database
        response = supabase.table("topic_analyses").insert(analysis_record).execute()

        if response.data:
            logger.info(f"Analysis stored successfully for topic: {topic['name']}")
            return analysis_record
        else:
            logger.error(f"Failed to store analysis for topic: {topic['name']}")
            return None

    def get_analyses_for_topic(self, topic_id: str) -> List[Dict[str, Any]]:
        """Get all analyses for a specific topic."""
        response = (
            supabase.table("topic_analyses")
            .select("*")
            .eq("topic_id", topic_id)
            .execute()
        )
        return response.data

    def fetch_user_topics(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch all topics belonging to a specific user."""
        response = supabase.table("topics").select("*").eq("user_id", user_id).execute()
        return response.data

    def analyze_all_user_topics(
        self, user_id: str, skip_existing: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze all topics belonging to a specific user.

        Args:
            user_id: The ID of the user whose topics will be analyzed
            skip_existing: If True, skip topics that already have analyses

        Returns:
            A dictionary with results of the operation
        """
        # Fetch all topics for this user
        topics = self.fetch_user_topics(user_id)

        if not topics:
            logger.warning(f"No topics found for user {user_id}")
            return {
                "success": False,
                "message": f"No topics found for user {user_id}",
                "topics_analyzed": 0,
                "topics_skipped": 0,
                "topics_failed": 0,
                "results": [],
            }

        # Keep track of results
        results = []
        topics_analyzed = 0
        topics_skipped = 0
        topics_failed = 0

        logger.info(f"Starting analysis of {len(topics)} topics for user {user_id}")

        # Process each topic
        for topic in topics:
            topic_id = topic["id"]
            topic_name = topic["name"]

            # Check if this topic already has analyses
            if skip_existing:
                existing_analyses = self.get_analyses_for_topic(topic_id)
                if existing_analyses:
                    logger.info(
                        f"Skipping topic '{topic_name}' ({topic_id}) - already has {len(existing_analyses)} analyses"
                    )
                    topics_skipped += 1
                    results.append(
                        {
                            "topic_id": topic_id,
                            "topic_name": topic_name,
                            "status": "skipped",
                            "reason": f"Already has {len(existing_analyses)} analyses",
                        }
                    )
                    continue

            # Analyze this topic
            logger.info(f"Analyzing topic '{topic_name}' ({topic_id})")
            try:
                analysis_result = self.analyze_topic(topic_id)
                if analysis_result:
                    topics_analyzed += 1
                    results.append(
                        {
                            "topic_id": topic_id,
                            "topic_name": topic_name,
                            "status": "success",
                            "analysis_id": analysis_result.get("id"),
                        }
                    )
                    logger.info(
                        f"Successfully analyzed topic '{topic_name}' ({topic_id})"
                    )
                else:
                    topics_failed += 1
                    results.append(
                        {
                            "topic_id": topic_id,
                            "topic_name": topic_name,
                            "status": "failed",
                            "reason": "Analysis function returned None",
                        }
                    )
                    logger.error(f"Failed to analyze topic '{topic_name}' ({topic_id})")
            except Exception as e:
                topics_failed += 1
                results.append(
                    {
                        "topic_id": topic_id,
                        "topic_name": topic_name,
                        "status": "failed",
                        "reason": str(e),
                    }
                )
                logger.error(f"Error analyzing topic '{topic_name}' ({topic_id}): {e}")
                import traceback

                logger.debug(traceback.format_exc())

        # Return summary
        return {
            "success": True,
            "message": f"Analyzed {topics_analyzed} topics, skipped {topics_skipped}, failed {topics_failed}",
            "topics_analyzed": topics_analyzed,
            "topics_skipped": topics_skipped,
            "topics_failed": topics_failed,
            "results": results,
        }


def main():
    """
    Run the topic analyzer directly without parameters.
    This function uses hardcoded values for quick testing.
    """
    # Hardcoded values for testing - USE VALID IDs FROM YOUR DATABASE
    topic_id = "e422e1eb-b72e-4be3-8bb6-d53ffe41d3d4"  # ID of the topic to analyze

    # Change this to True to analyze all topics for a user instead of a single topic
    analyze_user_topics = True
    user_id = "67c4d1bb-5ac1-4514-b7ec-88e56a5de123"  # Only used if analyze_user_topics is True
    skip_existing_analyses = True  # Skip topics that already have analyses

    try:
        # Initialize the analyzer
        analyzer = TopicAnalyzer()

        if analyze_user_topics:
            # Analyze all topics for a user
            print(f"\nAnalyzing all topics for user: {user_id}")
            if not skip_existing_analyses:
                print(
                    "Note: Analyzing ALL topics, including those with existing analyses"
                )

            # Run the analysis
            result = analyzer.analyze_all_user_topics(user_id, skip_existing_analyses)

            # Display the results
            print("\n=== ANALYSIS SUMMARY ===")
            print(f"Status: {'Success' if result['success'] else 'Failed'}")
            print(f"Message: {result['message']}")
            print(f"Topics analyzed: {result['topics_analyzed']}")
            print(f"Topics skipped: {result['topics_skipped']}")
            print(f"Topics failed: {result['topics_failed']}")

            if result["results"]:
                print("\nDetailed results:")
                for res in result["results"]:
                    status_display = {
                        "success": "✅ Success",
                        "skipped": "⏭️ Skipped",
                        "failed": "❌ Failed",
                    }.get(res["status"], res["status"])

                    print(
                        f"  - {res['topic_name']} ({res['topic_id']}): {status_display}"
                    )
                    if res["status"] == "failed":
                        print(f"    Reason: {res.get('reason', 'Unknown error')}")
        else:
            # Analyze a single topic
            # Fetch the topic details
            try:
                topic = analyzer.fetch_topic_details(topic_id)
                print(f"\nAnalyzing Topic: {topic['name']}")
                print(f"Description: {topic['description'] or 'N/A'}")
                print(f"Keywords: {', '.join(topic['keywords'])}")
            except ValueError as e:
                print(f"Error: Topic not found - {e}")
                return 1

            # Fetch the sessions and tweets and print info for debugging
            sessions = analyzer.fetch_plenary_sessions()
            tweets = analyzer.fetch_tweets()

            print(f"\n=== DATA BEING ANALYZED ===")
            print(f"Number of plenary sessions: {len(sessions)}")
            if sessions:
                print("First few plenary sessions:")
                for i, session in enumerate(sessions[:3]):  # Show first 3 sessions
                    print(
                        f"  - {session.get('title', 'No title')} ({session.get('date', 'No date')})"
                    )
                    print(f"    ID: {session.get('id', 'No ID')}")
                    content_preview = (
                        session.get("content", "")[:100] + "..."
                        if session.get("content")
                        else "No content"
                    )
                    print(f"    Content preview: {content_preview}")
            else:
                print("No plenary sessions found.")

            print(f"\nNumber of tweets: {len(tweets)}")
            if tweets:
                print("First few tweets:")
                for i, tweet in enumerate(tweets[:3]):  # Show first 3 tweets
                    print(
                        f"  - @{tweet.get('user_handle', 'No handle')} ({tweet.get('posted_at', 'No date')})"
                    )
                    print(f"    ID: {tweet.get('id', 'No ID')}")
                    content_preview = (
                        tweet.get("content", "")[:100] + "..."
                        if tweet.get("content")
                        else "No content"
                    )
                    print(f"    Content preview: {content_preview}")
            else:
                print("No tweets found.")

            # Run the analysis
            print("\nRunning analysis...")
            result = analyzer.analyze_topic(topic_id)

            if not result:
                print("Error: Analysis failed")
                return 1

            # Display the results
            print("\n=== ANALYSIS RESULTS ===\n")
            print(f"Analysis ID: {result.get('id', 'Unknown')}")
            print(f"Analyzed at: {result.get('analyzed_at', 'Unknown')}")

            if "analysis_data" in result:
                analysis_data = result["analysis_data"]

                # Display main analysis fields
                print(f"\nDate: {analysis_data.get('date', 'Not specified')}")
                print(f"Title: {analysis_data.get('title', 'Not specified')}")
                print(f"Source: {analysis_data.get('source', 'Not specified')}")
                print(
                    f"Priority: {analysis_data.get('priority', 'Not specified').upper()}"
                )
                print(
                    f"\nDescription: {analysis_data.get('description', 'No description available')}"
                )

                # Display topics
                if "topics" in analysis_data and analysis_data["topics"]:
                    print("\nTopics:")
                    for topic in analysis_data["topics"]:
                        print(f"- {topic}")

                print(
                    f"\nSentiment: {analysis_data.get('sentiment', 'No sentiment analysis available')}"
                )

            print("\nAnalysis completed and stored in database.")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
