import logging
import os
import pymongo
import azure.functions as func

app = func.FunctionApp()

@app.route(route="CV_data", auth_level=func.AuthLevel.ANONYMOUS)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get Cosmos DB connection string from environment variables
        cosmos_db_connection_string = os.environ['COSMOS_DB_CONNECTION_STRING'] 
        client = pymongo.MongoClient(cosmos_db_connection_string)
        
        database = client['CV']
        collection = database['cv']

        # Retrieve data from the collection
        data = list(collection.find({}, {"_id": 0}))  # Exclude the `_id` field from the results

        # Convert the list of documents to JSON string
        import json
        data_json = json.dumps(data)

        return func.HttpResponse(data_json, mimetype="application/json")

    except Exception as e:
        logging.error(f"Could not connect to the database: {str(e)}")
        return func.HttpResponse("Failed to fetch data from the database.", status_code=500)