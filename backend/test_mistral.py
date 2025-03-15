#!/usr/bin/env python3
"""
Simple test script for Mistral API
"""

import os

from dotenv import load_dotenv

# Load API key from environment
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    print("Error: MISTRAL_API_KEY not found in environment")
    exit(1)

print("Testing Mistral AI client version 0.0.7")

# Try to import and use the mistralai client
try:
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage

    print("Successfully imported MistralClient and ChatMessage")

    # Create client
    client = MistralClient(api_key=MISTRAL_API_KEY)

    # Test a simple chat completion with ChatMessage
    print("\nTesting chat completion with ChatMessage:")
    response = client.chat(
        model="mistral-tiny",
        messages=[ChatMessage(role="user", content="Hello, how are you?")],
        max_tokens=10,
    )

    print(f"Response: {response.choices[0].message.content}")
    print("Success using ChatMessage format")

    # Print the structure of the response
    print("\nResponse structure:")
    print(f"response.choices[0].message.content: {response.choices[0].message.content}")
    print(f"response.usage: {response.usage}")

except ImportError as e:
    print(f"Import error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

print("\nTest complete")
