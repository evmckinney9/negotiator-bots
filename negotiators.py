"""Here we define an abstract negotiator class and a few concrete negotiators.
A negotiator is an gpt-3 agent with a) an objective, b) personality (i.e. aggressiveness)
and c) a strategy for negotiating. These attributes are defining by an input"""
from abc import ABC, abstractmethod

class ConversationData():
    """Data for a conversation"""
    def __init__(self, message: str, conversationId: str, parentMessageId: str):
        self.lastResponse = message
        self.conversationId = conversationId
        self.parentMessageId = parentMessageId

    def setLastResponse(self, lastResponse: str):
        self.lastResponse = lastResponse
    
    def getLastResponse(self):
        return self.lastResponse
    
    def getConversationId(self):
        return self.conversationId
    
    def getParentMessageId(self):
        return self.parentMessageId

class Negotiator(ABC):
    def __init__(self):
        self.conversationData = None
        self.objective = None
        self.personality = None
        self.strategy = None

    """Abstract negotiator class"""
    def setConversationData(self, conversationData: ConversationData):
        self.conversationData = conversationData
    
    def setLastResponse(self, lastResponse: str):
        self.conversationData.setLastResponse(lastResponse)
    
    def getLastResponse(self):
        return self.conversationData.getLastResponse()
    
    @abstractmethod
    def constructor_prompt(self):
        """Used to initialize the negotiator and explaining to it it's objective.
        If is an aff bot, the first message should start presenting their offer.
        If is a neg bot, the first message should acknowledge waiting for the aff bot to make an offer."""
        setup_prompt = "You are a negotiator. Your objective is to {}. You are {}. You are using the {} strategy. " 
        return setup_prompt.format(self.objective, self.personality, self.strategy)

class BasicAff(Negotiator):
    """Basic aff negotiator"""
    def __init__(self):
        super().__init__()
        self.objective = "negotiate the price of berrires you are purchasing"
        self.personality = "aggressive"
        self.strategy = "bargaining"

    def constructor_prompt(self):
        prompt = super().constructor_prompt()
        prompt += "As the aff bot, begin by presenting your offer."
        return prompt

class BasicNeg(Negotiator):
    """Basic neg negotiator"""
    def __init__(self):
        super().__init__()
        self.objective = "negotiate the price of berries you are selling"
        self.personality = "timid"
        self.strategy = "flattery"

    def constructor_prompt(self):
        prompt = super().constructor_prompt()
        prompt += "As the neg bot, begin by waiting to recieve the first offer."
        return prompt