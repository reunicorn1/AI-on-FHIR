from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
from fastapi.middleware.cors import CORSMiddleware
from app.config import FHIR_BASE_URL, FHIR_HEADERS
from nlp_query.dispatcher import Dispatcher
from app.utils import simplify_patient_data

app = FastAPI(title="FHIR NL Query API")
dispatcher = Dispatcher()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    """Model for incoming query requests"""
    query: str

@app.post("/query")
def handle_query(request: QueryRequest):
    if request is None or not request.query:
        raise HTTPException(status_code=400, detail="Query parameter is required.")             
    query_string = request.query
    
    try:
        print(f"Received query: {query_string}")
        print(f"Dispatch generated: {query_string}")
        
        # 1. Process the NL query using your dispatch engine
        fhir_request = dispatcher.dispatch(query_string, FHIR_BASE_URL)

        # fhir_request should return a dict like:
        # {"method": "GET", "url": "[base]/Patient?birthdate=...", "parameters": {...}}

        # 2. Send request to FHIR server
        method = fhir_request.get("method", "GET")
        url = fhir_request.get("url", None)
        params = fhir_request.get("parameters", {})
        
        print(f"FHIR request to {url} with params {params}")
        if not url:
            raise HTTPException(status_code=400, detail="Invalid FHIR request generated.")
        
        handlers = {
            "GET": lambda url, params: requests.get(url, headers=FHIR_HEADERS, timeout=90)
        }
        if method not in handlers:
            raise HTTPException(status_code=501, detail=f"Method {method} not implemented.")
            
        response = handlers[method](url, params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        fhir_data = response.json()
        # 3. Convert to simplified JSON
        return {"results": simplify_patient_data(fhir_data, params)}

    except Exception as e:
        print("I caught an error:")
        print(e)
        raise HTTPException(status_code=500, detail=str(e))