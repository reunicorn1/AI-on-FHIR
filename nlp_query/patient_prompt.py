from nlp_query.base_prompt import FHIRBasePrompt
import re
from datetime import datetime
from nlp_query.patterns.disease_codes import DISEASE_CODE
from difflib import get_close_matches

class PatientPrompt(FHIRBasePrompt):
    CUTOFF=0.6
    """
    ### Patients

    - **Demographics** (name, birthdate, gender, deceased)
    - **Identifiers** (ID, MRN, SSN, etc.)
    - **Contact** (phone, email, address parts)
    - **Relations** (organization, GP, linked patient)

        Returns:
            _type_: _description_
    """
    def __init__(self, request_type):
        super().__init__(request_type)
        # This is for documentation purposes only
        self.field_map = {
            "identifier": "PID-3",
            "name": "PID-5",
            "family": "PID-5.1",
            "given": "PID-5.2",
            "gender": "PID-8",
            "birthdate": "PID-7",
            "address": "PID-11",
            "address-city": "PID-11.3",
            "address-state": "PID-11.4", 
            "deceased": "PID-30",
            "deceased-date": "PID-29",
            "phone": "PID-13",
            "email": "PID-13.4",
            "general-practitioner": "PV1-7",
            "organization": "PV1-3",
        }
        # Create reverse mapping for direct labels which require no processing
        self.entity_to_field_map = {
            "IDENTIFIER": "identifier",
            "PHONE": "phone",
            "EMAIL": "email",
            "GPE": "address",
            "LOC": "address",
            "FAC": "address",
        }
        self.entity_to_normalize = [
            "GP_TRIGGER", "GIVEN_NAME_TRIGGER", "FAMILY_NAME_TRIGGER",
            "NAME_GENERAL","DEATH_KEYWORD", "BIRTH_KEYWORD", "LABEL_1", "LABEL_2",
            # "YEAR_RANGE", "YEAR_AFTER", "YEAR_BEFORE", "ON_YEAR", "AGE_OVER",
            # "AGE_UNDER", "AGE_EXACT", "AGE", "DATE",
            "GENDER_MALE", "GENDER_FEMALE", "GENDER_OTHER"
        ] 
        self.data = {}
        self.filled_fields = set()
        self.skipped_fields = set(self.field_map.keys())
        
    def fill_from_entities(self, entities):
        """Extract and map entities to FHIR fields
        
        Handles:
        - Demographics (name, birthdate, gender, deceased)
        - Identifiers (ID, MRN, SSN, etc.)
        - Contact (phone, email, address parts)
        - Relations (organization, GP, linked patient)
        """
        for entity in entities:
            entity_label = entity.get("label", "").upper()
            entity_text = entity.get("text", "").strip()
            
            if not entity_text:
                continue
            
            # Try direct mapping first
            field = self.entity_to_field_map.get(entity_label, None)
            if field and field not in self.filled_fields:
                self._set_field(field, entity_text)
                continue
            if entity_label == "DEATH_KEYWORD":
                self._set_field("deceased", True)
                # Don't continue here, because we might want to extract date too if available
            # Try normalization if direct mapping fails
            if entity_label in self.entity_to_normalize:
                normalized_value, normalized_field = self._normalize_field_value(
                    entity_label, entity, entities # pass full entities for context because context is needed
                )
                if normalized_field and normalized_field not in self.filled_fields:
                    self._set_field(normalized_field, normalized_value)
        self._check_name_in_context(entities) # check if a PERSON entity is in context after the trigger
        self._check_age_in_context(entities) # check if an AGE entity is in context after the trigger
        
    def _set_field(self, field_name, value):
        """Helper to set field and update tracking sets"""
        self.data[field_name] = value
        self.filled_fields.add(field_name)
        self.skipped_fields.discard(field_name)

    def _check_name_in_context(self, entities):
        """Check if a PERSON entity is in context after the trigger"""
        if not any(data for data in self.data if data in ["given", "family", "general-practitioner"]):
            for ent in entities:
                if ent['label'] == 'PERSON':
                    self._set_field('name', ent['text'])
                    break

    def _check_age_in_context(self, entities):
        """Check if an AGE entity is in context after the trigger"""
        if not any(data for data in self.data if data in ["birthdate", "deceased-date"]):
            for ent in entities:
                if ent['label'] in {"AGE_OVER", "AGE_UNDER", "AGE_EXACT", "AGE"}:
                    age_value = self._normalize_age(ent)
                    if age_value:
                        self._set_field('birthdate', age_value)
                    break

    def _normalize_field_value(self, entity_label, entity, full_entities):
        """Normalize values according to FHIR specifications"""
        normalizers = {
            "GP_TRIGGER": self._normalize_gp,
            "GIVEN_NAME_TRIGGER": self._normalize_name, 
            "FAMILY_TRIGGER": self._normalize_name,
            "NAME_GENERAL": self._normalize_name,
            "DEATH_KEYWORD": self._normalize_death_birth,
            "BIRTH_KEYWORD": self._normalize_death_birth,
            "GENDER_FEMALE": self._normalize_gender,
            "GENDER_MALE": self._normalize_gender,
            "GENDER_OTHER": self._normalize_gender,
            "LABEL_1": self._normalize_condition,
            "LABEL_2": self._normalize_condition
        }
        normalizer = normalizers.get(entity_label, lambda x, e=None: x)
        return normalizer(field_name=entity_label, entity=entity, full_entities=full_entities) # Normalizers should return (value, field) tuple
    def _normalize_gp(self, **kwargs):
        """Extract GP name from context"""
        value = kwargs['entity']
        entities= kwargs['full_entities']
        gp_name = None
        for ent in entities:
            if ent['label'] == 'PERSON' and ent['start'] > value['end']:
                gp_name = ent['text']
                break
        return gp_name, "general-practitioner" if gp_name else (None, None)
    
    def _normalize_name(self, **kwargs):
        """Extract full name from context"""
        field_name = kwargs['field_name']
        value = kwargs['entity']
        entities= kwargs['full_entities']
        full_name = None
        value_label = {
            "GIVEN_NAME_TRIGGER": "given",
            "FAMILY_NAME_TRIGGER": "family",
            "NAME_GENERAL": "name",
        }
        for ent in entities:
            if ent['label'] == 'PERSON' and ent['start'] >= value['end']:
                full_name = ent['text']
                break
        return full_name, value_label[field_name] if full_name else (None, None)
    
    def _normalize_gender(self, **kwargs):
        """Extract gender value"""
        field_name = kwargs['field_name']
        if field_name == "GENDER_FEMALE":
            gender = "female"
        elif field_name == "GENDER_MALE":
            gender = "male"
        else:
            gender = "other"
        return gender, "gender"
    
    def _normalize_death_birth(self, **kwargs):
        """Set dates and times after as deceased time or birthdate"""
        # Look for DATE or ON_YEAR entities after the death keyword
        field_name = kwargs['field_name']
        value = kwargs['entity']
        entities= kwargs['full_entities']
        field = {
            "BIRTH_KEYWORD": "birthdate",
            "DEATH_KEYWORD": "deceased-date",
        }
        date_labels = {"DATE", "ON_YEAR", "YEAR_RANGE", "YEAR_AFTER", "YEAR_BEFORE"}
        age_labels = {"AGE_OVER", "AGE_UNDER", "AGE_EXACT", "AGE"}
        date = None
        for ent in entities:
            if ent['label'] in date_labels and ent['start'] > value['end']:
                date = self._normalize_date(ent)
                break
            if ent['label'] in age_labels and ent['start'] > value['end']:
                date = self._normalize_age(ent)
                break
        return date, field[field_name] if date else (None, None)
    
    def _normalize_date(self, entity=None):
        """Convert various date formats and patterns to FHIR search format"""
        text = entity.get("text", "") if isinstance(entity, dict) else str(entity)
        entity_label = entity.get("label", "") if entity else ""
        
        # Handle specific entity types
        if entity_label == "YEAR_RANGE":
            # "1990 to 2000" or "1990-2000" → ge1990,le2000 #in current implementation this is not used
            years = re.findall(r'\d{4}', text)
            if len(years) >= 2:
                return f"ge{years[0]},le{years[1]}"
        
        elif entity_label == "ON_YEAR":
            # "in 1995" or "on 1990" → 1995
            year_match = re.search(r'\b(\d{4})\b', text)
            if year_match:
                return year_match.group(1)
        
        elif entity_label == "YEAR_AFTER":
            # "after 2020" → gt2020-12-31
            year_match = re.search(r'\b(\d{4})\b', text)
            if year_match:
                return f"gt{year_match.group(1)}-12-31"
        
        elif entity_label == "YEAR_BEFORE":
            # "before 2034" → lt2034-01-01
            year_match = re.search(r'\b(\d{4})\b', text)
            if year_match:
                return f"lt{year_match.group(1)}-01-01"

        # Handle exact dates
        date_formats = [
            ("%Y-%m-%d", r'\b\d{4}-\d{1,2}-\d{1,2}\b'),       # YYYY-MM-DD
            ("%Y/%m/%d", r'\b\d{4}/\d{1,2}/\d{1,2}\b'),       # YYYY/MM/DD
            ("%d-%m-%Y", r'\b\d{1,2}-\d{1,2}-\d{4}\b'),       # DD-MM-YYYY
            ("%d/%m/%Y", r'\b\d{1,2}/\d{1,2}/\d{4}\b'),       # DD/MM/YYYY
            ("%B %d, %Y", r'\b[A-Za-z]+ \d{1,2}, \d{4}\b'),   # January 15, 2020
            ("%b %d, %Y", r'\b[A-Za-z]{3} \d{1,2}, \d{4}\b'), # Jan 15, 2020
            ("%d %B %Y", r'\b\d{1,2} [A-Za-z]+ \d{4}\b'),     # 15 January 2020
            ("%d %b %Y", r'\b\d{1,2} [A-Za-z]{3} \d{4}\b'),   # 15 Jan 2020
        ]
        
        for fmt, pattern in date_formats:
            match = re.search(pattern, text)
            if match:
                try:
                    matched_text = match.group(0)
                    parsed_date = datetime.strptime(matched_text, fmt)
                    return parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    continue
        
        # Handle year only as last resort
        year_match = re.search(r'\b(\d{4})\b', text)
        if year_match:
            year = year_match.group(1)
            # Check if it's a reasonable year (1900-2100)
            if 1900 <= int(year) <= 2100:
                return year
        
        return None
    
    def _normalize_condition(self, **kwargs):
        """Extract condition name from entity"""
        entity = kwargs['entity']
        entities = kwargs['full_entities']
        disease = entity.get("text", None)
        entity_label = entity.get('label', None) # This could be either LABEL_1 or LABEL_2
        if entity_label == "LABEL_1": # if "LABEL_2" was checked first, it won't be followed by another "LABEL_2"
            for ent in entities:
                if ent['label'] == 'LABEL_2' and ent['start'] == entity['end'] + 1:
                    disease += " " + ent['text']
                    break
        elif entity_label == "LABEL_2":
            for ent in entities:
                if ent['label'] == 'LABEL_1' and ent['end'] == entity['start'] - 1:
                    return None, None # skip this one because it was already handled
        return disease, "condition" if disease else (None, None)

            
    def _normalize_age(self, entity=None):
        """Convert age expressions to FHIR search format"""
        text = entity.get("text", "") if isinstance(entity, dict) else str(entity)
        entity_label = entity.get("label", "") if entity else ""
        
        # Extract age number from text
        age_match = re.search(r'(\d{1,3})', text)
        if not age_match:
            return None
        
        age_value = int(age_match.group(1))
        birth_year = datetime.now().year - age_value
        birth_date = f"{birth_year}-01-01"
        
        # Return appropriate format based on entity type
        if entity_label == "AGE_OVER":
            return f"lt{birth_date}"  # Over 30 means born before (birth_year - 30)
        elif entity_label == "AGE_UNDER":
            return f"gt{birth_date}"  # Under 30 means born after (birth_year - 30)
        elif entity_label in ["AGE_EXACT", "AGE"]:
            return birth_date
        
        return birth_date
    def _get_disease_code(self, disease):
        """Classify disease text and return SNOMED code"""
        disease_names = list(DISEASE_CODE.keys())
        matches = get_close_matches(disease.lower(), disease_names, n=1, cutoff=self.CUTOFF)
        return DISEASE_CODE[matches[0]] if matches else 0

    def process(self, entities: list, base_url: str = "[base]") -> dict:
        """Generate FHIR API request based on request_type"""
        self.fill_from_entities(entities)
        #print("This is entities", entities)
        #print("This is data", self.data)

        if self.request_type == "search":
            # Generate GET request URL
            return self._generate_get_request(base_url)
        elif self.request_type == "create":
            return self._generate_post_request(base_url)
        elif self.request_type == "update":
            return self._generate_put_request(base_url)
        else:
            return {"error": f"Unsupported request type: {self.request_type}"}

    def _generate_get_request(self, base_url: str = "[base]") -> dict:
        """Generate GET request for FHIR Patient search"""
        
        if not self.data:
            return {
                "method": "GET",
                "url": f"{base_url}/Patient",
                "parameters": {},
                "query_string": ""
            }
        
        # Build query parameters from processed data
        query_params = []
        condition = self.data.pop("condition", None) # extract condition if exists
        for field, value in self.data.items():
            if value is not None:
                # Handle boolean values (like deceased)
                if isinstance(value, bool):
                    query_params.append(f"{field}={str(value).lower()}")
                else:
                    # URL encode the value if needed (basic implementation)
                    encoded_value = str(value).replace(" ", "%20")
                    query_params.append(f"{field}={encoded_value}")
        if condition: # conditions needs to be extracted separately also they're assumed to be only one condition for now
            # Add reverse include for Condition resource
            code = self._get_disease_code(condition)
            query_params.append(f'_has:Condition:patient:code={code}')
            self.data['_has:Condition:patient:code'] = code # add it back to data for reference

        # Join parameters with &
        query_string = "&".join(query_params)
        full_url = f"{base_url}/Patient?{query_string}" if query_string else f"{base_url}/Patient"
        return {
            "method": "GET",
            "url": full_url,
            "parameters": dict(self.data),
            "query_string": query_string
        }

    def _generate_post_request(self, base_url: str = "[base]") -> dict:
        """Generate POST request for creating Patient"""
        # Convert processed data to FHIR Patient resource
        patient_resource = {
            "resourceType": "Patient"
        }
        # Field mapping for POST payload structure
        field_mapping = {
            "birthdate": "birthDate",           # API uses camelCase
            "deceased": "deceasedBoolean",      
            "deceased-date": "deceasedDateTime",
            "phone": "telecom",                 # Will need special handling
            "email": "telecom",                 # Will need special handling
            "address-city": "address",          # Will need special handling
            "address-state": "address",         # Will need special handling
            "general-practitioner": "generalPractitioner",
            "organization": "managingOrganization"
        }

        # Handle name fields specially (they need to be combined)
        name_obj = {}
        if "family" in self.data:
            name_obj["family"] = self.data["family"]
        if "given" in self.data:
            name_obj["given"] = [self.data["given"]]
        if name_obj:
            patient_resource["name"] = [name_obj]

        # Iterate through all other fields
        for field, value in self.data.items():
            if field in ["given", "family"]:
                continue  # Already handled above
            
            # Map field name to FHIR structure
            fhir_field = field_mapping.get(field, field)
            
            # Special handling for complex fields
            if field in ["phone", "email"]:
                if "telecom" not in patient_resource:
                    patient_resource["telecom"] = []
                system = "phone" if field == "phone" else "email"
                patient_resource["telecom"].append({
                    "system": system,
                    "value": value
                })
            else:
            # Direct mapping
                patient_resource[fhir_field] = value
        return {
            "method": "POST",
            "url": f"{base_url}/Patient",
            "body": patient_resource
        }

    def _generate_put_request(self, base_url: str = "[base]") -> dict:
        """Generate PUT request for updating Patient"""
        # Similar to POST but would need patient ID
        idx = self.data.get("identifier", "unknown-id")
        if idx == "unknown-id":
            return {"error": "Identifier is required for update"}
        return {
            "method": "PUT", 
            "url": f"{base_url}/Patient/[id]",
            "body": self._generate_post_request()["body"]
        }