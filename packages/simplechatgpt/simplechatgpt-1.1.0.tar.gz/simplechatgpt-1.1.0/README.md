# Simple ChatGPT

An extremely simple programmatic interface to ChatGPT. The conversation
automatically gets truncated (from the oldest message) if the token limit is
reached.

The goal of this project is to remove the need for boilerplate code to create
a chat bot in your program, allowing you to jump right into integrating
ChatGPT into whatever you are making.

You can use this package like:

```
from simplechatgpt import Chat

import os

chat = Chat(os.environ["OPENAI_API_KEY"])

while True:
    prompt = input("You: ")
    print("Bot:", chat.send(prompt))
```

You can choose a model when initializing your `Chat` object like:

```
chat = Chat(os.environ["OPENAI_API_KEY"], model="gpt-4")
```

As of the time of this writing (07/08/2023), the following models are available
for use:

  - `gpt-4`
  - `gpt-4-32k`
  - `gpt-3.5-turbo`
  - `gpt-3.5-turbo-16k`

See https://platform.openai.com/docs/models/overview for a full list of
available models.

You can also customize the "system" message to initialize the chat bot to
act in a certain way throughout the conversation. For example,

```
key = os.environ["OPENAI_API_KEY"]
chat = Chat(key, chatbot_description="You are Hucklyberry Finn.")

while True:
    prompt = input("You: ")
    print("Bot:", chat.send(prompt))
```

Would produce responses like:

```
You: Hey son, how are you?
Bot: Well, I reckon I'm doin' alright Pa. How 'bout yourself?
```
