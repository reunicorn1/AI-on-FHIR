# AI on FHIR API Engine

A modular, **object-oriented prototype** that converts natural language queries about patients into **FHIR API requests**. This engine is designed for rapid prototyping and demonstrates how to map unstructured medical queries into structured FHIR API calls.

## Table of Contents

- [AI on FHIR API Engine](#ai-on-fhir-api-engine)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Tech Stack](#tech-stack)
  - [Features](#features)
  - [Installation \& Setup](#installation--setup)
    - [Prerequisites](#prerequisites)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
    - [Quick Demo (API Engine Only)](#quick-demo-api-engine-only)
  - [Workflow](#workflow)
  - [Current Support and Limitations](#current-support-and-limitations)
    - [✅ What is currently supported](#-what-is-currently-supported)
    - [⚠️ Limitations](#️-limitations)
  - [Usage](#usage)
    - [Web Interface Usage](#web-interface-usage)
    - [API Engine Usage](#api-engine-usage)
  - [Example Mappings](#example-mappings)
  - [Demo](#demo)
  - [Future Improvements](#future-improvements)

## Overview

This engine takes a natural language query, extracts relevant patient information, and generates a **FHIR API request**. It is currently focused on the **Patient resource** with associated conditions, but the design is modular and can be extended to other FHIR resources in the future.

Key design principles:

- **Object-oriented**: Each resource (Patient, Condition, etc.) has its own class.
- **Leverages multiple NLP techniques/models**: The engine processes queries using a combination of NLP models and rule-based logic.
- **Extensible**: You can add more resource types or attributes with minimal changes.

## Tech Stack

- **Backend:** Flask API with Uvicorn ASGI server
- **Frontend:** React and Next.js
- **NLP Models:** 
  - Zero-shot classification with `facebook/bart-large-mnli`
  - NER with SpaCy `en_core_web_trf` transformer model
  - Medical NER using `distilbert-base-uncased-ft-ncbi-disease`
- **Data Visualization:** Interactive charts (pie charts, bar charts, data tables)

## Features

- **Natural Language Processing:** Convert medical queries into structured FHIR API requests
- **Smart Search:** Input query with autocompletion functionality
- **Multiple Visualizations:**
  - Data table view for detailed patient data inspection
  - Pie charts for demographic distributions
  - Bar charts for comparative analysis
  - Statistical summaries for key insights
- **Demographics Analysis:** Comprehensive patient demographic data visualization
- **FHIR Compliance:** Generate fully-formed FHIR API requests
- **Responsive Interface:** Built with React.js for smooth user experience

## Installation & Setup

### Prerequisites

Make sure you have the following installed:
- Python 3.7+
- Node.js 14+
- npm

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/reunicorn1/AI-on-FHIR.git/
   cd AI-on-FHIR
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask API server**
   ```bash
   uvicorn app.main:app --reload
   ```

   The backend server will start running on `http://localhost:8000` (or the configured port).

### Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd front-app
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

   The frontend application will be available at `http://localhost:3000` (or the configured port).

### Quick Demo (API Engine Only)

To test the core NLP-to-FHIR functionality without the web interface:

```bash
python3 main.py
```

## Workflow

1. **Input**: The user provides a natural language query.

2. **Zero-shot Classification**:

- Uses **`facebook/bart-large-mnli`** to determine the FHIR resource type (currently `Patient`) and request type (`GET`, `POST`, `PUT`, `DELETE`).

4. **Named Entity Recognition (NER)**:

- SpaCy with **`en_core_web_trf`** transformer model.

- **EntityRuler** for custom rules to extract patient attributes (e.g., demographics, identifiers, contact info, conditions).

- Medical-specific NER using **`distilbert-base-uncased-ft-ncbi-disease`** for disease recognition.

5. **Resource Class Handling**:

    - Entities are passed to the relevant resource class.

    - Tags are normalized, cleaned, processed and mapped into a structured dictionary for the API request.

    - The dictionary is used to build a FHIR API URL and parameters.

6. **Output**:

    - The engine generates a **fully-formed FHIR request** that can be sent to a FHIR server.

    - Currently supports `GET` requests; `POST`, `PUT`, and `DELETE` will be added soon.

**Workflow Diagram:**  

[![Screenshot-2025-09-25-at-6-58-24-AM.png](https://i.postimg.cc/kXS33dxr/Screenshot-2025-09-25-at-6-58-24-AM.png)]

## Current Support and Limitations

### ✅ What is currently supported

- Querying **multiple patients sharing the same condition**.

- Retrieving **specific patient information** based on extracted features such as age, gender, birthdate, identifiers, and condition codes.

- Generation of **fully-formed FHIR API requests** for `GET` operations.

- Extraction of patient-related attributes using **custom NER rules**, including demographics, contact info, relations, and identifiers.

- **Web Interface Features:**
  - Interactive data visualization with multiple chart types
  - Autocompletion for query input
  - Patient demographics analysis and statistical summaries

### ⚠️ Limitations

- **Disease vocabulary is limited**:

  - Although the engine uses NER to recognize diseases, it only handles a **narrow set of terms**, so synonyms or uncommon disease phrasing may not be recognized.

- **Single-condition queries only**:

  - You cannot query for patients with multiple conditions at the same time.

- **Single-feature per entity**:

  - You cannot currently combine multiple attributes for the same entity in a single query (e.g., searching a patient by multiple identifiers simultaneously).

- **Limited request types**:

  - Currently supports only `GET` requests. `POST`, `PUT`, and `DELETE` are planned for future releases.

- **No complex logical queries**:

  - Queries involving AND/OR conditions between attributes or conditions are not supported yet.

- **Fallback on NER accuracy**:

  - Some entities may not be detected perfectly due to rule-based or model-based NER limitations.

- **Limited NLP integration in web interface**:

  - The current web interface provides autocompletion without full natural language processing capabilities.
  
## Usage

### Web Interface Usage

1. Start both the backend and frontend servers as described in the installation section
2. Open your browser and navigate to the frontend URL (`http://localhost:3000`)
3. Use the search input with autocompletion to query patient data
4. Switch between different visualization modes:
   - Table view for detailed data inspection
   - Pie charts for demographic distributions
   - Bar charts for comparative analysis
   - Statistical summaries for key insights

### API Engine Usage

Run the **main demo file** to see the core NLP engine in action:

```bash
python3 main.py
```

Observe the output for each example query, including:
- Generated FHIR request (method, URL, parameters, query string)

> You can add your own queries in `main.py` to test the engine.

## Example Mappings

Here are some examples of **input NL queries** and their corresponding **FHIR API requests**:

``` text

--- Example 1 ---
Input NL query: Show me patients over 50 with diabetes
Generated FHIR Request:
Method: GET
URL: [base]/Patient?birthdate=lt1975-01-01&_has:Condition:patient:code=44054006
Parameters: {'birthdate': 'lt1975-01-01', '_has:Condition:patient:code': '44054006'}
Query string: birthdate=lt1975-01-01&_has:Condition:patient:code=44054006

--- Example 2 ---
Input NL query: Show me patients less than 40 who are hypertensive
Generated FHIR Request:
Method: GET
URL: [base]/Patient?birthdate=gt1985-01-01&_has:Condition:patient:code=38341003
Parameters: {'birthdate': 'gt1985-01-01', '_has:Condition:patient:code': '38341003'}
Query string: birthdate=gt1985-01-01&_has:Condition:patient:code=38341003

--- Example 3 ---
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

```

## Demo

Watch the application in action:

[![AI on FHIR Demo Video](https://img.youtube.com/vi/ivUJU1SSWLA/0.jpg)](https://youtu.be/ivUJU1SSWLA)

**[🎬 View Demo Video](https://youtu.be/ivUJU1SSWLA)**

The demo showcases:

-   Natural language query processing
-   Real-time autocompletion functionality
-   Multiple data visualization options (tables, charts, statistics)
-   Patient demographics analysis and filtering

## Future Improvements

1. **Enhanced entity extraction**:

    - Currently using rule-based NER and multiple models.

    - Plan to explore **large language models (LLMs)** to directly map medical notes to FHIR requests using embeddings for higher accuracy and speed. Refer to [this article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12312630/) for more information

2. **Support for additional request types**:

    - Add `POST`, `PUT`, and `DELETE` support to allow full CRUD operations.

3. **Caching**:

    - Avoid repeated requests for identical queries to improve performance.

4. **Enhanced Web Interface**:

    - Full natural language processing integration in the web interface
    - Advanced visualization options and filtering

5. **Extensibility to other FHIR resources**:

    - Expand to `Condition`, `Observation`, `MedicationRequest`, etc.
