"""
Main script to run the Stock Information System
This script starts all the necessary components:
1. MCP Servers (DuckDuckGo and YFinance)
2. A2A Agents (DuckDuckGo and YFinance)
3. Orchestrator (Stock Assistant)
"""

import threading
import time
from python_a2a import run_server
from mcpserver import run_duckduckgo_server, run_yfinance_server
from duck_a2a import DuckDuckGoAgent
from y_a2a import YFinanceAgent
from orc import StockAssistant

def run_duck_agent():
    """Run the DuckDuckGo agent on port 5003"""
    duck_agent = DuckDuckGoAgent()
    run_server(duck_agent, port=5003)

def run_yfinance_agent():
    """Run the YFinance agent on port 5004"""
    yf_agent = YFinanceAgent()
    run_server(yf_agent, port=5004)

def run_stock_assistant():
    """Run the main Stock Assistant on port 5000"""
    # Ollama check is done in the StockAssistant class

    # Create the assistant with remote Ollama server
    assistant = StockAssistant(
        model="llama3",  # Changed from llama2 to llama3.3
        duckduckgo_endpoint="http://localhost:5003/a2a",
        yfinance_endpoint="http://localhost:5004/a2a",
        ollama_host="http://20.150.213.196:11434"  # Remote Ollama server
    )

    run_server(assistant, port=5000)

if __name__ == "__main__":
    # Start MCP servers (already started in mcpserver.py import)
    print("Starting MCP servers...")

    # Start A2A agents
    print("Starting A2A agents...")
    duck_thread = threading.Thread(target=run_duck_agent, daemon=True)
    yf_thread = threading.Thread(target=run_yfinance_agent, daemon=True)

    duck_thread.start()
    yf_thread.start()

    # Give agents time to start
    time.sleep(2)

    # Start main assistant
    print("Starting Stock Assistant...")
    run_stock_assistant()






