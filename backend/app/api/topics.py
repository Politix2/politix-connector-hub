
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import re

router = APIRouter()

class DomainRequest(BaseModel):
    domain: str

class TopicResponse(BaseModel):
    topics: List[str]

# Mock implementation of domain-to-topic mapping
TOPIC_MAPPING = {
    "energy": ["Energy Taxation", "Solar Subsidies", "Carbon Pricing", "Grid Infrastructure", "Renewable Targets"],
    "tech": ["Digital Infrastructure", "Data Privacy", "Platform Regulation", "AI Governance", "Cybersecurity"],
    "healthcare": ["Drug Pricing", "Healthcare Access", "Medical Data", "Insurance Reform", "Telehealth"],
    "finance": ["Banking Regulation", "Investment Rules", "Consumer Protection", "Digital Currencies", "Tax Policy"],
    "automotive": ["Emissions Standards", "EV Incentives", "Autonomous Driving", "Supply Chain", "Safety Regulations"],
    "retail": ["Consumer Protection", "E-commerce Rules", "Labor Standards", "Import/Export", "Tax Compliance"],
}

@router.post("/suggest", response_model=TopicResponse)
async def suggest_topics(request: DomainRequest):
    """Suggest regulatory topics based on the user's domain/industry."""
    # Convert domain to lowercase for case-insensitive matching
    domain_lower = request.domain.lower()
    
    # Find the best match in our mapping
    matched_topics = []
    
    for key, topics in TOPIC_MAPPING.items():
        if re.search(r'\b' + re.escape(key) + r'\b', domain_lower):
            matched_topics = topics
            break
    
    # If no match, return a default set of topics
    if not matched_topics:
        matched_topics = ["Energy Taxation", "Digital Infrastructure", "Market Competition", 
                          "Data Privacy", "Import/Export"]
    
    return TopicResponse(topics=matched_topics)
