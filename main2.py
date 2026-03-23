import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import streamofepic 
import supa
import csv
import os
from threading import Lock
import asyncio
import json

app = FastAPI(
    title="EPIC Service",
    description="Epic Service",
    version="1.0.0"
)

class EpicPayload(BaseModel):
    epnos: List[str]

output_file = r"D:\Code\nbmc_js\Captcha\details_using_epicNo\resultsnew.csv"
column_names = ["epNo", "status", "data"]
# A lock to prevent race conditions when writing to the CSV from multiple requests
csv_lock = Lock()

@app.post("/process")
async def process_epics(payload: EpicPayload):
    
    if not payload.epnos:
        raise HTTPException(status_code=400, detail="The 'epnos' list cannot be empty.")


    results_generator = streamofepic.process_stream_epics(payload.epnos, max_workers=30)

    all_results = []
    
    # Acquire lock to ensure safe file writing
    with csv_lock:
        file_exists = os.path.isfile(output_file)
        
        with open(output_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=column_names)
            
            if not file_exists:
                writer.writeheader()

            # Process each result from the generator
            for result in results_generator:
                if isinstance(result.get('data'), dict):
                    # Save to Supabase
                    if result.get('status') == 'success':
                        try:
                            parsed_data = supa.parse_eci_response(result['data'])
                            save_task = asyncio.create_task(supa.process_voter_data(parsed_data))
                            # We can choose to wait for it or not.
                            # If we don't await, it will run in the background.
                            # Let's wait to ensure it's saved before responding if it's just one.
                            # If processing many, it's better to not wait here.
                            # await save_task
                        except Exception as e:
                            print(f"Error saving to Supabase: {e}")

                    result['data'] = json.dumps(result['data'])
                
                writer.writerow(result)
                all_results.append(result)
            
            file.flush()

    return {"status": "processing_complete", "results_count": len(all_results), "output_file": output_file}

if __name__ == "__main__":
    print(f"Server shuru hoing")
    uvicorn.run(app, host="127.0.0.1", port=8001)