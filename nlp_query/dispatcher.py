from transformers import pipeline
from transformers import pipeline
import spacy
import pandas as pd
from nlp_query.base_prompt import FHIRBasePrompt
from nlp_query.patient_prompt import PatientPrompt
from nlp_query.condition_prompt import ConditionPrompt
from nlp_query.patterns.patients_patterns import PATIENT_PATTERNS

"""Dispatcher to classify prompts and route to appropriate FHIR resource handlers"""
class Dispatcher:
    """Main dispatcher class to classify and route prompts"""
    CONF_THRESHOLD = 0.5
    def __init__(self):
        """Initialize the dispatcher with resource templates and classifiers"""
        self.resource_templates = {"medical conditions": PatientPrompt, # Currently we're expecting only specific format. since I'm using reverse condition, I'll modify this for now to patient prompt
                                   "patients information": PatientPrompt, 
                                   "others": FHIRBasePrompt}
        self.requests = {
            "search for existing patients": "search",
            "find existing records": "search",
            "create new patient record": "create",
            "update existing data": "update",
            "query patient database": "search",
            "delete patient record": "delete",
        }
        self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
        #self.nlp = spacy.load("en_core_web_trf")
        self.nlp = spacy.load("en_core_web_sm")
        self.add_entity_ruler_patterns(PATIENT_PATTERNS) # add condition patterns as well later here
        self.medical_ner = pipeline(
            "ner",
            model="sarahmiller137/distilbert-base-uncased-ft-ncbi-disease",
            tokenizer="sarahmiller137/distilbert-base-uncased-ft-ncbi-disease",
            aggregation_strategy="simple"
        )
    def classify(self, prompt: str):
        """Classify the prompt into a FHIR resource and request type"""
        classify_resource = self.classifier(prompt, list(self.resource_templates.keys()))
        classify_request = self.classifier(prompt, list(self.requests.keys()))
        
        resource_idx_max = pd.Series(classify_resource['scores']).idxmax()
        resource = classify_resource['labels'][resource_idx_max]
        
        request_idx_max = pd.Series(classify_request['scores']).idxmax()
        request = classify_request['labels'][request_idx_max]
        
        return self.resource_templates[resource], self.requests[request]
    
    def create_ruler(self):
        """Add resource-specific rules"""
        if "entity_ruler" not in self.nlp.pipe_names:
            ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        else:
            ruler = self.nlp.get_pipe("entity_ruler")
        return ruler
    
    def add_entity_ruler_patterns(self, patterns: list):
        """Add patterns to the EntityRuler"""
        ruler = self.create_ruler()
        ruler.add_patterns(patterns)
    
    def apply_ner(self, prompt: str):
        """Extract entities using NER + EntityRuler"""
        doc = self.nlp(prompt)
        entities = [{"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char} 
                    for ent in doc.ents]
        medical_entities = self.medical_ner(prompt)
        for ent in medical_entities:
            if ent['entity_group'] != 'LABEL_0':
                entities.append({"text": ent['word'], "label": ent['entity_group'], 
                                "start": ent['start'], "end": ent['end']})
        return entities
    
    def dispatch(self, prompt: str, base_url: str = "[base]"):
        """Main dispatch function to classify, extract entities, and generate payload"""
        fhir_resource, request = self.classify(prompt)
        entities = self.apply_ner(prompt)
        if not entities:
            return {"error": "No entities found", "resource": str(fhir_resource.__name__)}
        fhir_prompt = fhir_resource(request) # Instantionation happend here
        try: 
            payload = fhir_prompt.process(entities, base_url) # a base url can be passed here
        except NotImplementedError as e:
            return {"error": str(e), "resource": str(fhir_resource.__name__)}
        return payload
