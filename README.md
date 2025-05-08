# Stock Information System

A multi-agent system for retrieving stock information using the A2A (Agent-to-Agent) framework with Ollama for local LLM capabilities.

## Installation Guide

### Prerequisites
- Python 3.8 or higher
- Ollama (for local LLM capabilities)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/stock-information-system.git
cd stock-information-system
```

### Step 2: Install Ollama
1. Visit [https://ollama.com/download](https://ollama.com/download) and follow the instructions for your operating system.
2. After installation, pull the required model:
```bash
ollama pull llama3.3
```
3. Verify Ollama is running:
```bash
ollama list
```

### Step 3: Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```

Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the System

### Step 1: Start the Main System
In your terminal, run:
```bash
python main.py
```
This will start:
- DuckDuckGo MCP Server (port 5001)
- YFinance MCP Server (port 5002)
- DuckDuckGo A2A Agent (port 5003)
- YFinance A2A Agent (port 5004)
- Stock Assistant Orchestrator (port 5000)

You should see output confirming each component has started successfully.

### Step 2: Start the Client
In a separate terminal (with the virtual environment activated), run:
```bash
python a2aclient.py
```

This will start an interactive session where you can ask questions about stock prices.

### Step 3: Ask Questions
Example queries:
- "What's the stock price of Apple?"
- "How much is Microsoft trading for?"
- "Get the current price of Tesla stock"

## Architecture

This system demonstrates the Agent-to-Agent architecture with:

1. **MCP Servers (Machine Capability Providers)**
   - DuckDuckGo MCP: Provides search capabilities to find stock ticker symbols
   - YFinance MCP: Provides stock price data using the yfinance library

2. **A2A Agents**
   - DuckDuckGoAgent: Specialized agent for finding ticker symbols
   - YFinanceAgent: Specialized agent for retrieving stock prices

3. **Orchestrator**
   - StockAssistant: Coordinates between specialized agents using Ollama (local LLM)

## Components

- **mcpserver.py**: Implements the MCP servers
  - DuckDuckGo MCP (port 5001): Provides ticker symbol lookup
  - YFinance MCP (port 5002): Provides stock price data

- **duck_a2a.py**: DuckDuckGo agent for ticker lookup
  - Runs on port 5003
  - Communicates with DuckDuckGo MCP

- **y_a2a.py**: YFinance agent for stock prices
  - Runs on port 5004
  - Communicates with YFinance MCP

- **ollama_server.py**: Custom A2A server implementation using Ollama
  - Provides LLM capabilities without requiring OpenAI API keys
  - Supports both local and remote Ollama servers

- **orc.py**: Orchestrator that coordinates the agents
  - Runs on port 5000
  - Uses Ollama for natural language understanding
  - Coordinates between specialized agents

- **a2aclient.py**: Command-line client for interacting with the system
  - Connects to the orchestrator on port 5000
  - Provides an interactive interface for stock queries

- **main.py**: Script to run all components
  - Starts MCP servers, A2A agents, and the orchestrator
  - Configures the system components

## Flow

1. User enters a query in the client
2. Query is sent to the StockAssistant orchestrator
3. Orchestrator extracts the company name using Ollama
4. Orchestrator asks DuckDuckGo agent for the ticker symbol
5. Orchestrator asks YFinance agent for the current price
6. Combined information is returned to the user

## Benefits of Using Ollama

1. **No API Key Required**: No need for OpenAI API keys or accounts
2. **Cost-Free**: No usage charges or rate limits
3. **Customizable**: Can use any model supported by Ollama (llama3.3, mistral, etc.)
4. **Flexible Deployment**: Can use either a local or remote Ollama server
5. **Easy Configuration**: Simply change the ollama_host parameter to switch between servers

## Troubleshooting

- **404 Not Found Error**: Ensure Ollama is running and the model is pulled
  ```
  ollama pull llama3.3
  ```

- **Connection Issues**: Check that all ports (5000-5004) are available and not blocked by firewall

- **Model Not Found**: Verify you have the correct model name in main.py
  - Available models can be checked with `ollama list`

- **Port Already in Use**: If you get an error that a port is already in use, you can either:
  - Close the application using that port
  - Modify the port numbers in main.py

## Port Configuration

- 5000: StockAssistant (Orchestrator)
- 5001: DuckDuckGo MCP Server
- 5002: YFinance MCP Server
- 5003: DuckDuckGo A2A Agent
- 5004: YFinance A2A Agent


