"""
An extremely simple programmatic interface to ChatGPT to expedite integrating
ChatGPT into other projects. The conversation automatically gets truncated
(from the oldest message) if the token limit is reached.
"""

import openai
from openai import OpenAI

client = OpenAI(api_key=token)

DEFAULT_CHATBOT_DESCRIPTION = "You are a helpful assistant."


class Chat:
    def __init__(
        self,
        token: str,
        model: str = "gpt-3.5-turbo",
        chatbot_description: str = DEFAULT_CHATBOT_DESCRIPTION,
    ):
        """
        Initialize a ChatGPT chatbot.

        Args:
            token (str): OpenAI API token.
            model (str): The model to use.
            chatbot_description (str): The description of the chatbot to
                customize the chatbot's responses.
        """

        self.model = model
        self.chatbot_description = chatbot_description
        self.reset(chatbot_description)

    def send(self, prompt: str) -> str:
        """
        Ask a question to the chatbot.

        Args:
            prompt (str): The prompt to ask the chatbot.

        Returns:
            str: The chatbot's response.
        """
        try:
            self.messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(
                model=self.model, messages=self.messages
            )
            message = response.choices[0].message
            self.messages.append(message)
            return message.content
        except openai.InvalidRequestError:
            self.messages.pop(0)
            return self.send(prompt)

    def reset(self, chatbot_description: str = DEFAULT_CHATBOT_DESCRIPTION):
        """
        Reset the conversation.

        Args:
            chatbot_description (str): The description of the chatbot to
                customize the chatbot's responses.
        """
        self.messages = [{"role": "system", "content": chatbot_description}]
