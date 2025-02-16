
import logging
logger = logging.getLogger("monkey")

class Analysis:
    def __init__(self):
        self.data = {}
    
    def to_dict(self) -> dict:
        return self.data
    