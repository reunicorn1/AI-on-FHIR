from typing import Dict, Any

class FHIRBasePrompt:
    def __init__(self, request_type: str):
        # Each class can have its own NER model or rules
        self.request_type = request_type

    def process(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Further process entity to build final FHIR API payload"""
        raise NotImplementedError("Must implement process in subclass")