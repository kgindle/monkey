
import importlib
from .Analysis import Analysis

class Analyzer:
    """
    A base class for content analyzers. Content analyzers are used to analyze
    data at a given path and return an Analysis object.
    """
    def __init__(self):
        pass

    def get_analyzer_name(self) -> str:
        """
        Returns the name of this analyzer. This is used to identify the
        analyzer.
        
        By default this is the class name with "Analyzer" removed and converted
        to lowercase.
        """
        name = self.__class__.__name__
        return name.replace("Analyzer", "").lower()
    
    def supports(self, path: str) -> bool:
        """
        Checks if this analyzer supports analyzing data at the given path.
        Args:
            path (str): The file path to check for support.
        Returns:
            bool: True if this analyzer can analyze the data at the given path, False otherwise.
        """
        raise NotImplementedError("supports() must be implemented by a subclass")

    def analyze(self, path: str) -> Analysis|None:
        """
        Analyzes the data at the given path and returns an Analysis object.
        """
        raise NotImplementedError("analyze() must be implemented by a subclass")
