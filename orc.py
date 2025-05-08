from python_a2a import A2AClient, Message, TextContent, MessageRole, run_server
from ollama_server import OllamaA2AServer
import re
import requests

class StockAssistant(OllamaA2AServer):
    """An AI assistant for stock information that coordinates specialized agents."""

    def __init__(self, model="llama3", duckduckgo_endpoint="http://localhost:5003/a2a",
                 yfinance_endpoint="http://localhost:5004/a2a", ollama_host="http://localhost:11434"):
        # Initialize the Ollama-powered agent
        super().__init__(
            model=model,
            system_prompt=(
                "You are a helpful financial assistant that helps users get stock information. "
                "You extract company names from user queries to find ticker symbols and prices."
            ),
            ollama_host=ollama_host
        )

        # Create clients for connecting to specialized agents
        self.duckduckgo_client = A2AClient(duckduckgo_endpoint)
        self.yfinance_client = A2AClient(yfinance_endpoint)

    def handle_message(self, message):
        """Override to intercept stock-related queries."""
        if message.content.type == "text":
            text = message.content.text.lower()

            # Check if this is a stock price query
            if ("stock" in text or "price" in text or "trading" in text) and any(company in text for company in ["apple", "microsoft", "google", "amazon", "tesla", "facebook", "meta"]):
                # Process as a stock query
                return self._get_stock_info(message)

        # For all other messages, defer to Ollama
        return super().handle_message(message)

    def _get_stock_info(self, message):
        """Process a stock information query by coordinating with specialized agents."""
        try:
            # First, use Ollama to extract the company name
            ollama_response = super().handle_message(Message(
                content=TextContent(
                    text=f"Extract only the company name from this query: '{message.content.text}'. "
                         f"Return ONLY the company name, nothing else."
                ),
                role=MessageRole.USER,
                conversation_id=f"{message.conversation_id}_extract"  # Use a separate conversation for extraction
            ))

            company_name = ollama_response.content.text.strip()
            company_name = company_name.strip('"\'.,')

            # Simple fallback for common companies if extraction fails
            if len(company_name) > 20 or not company_name:
                # Try to extract using simple pattern matching
                text = message.content.text.lower()
                for company in ["apple", "microsoft", "google", "amazon", "tesla", "facebook", "meta"]:
                    if company in text:
                        company_name = company
                        break

            # Step 1: Get the ticker symbol from DuckDuckGo agent
            ticker_message = Message(
                content=TextContent(text=f"What's the ticker for {company_name}?"),
                role=MessageRole.USER
            )
            ticker_response = self.duckduckgo_client.send_message(ticker_message)

            # Extract ticker from response
            ticker_match = re.search(r'ticker\s+(?:symbol\s+)?(?:for\s+[\w\s]+\s+)?is\s+([A-Z]{1,5})',
                                   ticker_response.content.text, re.I)
            if not ticker_match:
                return Message(
                    content=TextContent(text=f"I couldn't find the ticker symbol for {company_name}."),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id
                )

            ticker = ticker_match.group(1)

            # Step 2: Get the stock price from YFinance agent
            price_message = Message(
                content=TextContent(text=f"What's the current price of {ticker}?"),
                role=MessageRole.USER
            )
            price_response = self.yfinance_client.send_message(price_message)

            # Return the combined information
            return Message(
                content=TextContent(
                    text=f"{company_name} ({ticker}): {price_response.content.text}"
                ),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

        except Exception as e:
            # Handle any errors
            return Message(
                content=TextContent(text=f"Sorry, I encountered an error: {str(e)}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )
# Run the assistant
if __name__ == "__main__":
    # Check if Ollama is running at the local address
    try:
        import requests
        response = requests.get("http://localhost:11434/api/version")
        if response.status_code == 200:
            print("Connected to Ollama server at http://localhost:11434")
    except:
        print("Error: Cannot connect to Ollama server at http://localhost:11434")
        print("Please check if the server is running and accessible.")
        exit(1)

    # Create the assistant with default parameters
    assistant = StockAssistant(
        model="llama3.3",  # You can change this to any model available in your Ollama
        duckduckgo_endpoint="http://localhost:5003/a2a",
        yfinance_endpoint="http://localhost:5004/a2a"
    )

    run_server(assistant, port=5000)
