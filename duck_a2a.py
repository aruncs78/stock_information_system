# DuckDuckGo Agent for ticker lookup
from python_a2a import A2AServer, Message, TextContent, MessageRole
from python_a2a.mcp import FastMCPAgent

class DuckDuckGoAgent(A2AServer, FastMCPAgent):
    """Agent that finds stock ticker symbols."""

    def __init__(self):
        A2AServer.__init__(self)
        FastMCPAgent.__init__(
            self,
            mcp_servers={"search": "http://localhost:5001"}
        )

    async def handle_message_async(self, message):
        if message.content.type == "text":
            # Extract company name from message
            import re
            company_match = re.search(r"ticker\s+(?:for|of)\s+([A-Za-z\s]+)", message.content.text, re.I)
            if company_match:
                company_name = company_match.group(1).strip()
            else:
                # Default to using the whole message
                company_name = message.content.text.strip()

            # Call MCP tool to lookup ticker
            ticker = await self.call_mcp_tool("search", "search_ticker", company_name=company_name)

            return Message(
                content=TextContent(text=f"The ticker symbol for {company_name} is {ticker}."),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

        # Handle other message types or errors
        return Message(
            content=TextContent(text="I can help find ticker symbols for companies."),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )