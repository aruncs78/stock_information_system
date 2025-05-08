"""
Custom A2A Server implementation using Ollama
"""

import ollama
import os
from python_a2a import A2AServer, Message, TextContent, MessageRole

class OllamaA2AServer(A2AServer):
    """
    A2A Server implementation that uses Ollama for LLM capabilities.
    This replaces the OpenAIA2AServer with a local Ollama-based alternative.
    """

    def __init__(self, model="llama3", system_prompt=None, ollama_host=None):
        """
        Initialize the Ollama A2A Server.

        Args:
            model (str): The Ollama model to use (default: "llama3")
            system_prompt (str): Optional system prompt to set context
            ollama_host (str): Optional Ollama host URL (default: None, uses OLLAMA_HOST env var or localhost)
        """
        super().__init__()
        self.model = model
        self.system_prompt = system_prompt
        self.conversation_history = {}

        # Set Ollama host if provided
        if ollama_host:
            os.environ["OLLAMA_HOST"] = ollama_host
            print(f"Using Ollama server at: {ollama_host}")

    def handle_message(self, message):
        """
        Process an incoming message using Ollama.

        Args:
            message: The A2A message to process

        Returns:
            Message: The response message
        """
        if message.content.type != "text":
            return Message(
                content=TextContent(text="I can only process text messages."),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

        # Get or create conversation history
        conv_id = message.conversation_id
        if conv_id not in self.conversation_history:
            self.conversation_history[conv_id] = []

            # Add system prompt if provided
            if self.system_prompt:
                self.conversation_history[conv_id].append({
                    "role": "system",
                    "content": self.system_prompt
                })

        # Add user message to history
        self.conversation_history[conv_id].append({
            "role": "user",
            "content": message.content.text
        })

        # Prepare messages for Ollama
        messages = self.conversation_history[conv_id]

        try:
            # Call Ollama API
            response = ollama.chat(
                model=self.model,
                messages=messages
            )

            # Extract the response text
            response_text = response['message']['content']

            # Add assistant response to history
            self.conversation_history[conv_id].append({
                "role": "assistant",
                "content": response_text
            })

            # Create and return A2A message
            return Message(
                content=TextContent(text=response_text),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=conv_id
            )

        except Exception as e:
            return Message(
                content=TextContent(text=f"Error processing with Ollama: {str(e)}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=conv_id
            )
