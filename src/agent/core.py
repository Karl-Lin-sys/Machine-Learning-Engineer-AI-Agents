import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from src.agent.tools import AgentTools

class CrestaAIAgent:
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.0):
        """
        Initializes the ReAct AI Agent with standard tools and reasoning capabilities.
        Connects it to an LLM provider (OpenAI by default, easily swappable).
        """
        # Ensure API key is set or provide a robust default exception message
        if not os.getenv("OPENAI_API_KEY") and not os.getenv("MOCK_LLM_MODE"):
            print("WARNING: OPENAI_API_KEY not found in environment.")

        # Initialize LLM
        # For a full production system, we'd wrap this with fallback logic (e.g., fallback to Azure or Anthropic)
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        
        self.tools = AgentTools.get_all_tools()
        
        # System instructions to enforce reasoning and planning capabilities
        self.system_prompt = """You are a highly capable AI Support Agent for Cresta.
Your role is to assist human agents or directly resolve customer issues efficiently.
You have access to specific tools to retrieve internal knowledge and query CRM databases.

Follow these strict guidelines:
1. REASONING: Before answering, think step-by-step about what information you need.
2. TOOL USE: If a user asks about an order, ALWAYS use the `check_order_status` tool. 
   If they ask a policy question, use the `search_knowledge_base` tool.
3. EMPATHY: Always maintain a professional and empathetic tone.
4. HONESTY: If you cannot find the answer using your tools, do not hallucinate. Admit you don't know and offer to connect them to a human agent.

Do your best to resolve the inquiry completely.
"""
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Construct the OpenAI Tools agent
        self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        
        # Create an agent executor by passing in the agent and tools
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True,
            return_intermediate_steps=True # Crucial for "evaluating reasoning steps" later
        )
        
        # Store chat history locally for the session
        self.chat_history = []

    def get_response(self, user_input: str) -> Dict[str, Any]:
        """
        Processes a user request and returns the response and intermediate reasoning steps.
        """
        response = self.agent_executor.invoke({
            "input": user_input,
            "chat_history": self.chat_history
        })
        
        # Update history
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response["output"]))
        
        # We return the intermediate steps for traceability and evaluation
        return {
            "answer": response["output"],
            "intermediate_steps": [(action.log, observation) for action, observation in response.get("intermediate_steps", [])]
        }
