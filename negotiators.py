"""Here we define an abstract negotiator class and a few concrete negotiators.
A negotiator is an gpt-3 agent with a) an objective, b) personality (i.e. aggressiveness)
and c) a strategy for negotiating. These attributes are defining by an input"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ConversationData():
    """Dataclass for storing conversation data"""
    conversationId: str
    parentMessageId: str
    lastResponse: str
    def __iter__(self):
        return iter([self.conversationId, self.parentMessageId, self.lastResponse])
    
    def __str__(self):
        return f"Response: {self.lastResponse}\n"

class Negotiator(ABC):
    def __init__(self):
        self.conversationData = ConversationData(None, None, self.constructor_prompt())
    
    #NOTE These might be all deprecatable
    """Abstract negotiator class"""
    def setConversationData(self, conversationData: ConversationData):
        self.conversationData = conversationData
    
    def setLastResponse(self, lastResponse: str):
        self.conversationData.lastResponse = lastResponse
    
    def getLastResponse(self):
        if self.conversationData is None:
            return self.constructor_prompt()
        return self.conversationData.lastResponse
    
    @abstractmethod
    def constructor_prompt(self):
        """Used to initialize the negotiator and explaining to it it's objective.
        If is an buyer bot, the first message should start presenting their offer.
        If is a seller bot, the first message should acknowledge waiting for the buyer bot to make an offer."""
        setup_prompt = "You are a negotiator. Your objective is to {}. You are {}. You are using the {} strategy. " 
        return setup_prompt.format(self.objective, self.personality, self.strategy)

class BasicBuyer(Negotiator):
    """Basic buyer negotiator"""
    def __init__(self):
        self.objective = "negotiate the price of berrires you are purchasing"
        self.personality = "aggressive"
        self.strategy = "bargaining"
        super().__init__()

    def constructor_prompt(self):
        prompt = super().constructor_prompt()
        prompt += "As the buying bot, begin by presenting your offer which will be given to the seller bot."
        return prompt

class BasicSeller(Negotiator):
    """Basic seller negotiator"""
    def __init__(self):
        self.objective = "negotiate the price of berries you are selling"
        self.personality = "timid"
        self.strategy = "flattery"
        super().__init__()

    def constructor_prompt(self):
        prompt = super().constructor_prompt()
        prompt += "As the selling bot, begin by waiting to recieve the first offer."
        return prompt