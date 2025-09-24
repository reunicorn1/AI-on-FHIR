# AI on FHIR API Engine

A  modular, **object-oriented prototype**  that converts natural language queries about patients into  **FHIR API requests**. This engine is designed for rapid prototyping and demonstrates how to map unstructured medical queries into structured FHIR API calls.

## Table of Contents

- [AI on FHIR API Engine](#ai-on-fhir-api-engine)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Workflow](#workflow)
  - [Current Support and Limitations](#current-support-and-limitations)
    - [✅ What is currently supported](#-what-is-currently-supported)
    - [⚠️ Limitations](#️-limitations)
  - [Usage](#usage)
  - [Example Mappings](#example-mappings)
  - [Future Improvements](#future-improvements)

## Overview

This engine takes a natural language query, extracts relevant patient information, and generates a  **FHIR API request**. It is currently focused on the  **Patient resource**  with associated conditions, but the design is modular and can be extended to other FHIR resources in the future.

Key design principles:

- **Object-oriented**: Each resource (Patient, Condition, etc.) has its own class.
- ****Leverages multiple NLP techniques/models****: The engine processes queries using a combination of NLP models and rule-based logic.
- **Extensible**: You can add more resource types or attributes with minimal changes.

## Workflow

1. **Input**: The user provides a natural language query.

2. **Zero-shot Classification**:

- Uses  **`facebook/bart-large-mnli`**  to determine the FHIR resource type (currently  `Patient`) and request type (`GET`,  `POST`,  `PUT`,  `DELETE`).

4. **Named Entity Recognition (NER)**:

- SpaCy with  **`en_core_web_trf`**  transformer model.

- **EntityRuler**  for custom rules to extract patient attributes (e.g., demographics, identifiers, contact info, conditions).

- Medical-specific NER using  **`distilbert-base-uncased-ft-ncbi-disease`**  for disease recognition.

5. **Resource Class Handling**:

    - Entities are passed to the relevant resource class.

    - Tags are normalized, cleaned, processed and mapped into a structured dictionary for the API request.

    - The dictionary is used to build a FHIR API URL and parameters.

6. **Output**:

    - The engine generates a  **fully-formed FHIR request**  that can be sent to a FHIR server.

    - Currently supports  `GET`  requests;  `POST`,  `PUT`, and  `DELETE`  will be added soon.

**Workflow Diagram:**  

![Screenshot-2025-09-24-at-3-04-39-PM.png](https://i.postimg.cc/C5pr5jww/Screenshot-2025-09-24-at-3-04-39-PM.png)

## Current Support and Limitations

### ✅ What is currently supported

- Querying  **multiple patients sharing the same condition**.

- Retrieving  **specific patient information**  based on extracted features such as age, gender, birthdate, identifiers, and condition codes.

- Generation of  **fully-formed FHIR API requests**  for  `GET`  operations.

- Extraction of patient-related attributes using  **custom NER rules**, including demographics, contact info, relations, and identifiers.

### ⚠️ Limitations

- **Disease vocabulary is limited**:

  - Although the engine uses NER to recognize diseases, it only handles a  **narrow set of terms**, so synonyms or uncommon disease phrasing may not be recognized.

- **Single-condition queries only**:

  - You cannot query for patients with multiple conditions at the same time.

- **Single-feature per entity**:

  - You cannot currently combine multiple attributes for the same entity in a single query (e.g., searching a patient by multiple identifiers simultaneously).

- **Limited request types**:

  - Currently supports only  `GET`  requests.  `POST`,  `PUT`, and  `DELETE`  are planned for future releases.

- **No complex logical queries**:

  - Queries involving AND/OR conditions between attributes or conditions are not supported yet.

- **Fallback on NER accuracy**:

  - Some entities may not be detected perfectly due to rule-based or model-based NER limitations.
  
## Usage

1. Clone the repository and install dependencies:

`git clone https://github.com/reunicorn1/AI-on-FHIR.git/`
 `cd AI-on-FHIR`
`pip install -r requirements.txt`

2. Run the  **main demo file**  to see the engine in action:

`python3 main.py`

3. Observe the output for each example query, including:

      plain - Generated FHIR request (method, URL, parameters, query string)

> You can add your own queries in  `main.py`  to test the engine.

## Example Mappings

Here are some examples of  **input NL queries**  and their corresponding  **FHIR API requests**:

   plain ```

   plain --- Example 1 ---
    Input NL query: Show me patients over 50 with diabetes
    Generated FHIR Request:
    Method: GET
    URL: [base]/Patient?birthdate=lt1975-01-01&_has:Condition:patient:code=44054006
    Parameters: {'birthdate': 'lt1975-01-01', '_has:Condition:patient:code': '44054006'}
    Query string: birthdate=lt1975-01-01&_has:Condition:patient:code=44054006
    
   plain --- Example 2 ---
    Input NL query: Show me patients less than 40 who are hypertensive
    Generated FHIR Request:
    Method: GET
    URL: [base]/Patient?birthdate=gt1985-01-01&_has:Condition:patient:code=38341003
    Parameters: {'birthdate': 'gt1985-01-01', '_has:Condition:patient:code': '38341003'}
    Query string: birthdate=gt1985-01-01&_has:Condition:patient:code=38341003
    
   plain --- Example 3 ---
    Input NL query: Find patients aged 30 with asthma
    Generated FHIR Request:
    Method: GET
    URL: [base]/Patient?birthdate=1995-01-01&_has:Condition:patient:code=195967001
    Parameters: {'birthdate': '1995-01-01', '_has:Condition:patient:code': '195967001'}
    Query string: birthdate=1995-01-01&_has:Condition:patient:code=195967001
    
    --- Example 4 ---
    Input NL query: Find all female patients born after 1990.
    Generated FHIR Request:
    Method: GET
    URL: [base]/Patient?gender=female&birthdate=gt1990-12-31
    Parameters: {'gender': 'female', 'birthdate': 'gt1990-12-31'}
    Query string: gender=female&birthdate=gt1990-12-31
    
    --- Example 5 ---
    Input NL query: Find diabetes cases diagnosed before 2015.
    Generated FHIR Request:
    Method: GET
    URL: [base]/Patient?_has:Condition:patient:code=44054006
    Parameters: {'_has:Condition:patient:code': '44054006'}
    Query string: _has:Condition:patient:code=44054006

## Future Improvements

1. **Enhanced entity extraction**:

    - Currently using rule-based NER and multiple models.

    - Plan to explore  **large language models (LLMs)**  to directly map medical notes to FHIR requests using embeddings for higher accuracy and speed. Refer to [this article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12312630/) for more information

2. **Support for additional request types**:

    - Add  `POST`,  `PUT`, and  `DELETE`  support to allow full CRUD operations.

3. **Caching**:

    - Avoid repeated requests for identical queries to improve performance.

5.   **Extensibility to other FHIR resources**:

   plain - Expand to  `Condition`,  `Observation`,  `MedicationRequest`, etc.
