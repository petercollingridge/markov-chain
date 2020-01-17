class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MarkovChainPropertyError(Error):
    """Exception raised for errors in a Markov chain's property."""

    def __init__(self, message):
        self.message = message
