"""
Demo of the Medical Query Engine
This file demonstrates how the engine processes queries,
extracts entities, normalizes them, and generates FHIR requests.
"""

from nlp_query.dispatcher import Dispatcher

# Instantiate the engine
dispatcher = Dispatcher()

# Example queries to demonstrate
# Currently we support patient queries with conditions
# Next update will support creating new patients, updating existing patients
demo_queries = [
    "Show me patients over 50 with diabetes",
    "Show me patients less than 40 who are hypertensive",
    "Find patients aged 30 with asthma",
    "Find all female patients born after 1990.",
    #"Create a new patient record for John Doe, a 45-year",
    "Find diabetes cases diagnosed before 2015.",
    #"Update the record of patient with ID 1733722 to update their name to Jane Smith",
]

for i, query in enumerate(demo_queries, 1):
    print(f"\n--- Example {i} ---")
    print(f"Input NL query: {query}")

    # Process the query through your engine
    # This should extract entities, normalize them, and build the FHIR URL
    fhir_request = dispatcher.dispatch(query)  # returns dict with method, url, params, etc.

    # Output demonstration
    print("Generated FHIR Request:")
    print(f"Method: {fhir_request['method']}")
    print(f"URL: {fhir_request['url']}")
    print(f"Parameters: {fhir_request.get('parameters')}")
    print(f"Query string: {fhir_request.get('query_string')}")

