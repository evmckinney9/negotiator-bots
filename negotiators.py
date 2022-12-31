"""Here we define an abstract negotiator class and a few concrete negotiators.
A negotiator is an gpt-3 agent with a) an objective, b) personality (i.e. aggressiveness)
and c) a strategy for negotiating. These attributes are defining by an input"""
from abc import ABC, abstractmethod

class Negotiator(ABC):
    """Abstract negotiator class"""
    def __init__(self, objective: str, personality: str, strategy: str):
        self.objective = objective #offense, defense
        self.personality = personality
        self.strategy = strategy

    @abstractmethod
    def constructor_prompt(self):
        """Used to initialize the negotiator and explaining to it the objective.
        Returns a prompt for the constructor"""
        pass

    @abstractmethod
    def respond(self, message: str):
        """Responds to a message"""
        pass


