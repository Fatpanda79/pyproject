# ============================================
# api_server.py
# ============================================

from fastapi import FastAPI, Query
from pydantic import BaseModel
import math

app = FastAPI(
    title="Example API Service",
    description="A demo API using dictionaries (no explicit JSON).",
    version="1.0.0"
)

# ---- 1) GET: square root ----
@app.get("/sqrt")
def get_square_root(value: int = Query(..., description="Integer number to find square root of")):
    if value < 0:
        return {"error": "Cannot compute square root of a negative number"}
    return {"input": value, "square_root": math.sqrt(value)}

# ---- 2) GET: sum of range ----
@app.get("/range_sum")
def get_range_sum(from_param: int = Query(...), to_param: int = Query(...)):
    if from_param > to_param:
        from_param, to_param = to_param, from_param
    total = sum(range(from_param, to_param + 1))
    return {"from": from_param, "to": to_param, "sum": total}

# ---- 3) POST: receive and return dictionary ----
class DataModel(BaseModel):
    data: dict

@app.post("/process_dict1")
def process_dictionary(payload: dict):
    return {"received_data": payload, "key_count": len(payload)}

@app.post("/process_dict2")
def process_dictionary(payload: DataModel):
    data = payload.data
    return {"received_data": data, "key_count": len(data)}

# Run using: uvicorn api_server:app --reload
