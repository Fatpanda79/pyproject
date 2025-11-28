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

CUSTOMER_FILE = "customer.txt"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write("")
if not os.path.exists(CUSTOMER_FILE):
    with open(CUSTOMER_FILE, "w", encoding="utf-8") as f:
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


# @app.post("/cars/{car_id}/book")
# def book_car(car_id: int):
#     cars = read_cars()
#     car = find_car(cars, car_id)
#     if not car:
#         raise HTTPException(status_code=404, detail="Car not found")
#     if car["status"] != "available":
#         raise HTTPException(status_code=400, detail="Car is not available")
#     car["status"] = "booked"
#     write_cars(cars)
#     return {"message": "Car booked", "car": car}

# ------------------------------>


class CustomerIn(BaseModel):
    customer_name: str
    customer_password: str

class CustomerUpdate(BaseModel):
    customer_name: Optional[str]
    customer_password: Optional[str]


def read_customers():
    customers = []
    if not os.path.exists(CUSTOMER_FILE):
        open(CUSTOMER_FILE, "w").close()
    with open(CUSTOMER_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 3:
                continue
            customers.append({
                "customer_id": int(parts[0]),
                "customer_name": parts[1],
                "customer_password": parts[2]
            })
    return customers


def new_customer_id(customers):
    if not customers:
        return 1
    return max(c["customer_id"] for c in customers) + 1


def write_customers(customers):
    fd, tmpname = tempfile.mkstemp()
    with os.fdopen(fd, 'w', encoding="utf-8") as tmp:
        for c in customers:
            line = f'{c["customer_id"]},{c["customer_name"]},{c["customer_password"]}\n'
            tmp.write(line)
    os.replace(tmpname, CUSTOMER_FILE)


@app.post("/customers")
def add_customer(customer: CustomerIn):
    customers = read_customers()
    new_id = new_customer_id(customers)
    new_customer = {
        "customer_id": new_id,
        "customer_name": customer.customer_name,
        "customer_password": customer.customer_password
    }
    customers.append(new_customer)
    write_customers(customers)
    return {"message": "Customer added", "customer": new_customer}


@app.post("/login")
def login(customer: CustomerIn):
    customers = read_customers()

    for c in customers:
        if c["customer_name"] == customer.customer_name and c["customer_password"] == customer.customer_password:
            return {
                "message": "Login successful",
                "customer": {
                    "customer_id": c["customer_id"],
                    "customer_name": c["customer_name"]
                }
            }
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, update: CustomerUpdate):
    customers = read_customers()
    customer = None

    for c in customers:
        if c["customer_id"] == customer_id:
            customer = c
            break

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if update.customer_name is not None:
        customer["customer_name"] = update.customer_name

    if update.customer_password is not None:
        customer["customer_password"] = update.customer_password

    write_customers(customers)

    return {"message": "Customer updated", "customer": customer}

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    customers = read_customers()

    exists = any(c["customer_id"] == customer_id for c in customers)
    if not exists:
        raise HTTPException(status_code=404, detail="Customer not found")

    customers = [c for c in customers if c["customer_id"] != customer_id]

    write_customers(customers)

    return {"message": "Customer deleted", "customer_id": customer_id}



Booking_FILE = "Booking.txt"


def read_Bookings():
    Bookings = []
    if not os.path.exists(Booking_FILE):
        open(Booking_FILE, "w").close()

    with open(Booking_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            Bookings.append({
                "Booking_id": int(parts[0]),
                "customer_id": int(parts[1]),
                "car_id": int(parts[2])
            })
    return Bookings


def write_Bookings(Bookings):
    fd, tmpname = tempfile.mkstemp()
    with os.fdopen(fd, 'w', encoding="utf-8") as tmp:
        for r in Bookings:
            tmp.write(f'{r["Booking_id"]},{r["customer_id"]},{r["car_id"]}\n')
    os.replace(tmpname, Booking_FILE)


def next_Booking_id(Bookings):
    if not Bookings:
        return 1
    return max(r["Booking_id"] for r in Bookings) + 1


@app.post("/cars/{car_id}/book/")
def book_car(car_id: int, customer_id: int):
    customers = read_customers()
    cars = read_cars()
    Bookings = read_Bookings()

    car = find_car(cars, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if not any(c["customer_id"] == customer_id for c in customers):
        raise HTTPException(status_code=404, detail="Customer not found")

    if car["status"] != "available":
        raise HTTPException(status_code=400, detail="Car is not available")

    car["status"] = "booked"
    write_cars(cars)

    new_id = next_Booking_id(Bookings)
    Bookings.append({
        "Booking_id": new_id,
        "customer_id": customer_id,
        "car_id": car_id
    })
    write_Bookings(Bookings)

    return {"message": "Car booked", "Booking_id": new_id}


@app.get("/customers/{customer_id}/Bookings")
def getCustomerBookings(customer_id: int):
    Bookings = read_Bookings()
    cars = read_cars()

    customer_Bookings = [r for r in Bookings if r["customer_id"] == customer_id]

    if not customer_Bookings:
        return {"message": "No Bookinged cars found", "cars": []}

    Booked_cars = []
    for Booking in customer_Bookings:
        for car in cars:
            if car["car_id"] == Booking["car_id"]:
                Booked_cars.append(car)

    return {
        "customer_id": customer_id,
        "count": len(Booked_cars),
        "cars": Booked_cars
    }


@app.delete("/customers/{customer_id}/cancel/{car_id}")
def cancel_booking(customer_id: int, car_id: int):
    customers = read_customers()
    cars = read_cars()
    bookings = read_Bookings()
    if not any(c["customer_id"] == customer_id for c in customers):
        raise HTTPException(status_code=404, detail="customer not found")


    car = find_car(cars, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    booking_found = False
    new_bookings = []

    for b in bookings:
        if b["customer_id"] == customer_id and b["car_id"] == car_id:
            booking_found = True
            continue
        new_bookings.append(b)

    if not booking_found:
        raise HTTPException(status_code=404, detail="no booking found")

    car["status"] = "available"
    write_cars(cars)


    write_Bookings(new_bookings)

    return {"message": "Car  cancelled successfully"}
