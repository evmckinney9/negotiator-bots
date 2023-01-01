from negotiators import Negotiator, BasicAff, BasicNeg, ConversationData
import requests

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
        self.init_bots()

    async def init_bots(self):
        # need to start 2 conversations, one for each negotiator
        self.aff.setConversationData(self.bot_response(self.aff.constructor_prompt()))
        self.neg.setConversationData(self.bot_response(self.neg.constructor_prompt()))

    async def conversation_turn(self):
        """1 back and forth rotation between the 2 bots"""
        # send aff's message to the neg bot
        self.neg.setConversationData(self.bot_response(self.aff.getLastResponse(), self.neg.getLastResponse()))
    
    async def bot_response(self, conversationData: ConversationData):
        return self.atomic_message(conversationData.getLastResponse(), conversationData.conversationId, conversationData.parentMessageId)

    async def atomic_message(self, message: str, conversationId: str, parentMessageId: str):
        """Return a response to the user's message."""

        if conversationId is None and parentMessageId is None:
            payload = {"q": message}
        else:
            payload = {"q": message, "conversationId": conversationId, "parentMessageId": parentMessageId}
       
        ret = requests.get("http://localhost:8661/", params=payload).json()

        # clean response, jank formatting
        assert ret['conversationId'].split('&')[1].split('=')[1] == conversationId
        parentMessageId = ret['conversationId'].split('&')[2].split('=')[1]

        return ret['answer'], conversationId, parentMessageId


if __name__ == "__main__":
    aff = BasicAff()
    neg = BasicNeg()
    conv = Conversation(aff, neg)
    

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