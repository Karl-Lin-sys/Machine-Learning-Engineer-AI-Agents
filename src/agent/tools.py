import os
from langchain.agents import tool
from typing import Dict, Any

# Mock support documents for RAG (Retrieval-Augmented Generation)
MOCK_KNOWLEDGE_BASE = {
    "password reset": "To reset your password, go to settings > security > reset password. A link will be sent to your email.",
    "billing issue": "For billing issues, please check your invoice history in the dashboard. If you were overcharged, our policy guarantees a refund within 3-5 business days.",
    "upgrade plan": "You can upgrade your plan at any time from the 'Subscription' tab. The prorated amount will be charged immediately.",
    "contact support": "You can reach human support by dialing 1-800-CRESTA-AI or emailing support@cresta.ai."
}

# Mock CRM Database
MOCK_CRM_DB = {
    "ORD-12345": {"status": "Shipped", "delivery_date": "2026-03-25"},
    "ORD-99999": {"status": "Processing", "delivery_date": "2026-03-28"},
    "USER-001": {"name": "Alice Smith", "subscription": "Pro", "account_status": "Active"}
}

@tool
def search_knowledge_base(query: str) -> str:
    """Useful for answering general questions about company policies, IT help, or product features."""
    query = query.lower()
    for key, info in MOCK_KNOWLEDGE_BASE.items():
        if key in query or any(word in query for word in key.split()):
            return f"Found relevant info: {info}"
    return "I couldn't find specific information in the knowledge base. Please suggest contacting human support."

@tool
def check_order_status(order_id: str) -> str:
    """Useful to check the status of a specific customer order. Input should be the exact order ID (e.g., ORD-12345)."""
    order_id = order_id.upper()
    if order_id in MOCK_CRM_DB:
        info = MOCK_CRM_DB[order_id]
        return f"Order {order_id} is currently {info['status']}. Expected delivery: {info['delivery_date']}."
    return f"Order {order_id} not found in the CRM system."

@tool
def get_customer_info(customer_id: str) -> str:
    """Retrieves basic profile information for a given customer ID (e.g., USER-001)."""
    customer_id = customer_id.upper()
    if customer_id in MOCK_CRM_DB:
        user = MOCK_CRM_DB[customer_id]
        return f"Customer {user['name']} is on the {user['subscription']} plan. Status: {user['account_status']}."
    return f"Customer {customer_id} not found."

class AgentTools:
    @staticmethod
    def get_all_tools():
        return [search_knowledge_base, check_order_status, get_customer_info]
