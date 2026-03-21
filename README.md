# Cresta: Enterprise AI Agent System

This repository contains a full-stack, production-ready AI Agent Project developed as part of the application for the **Machine Learning Engineer (AI Agents)** role at [Cresta](https://www.cresta.com/).

## Project Overview

Cresta seeks engineers who can design, develop, and deploy AI Agent solutions, focusing on practical AI challenges like improving reasoning, planning capabilities, and evaluation in real-world scenarios. This project directly addresses those requirements through a **Customer Support AI Agent**.

### Key Features
1. **ReAct Reasoning Loop**: The AI agent utilizes a Reasoning and Acting (ReAct) paradigm to plan its approach to user queries step-by-step.
2. **Dynamic Tool Usage**:
   - **Knowledge Base RAG**: Retrieves policy and help center information dynamically.
   - **CRM Database Mock**: Checks order statuses and user profiles in real-time.
3. **Cost-Efficiency & Telemetry**: Built-in telemetry tracking token usage, estimated costs, and latency for every interaction, demonstrating a focus on production reliability and efficiency.
4. **Full-Stack Integration**: An asynchronous `FastAPI` backend paired with a modern, responsive HTML/JS frontend chat interface.
5. **Agent Evaluation Suite**: Includes an automated evaluation script to test the agent's reasoning pathways and tool selection against expected outcomes.
6. **Production Ready**: Containerized using Docker and `docker-compose`.

## Technology Stack
- **AI Core**: LangChain, OpenAI (or swap for open-source Hugging Face models)
- **Backend**: FastAPI, Uvicorn, Python 3.10
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Deployment**: Docker

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.10+ (if running locally without Docker)
- OpenAI API Key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Karl-Lin-sys/Machine-Learning-Engineer-AI-Agents.git
   cd Machine-Learning-Engineer-AI-Agents
   ```

2. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and append your OPENAI_API_KEY
   ```

3. Run the application via Docker:
   ```bash
   docker-compose up --build
   ```
   The API will be available at `http://localhost:8000`.

4. Open the Frontend:
   Simply open `src/frontend/index.html` in your web browser to interact with the agent.

## Evaluation

To evaluate the agent's reasoning and planning capabilities against ground-truth test cases, run:

```bash
# Ensure dependencies are installed first locally: pip install -r requirements.txt
python -m src.evaluate.evaluate_agent
```

This tests the agent on:
- Resolving CRM queries (Orders, Users)
- Searching the Knowledge Base
- Avoiding hallucinations

## Why this fits Cresta
- **Practical AI Application**: Focuses directly on contact center / customer support realities.
- **Production Emphasis**: Includes latency tracking, cost estimation, and Dockerization.
- **Evaluation First**: Demonstrates that measuring an AI's intermediate steps is just as important as the final answer.
