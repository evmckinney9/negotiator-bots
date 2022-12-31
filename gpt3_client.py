import openai
import json
from negotiators import Negotiator

class NegotiationDeal():
    def __init__(self, aff: Negotiator, neg: Negotiator, prompt: str:
       raise NotImplementedError
        

class Message():
    """Server must be running on """
    async def bot_response(self):
        """Create and respond to the prompt with a message to the channel"""
        async with self.context.typing():
            prompt = self.prompt_cleaner(self.prompt)
            print(prompt)
            ret = self.chatgpt3(prompt)
            response_text = self.response_cleaner(ret)
            await self.context.send(response_text)

    def prompt_cleaner(self, prompt: str) -> str:
        #personality
        prompt += f"Write the text message response using personality of: {self.personality}\n"

        # small chance they knows their own name
        if random.random() > 0.1:
            prompt = prompt.replace(f"named {self.name} ", "")
        
        # only chance to mention current location
        if random.random() > 0.15:
            # prompt = prompt.replace(f"at a {self.personality.location} ", "")
            # use regular expression to remove location, multi-word until next new line
            prompt = re.sub(r"at a [a-zA-Z ]+\n", ".\n", prompt)
        
        if self.author is not None:
            prompt += f"Remember that {self.author.display_name} wrote this message and mention them.\n"
        if self.reactor is not None and self.reactor != self.author:
            prompt += f"Remember that {self.reactor.display_name} reacted to the message and mention them.\n"

        # parsed for tagged user in the original message part of the prompt
        if self.mentions is not None:
            for user in self.mentions:
                prompt = prompt.replace(f"<@{user.id}>", user.display_name)
        
        return prompt

    def response_cleaner(self, message: str) -> str:
        """Cleans the response from GPT-3"""
        # remove newline chars
        message = message.replace("\n", "")
        message = message.replace("  ", " ")

        # don't start or end with qoutes
        if message[0] == '"':
            message = message[1:]
        if message[-1] == '"':
            message = message[:-1]

        #sub tags in response if author or reactors kwargs
        # clean response_text, want to replace names with discord mentions
        # remove @
        message = message.replace("@", "")
        if self.author is not None:
            # response_text = response_text.replace(author.display_name, author.mention)
            # replace all instances, case insensitive
            message = re.sub(self.author.display_name, self.author.mention, message, flags=re.IGNORECASE)
        if self.reactor is not None:
            # response_text = response_text.replace(reactor.display_name, reactor.mention)
            message = re.sub(self.reactor.display_name, self.reactor.mention, message, flags=re.IGNORECASE)

        return message

    def chatgpt3(self, prompt: str) -> str:
        """Returns a response from GPT-3"""

        # get api key from config.json
        with open("config.json") as file:
            data = json.load(file)
            openai.api_key = data["openai_api_key"]

        # make a prompt
        kwargs= {
            "model": "text-davinci-003",
            "prompt": prompt,
            "max_tokens": 140,
            "temperature": 1,
            "top_p": 1,
            "n": 1,
            "stream": False,
            "logprobs": None,
            "presence_penalty": .5,
            "frequency_penalty": .5,
        }

        # generate a response
        print("Generating response...")
        response = openai.Completion.create(**kwargs)
        print(response)
        ret = response["choices"][0]["text"]
        return ret