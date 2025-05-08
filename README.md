# Stock Information System

A multi-agent system for retrieving stock information using the A2A (Agent-to-Agent) framework with Ollama for local LLM capabilities.

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

## Setup

1. Ollama Server:
   - This project is configured to use a remote Ollama server at http://20.150.213.196:11434
   - No local Ollama installation is required
   - The server should have the llama3 model (or other models) available

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the system:
   ```
   python main.py
   ```

4. In a separate terminal, run the client:
   ```
   python a2aclient.py
   ```

## Usage

Once the system is running, you can ask questions like:
- "What's the stock price of Apple?"
- "How much is Microsoft trading for?"
- "Get the current price of Tesla stock"

## Components

- **mcpserver.py**: Implements the MCP servers
- **duck_a2a.py**: DuckDuckGo agent for ticker lookup
- **y_a2a.py**: YFinance agent for stock prices
- **ollama_server.py**: Custom A2A server implementation using Ollama
- **orc.py**: Orchestrator that coordinates the agents
- **a2aclient.py**: Command-line client for interacting with the system
- **main.py**: Script to run all components

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
3. **Customizable**: Can use any model supported by Ollama (llama3, mistral, etc.)
4. **Flexible Deployment**: Can use either a local or remote Ollama server
5. **Easy Configuration**: Simply change the ollama_host parameter to switch between servers
