from negotiators import Negotiator, BasicAff, BasicNeg, ConversationData
import requests
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
    def __init__(self, aff: Negotiator, neg: Negotiator):
        self.aff = aff
        self.neg = neg
        self.initiated = False

    async def init_bots(self):
        # need to start 2 conversations, one for each negotiator
        data = await self._construction_response(self.aff.constructor_prompt())
        print(data)
        self.aff.setConversationData(data)
        data = await self._construction_response(self.neg.constructor_prompt())
        print(data)
        self.neg.setConversationData(data)  
        self.initiated = True

    async def conversation_turn(self):
        """1 back and forth rotation between the 2 bots"""
        assert self.initiated, "Bots not initiated"

        # send aff's message to the neg bot
        #pass responses by using the conversationData set last response
        self.neg.setLastResponse(self.aff.getLastResponse())

        # get neg's response, and save new conversationData
        data = await self._bot_response(self.neg.conversationData)
        print(data)
        self.neg.setConversationData(data)

        # send neg's response to the aff bot
        self.aff.setLastResponse(data.getLastResponse())

        # get aff's response, and save new conversationData
        data = await self._bot_response(self.aff.conversationData)
        print(data)
        self.aff.setConversationData(data)

    async def _construction_response(self, message: str) -> ConversationData:
        """Conversation construction, need this function before ConversationData has been initialized"""
        return self._atomic_message(message, None, None)

    async def _bot_response(self, conversationData: ConversationData) -> ConversationData:
        return self._atomic_message(conversationData.getLastResponse(), conversationData.getConversationId(), conversationData.getParentMessageId())

    async def _atomic_message(self, message: str, conversationId: str, parentMessageId: str) -> ConversationData:
        """Return a response to the user's message."""

        if conversationId is None and parentMessageId is None:
            payload = {"q": message}
        else:
            payload = {"q": message, "conversationId": conversationId, "parentMessageId": parentMessageId}
       
        # ret = requests.get("http://localhost:8661/", params=payload).json()
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8661/", params=payload) as resp:
                ret = await resp.json()

        # clean response, jank formatting
        assert ret['conversationId'].split('&')[1].split('=')[1] == conversationId
        parentMessageId = ret['conversationId'].split('&')[2].split('=')[1]

        return ConversationData(ret['answer'], conversationId, parentMessageId)


async def main():
    aff = BasicAff()
    neg = BasicNeg()
    conv = Conversation(aff, neg)
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