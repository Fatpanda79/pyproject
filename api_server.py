# ============================================
# api_server.py
# Simple Car Rental API using text file storage
# Supports: list, add, update, delete cars & book a car
# ============================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import tempfile

app = FastAPI(
    title="Car Rental API",
    description="Admin can manage cars; customers can book cars",
    version="1.0.0"
)

DATA_FILE = "cars.txt"


if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write("")


def read_cars():
    cars = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 5:
                continue
            cars.append({
                "car_id": int(parts[0]),
                "car_name": parts[1],
                "car_type": parts[2],
                "price": parts[3],
                "status": parts[4]
            })
    return cars

def write_cars(cars):
    fd, tmpname = tempfile.mkstemp()
    with os.fdopen(fd, 'w', encoding="utf-8") as tmp:
        for c in cars:
            line = f'{c["car_id"]},{c["car_name"]},{c["car_type"]},{c["price"]},{c["status"]}\n'
            tmp.write(line)
    os.replace(tmpname, DATA_FILE)

def next_id(cars):
    if not cars:
        return 1
    return max(c["car_id"] for c in cars) + 1

def find_car(cars, car_id):
    for c in cars:
        if c["car_id"] == car_id:
            return c
    return None

class CarIn(BaseModel):
    car_name: str
    car_type: str
    price: str

class CarUpdate(BaseModel):
    car_name: Optional[str]
    car_type: Optional[str]
    price: Optional[str]
    status: Optional[str]

# Routes
@app.get("/cars")
def list_cars():
    cars = read_cars()
    return {"cars": cars, "count": len(cars)}

@app.post("/cars")
def add_car(car: CarIn):
    cars = read_cars()
    new_id = next_id(cars)
    new_car = {
        "car_id": new_id,
        "car_name": car.car_name,
        "car_type": car.car_type,
        "price": car.price,
        "status": "available"
    }
    cars.append(new_car)
    write_cars(cars)
    return {"message": "Car added", "car": new_car}

@app.put("/cars/{car_id}")
def update_car(car_id: int, update: CarUpdate):
    cars = read_cars()
    car = find_car(cars, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    if update.car_name is not None:
        car["car_name"] = update.car_name
    if update.car_type is not None:
        car["car_type"] = update.car_type
    if update.price is not None:
        car["price"] = update.price
    if update.status is not None:
        car["status"] = update.status
    write_cars(cars)
    return {"message": "Car updated", "car": car}

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    cars = read_cars()
    car = find_car(cars, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    cars = [c for c in cars if c["car_id"] != car_id]
    write_cars(cars)
    return {"message": "Car removed", "car_id": car_id}

@app.get("/cars/available")
def available_cars():
    cars = read_cars()
    available = [c for c in cars if c["status"] == "available"]
    return {"cars": available, "count": len(available)}

@app.post("/cars/{car_id}/book")
def book_car(car_id: int):
    cars = read_cars()
    car = find_car(cars, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    if car["status"] != "available":
        raise HTTPException(status_code=400, detail="Car is not available")
    car["status"] = "booked"
    write_cars(cars)
    return {"message": "Car booked", "car": car}
