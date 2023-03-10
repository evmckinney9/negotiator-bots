from negotiators import Negotiator, BasicBuyer, BasicSeller, ConversationData
import asyncio
import aiohttp

class Conversation():
    """Server running at localhost:8661
    Usage Example:
    # then try it with
    curl "http://localhost:8661/?q=hello"
    # >> {answer: "xxx", sameConversationUrlComponent: "&conversationId=123&parentMessageId=456"}
    # then try it with
    curl "http://localhost:8661/?q=hello&conversationId=123&parentMessageId=456"
    """
    def __init__(self, buyer: Negotiator, seller: Negotiator):
        self.buyer = buyer
        self.seller = seller
        self.initiated = False

    async def init_bots(self):
        # need to start 2 conversations, one for each negotiator
        assert not self.initiated, "Bots already initiated"
        # here, bot.conversationData is None, so will return constructor_prompt in place of lastResponse
        await self._bot_response(self.buyer)
        await self._bot_response(self.seller)
        self.initiated = True

    async def conversation_turn(self):
        """1 back and forth rotation between the 2 bots"""
        assert self.initiated, "Bots not initiated"

        # send buyer's message to the seller bot
        #pass responses by using the conversationData set last response
        self.seller.setLastResponse(self.buyer.getLastResponse())

        # get seller's response, and save new conversationData
        await self._bot_response(self.seller)
      
        # send seller's response to the buyer bot
        self.buyer.setLastResponse(self.seller.getLastResponse())

        # get buyer's response, and save new conversationData
        await self._bot_response(self.buyer)

    async def _bot_response(self, bot: Negotiator) -> None:
        data = await self._atomic_message(*bot.conversationData)
        # update the conversationData in the bot
        bot.setConversationData(data)

    async def _atomic_message(self, conversationId: str, parentMessageId: str, message: str) -> ConversationData:
        """Return a response to the user's message."""
        if conversationId is None and parentMessageId is None:
            payload = {"q": message}
        else:
            payload = {"q": message, "conversationId": conversationId, "parentMessageId": parentMessageId}
       
        # ret = requests.get("http://localhost:8661/", params=payload).json()
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8661/", params=payload) as resp:
                if resp.status == 200:
                    ret = await resp.json()
                else:
                    print(f"Request failed with status code {resp.status}")

        # clean response, jank formatting
        assert conversationId is None or ret['sameConversationUrlComponent'].split('&')[1].split('=')[1] == conversationId
        parentMessageId = ret['sameConversationUrlComponent'].split('&')[2].split('=')[1]

        ret = ConversationData(conversationId, parentMessageId, ret['answer'])
        print(ret)
        return ret 


async def main():
    buyer = BasicBuyer()
    seller = BasicSeller()
    conv = Conversation(buyer, seller)
    await conv.init_bots()
    await conv.conversation_turn()
    
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

# if __name__ == "__main__":
#     # Hello World to test the server
#     prompt = "What is the smallest animal in the world?"
#     payload = {"q": prompt}
#     ret = requests.get("http://localhost:8661/", params=payload).json()
#     print(ret,"\n")
#     text_response = ret['answer']

#     # for some reason need to do some text cleaning
#     ret_data = ret['sameConversationUrlComponent']
#     conversationid = ret_data.split('&')[1].split('=')[1]
#     parentmessageid = ret_data.split('&')[2].split('=')[1]

#     # follow up question
#     payload = {"q": "where does it live?", "conversationId": conversationid, "parentMessageId": parentmessageid}
#     ret = requests.get("http://localhost:8661/", params=payload).json()
#     print(ret)