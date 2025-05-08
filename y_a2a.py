# YFinance Agent for stock prices
from python_a2a import A2AServer, Message, TextContent, MessageRole
from python_a2a.mcp import FastMCPAgent

class YFinanceAgent(A2AServer, FastMCPAgent):
    """Agent that provides stock price information."""

    def __init__(self):
        A2AServer.__init__(self)
        FastMCPAgent.__init__(
            self,
            mcp_servers={"finance": "http://localhost:5002"}
        )

    async def handle_message_async(self, message):
        if message.content.type == "text":
            # Extract ticker from message
            import re
            ticker_match = re.search(r"\b([A-Z]{1,5})\b", message.content.text)
            if ticker_match:
                ticker = ticker_match.group(1)

                # Call MCP tool to get price
                price_info = await self.call_mcp_tool("finance", "get_stock_price", ticker=ticker)

                if "error" in price_info:
                    return Message(
                        content=TextContent(text=f"Error getting price for {ticker}: {price_info['error']}"),
                        role=MessageRole.AGENT,
                        parent_message_id=message.message_id,
                        conversation_id=message.conversation_id
                    )

                return Message(
                    content=TextContent(
                        text=f"{ticker} is currently trading at {price_info['price']:.2f} {price_info['currency']}."
                    ),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id
                )

        # Handle other message types or errors
        return Message(
            content=TextContent(text="I can provide stock price information for ticker symbols."),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )