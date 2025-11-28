# ============================================
# api_client.py
# ============================================

import requests

API_BASE = "http://127.0.0.1:8000"


def call_list_cars():
    try:
        response = requests.get(f"{API_BASE}/cars")
        if response.status_code == 200:
            data = response.json()
            cars = data.get("cars", [])
            print(f"\n--- Total Cars: {data.get('count', 0)} ---")
            print(f"{'ID':<4} {'Name':<15} {'Type':<10} {'Price':<8} {'Year':<6} {'Mileage':<10} {'Trans':<10} {'Cond':<8} {'Status'}")
            print("-" * 95)
            for car in cars:
                print(
                    f"{car['car_id']:<4} {car['car_name']:<15} {car['car_type']:<10} {car['price']:<8} "
                    f"{car['year']:<6} {car['mileage']:<10} {car['transmission']:<10} {car['condition']:<8} {car['status']}"
                )
            print("-" * 95)
        else:
            print("Failed to fetch cars:", response.text)
    except Exception as e:
        print("Error connecting to server:", e)


def call_add_car():
    print("\n--- ADD NEW CAR ---")
    try:
        name = input("Enter car name: ").strip()
        ctype = input("Enter car type: ").strip()
        price = input("Enter price per day: ").strip()
        year = input("Enter Year (e.g. 2022): ").strip()
        mileage = input("Enter Mileage (e.g. 15000km): ").strip()
        transmission = input("Enter Transmission (e.g. Auto): ").strip()
        condition = input("Enter Condition (e.g. Used): ").strip()

        if not name or not ctype or not price:
            print("All fields are required!")
            return

        payload = {
            "car_name": name,
            "car_type": ctype,
            "price": price,
            "year": year,
            "mileage": mileage,
            "transmission": transmission,
            "condition": condition
        }

        response = requests.post(f"{API_BASE}/cars", json=payload)

        if response.status_code == 200:
            result = response.json()
            print("\nSUCCESS: Car added!")
            print(f"New Car ID: {result['car']['car_id']}")
        else:
            print("\nError adding car:", response.json())

    except Exception as e:
        print("Error:", e)


def call_delete_car():
    """Admin function to remove a car."""
    call_list_cars()
    print("\n--- REMOVE CAR ---")
    try:
        car_id = input("Enter the ID of the car to remove: ").strip()

        if not car_id.isdigit():
            print("Invalid ID. Please enter a number.")
            return

        confirm = input(f"Are you sure you want to delete Car ID {car_id}? (yes/no): ").lower()
        if confirm != 'yes':
            print("Deletion cancelled.")
            return

        response = requests.delete(f"{API_BASE}/cars/{car_id}")

        if response.status_code == 200:
            print(f"\nSUCCESS: Car ID {car_id} removed.")
        elif response.status_code == 404:
            print("\nError: Car ID not found.")
        else:
            print("\nError deleting car:", response.json())

    except Exception as e:
        print("Error:", e)


def adminPanel():
    while True:
        print("\n==============================")
        print("      ADMIN DASHBOARD        ")
        print("==============================")
        print("1. List All Cars")
        print("2. Add a Car")
        print("3. Remove a Car")
        print("4. Back to Main Menu")
        print("==============================")

        choice = input("Admin Option (1-4): ").strip()

        if choice == "1":
            call_list_cars()
        elif choice == "2":
            call_add_car()
        elif choice == "3":
            call_delete_car()
        elif choice == "4":
            break
        else:
            print("Invalid option.")


def askAdmin():
    try:
        password = input("type the password to access admin panel: ")
        if password == "admin123":
            adminPanel()
        else:
            print("the password is wrong try again")
            askAdmin()
    except Exception as e:
        print("Error:", e)

#--------------------------------------------------------------->



# customer_id = None

# def customer_menu():
#     print("\n--- CUSTOMER BOOKING ---")

#     try:
#         response = requests.get(f"{API_BASE}/cars/available")
#         if response.status_code == 200:
#             data = response.json()
#             cars = data.get("cars", [])
            

#             if not cars:
#                 print("No cars currently available.")
#                 return

#             print(f"\nAvailable Cars: {len(cars)}")
#             for car in cars:
#                 print(f"[ID: {car['car_id']}] {car['car_name']} ({car['car_type']}) - ${car['price']}/day")

#             book_id = input("\nEnter Car ID to book (or press Enter to cancel): ")
#             if book_id:
#                 res = requests.post(f"{API_BASE}/cars/{book_id}/book/{customer_id}")
#                 if res.status_code == 200:
#                     print(f"SUCCESS: You have booked the car!")
#                 else:
#                     print(f"Failed: {res.json().get('detail')}")
#         else:
#             print("Could not fetch available cars.")
#     except Exception as e:
#         print("Error:", e)


def customer_panel():
    print("1) Signup")
    print("2) Login")
    print("3) Return to Home")

    choice = input("choose between 1 to 3: ")
    if choice == "1":
        add_customer()
    elif choice == "2":
        logincustomer()
    elif choice == "3":
        main()
    else:
        print("please choose between 1 or 3")
        customer_panel()

def add_customer():

    name = input("Enter customer name: ").strip()
    password = input("Enter customer password: ").strip()
    payload = {
        "customer_name": name,
        "customer_password": password
    }

    try:
        response = requests.post(f"{API_BASE}/customers", json=payload)
        data = response.json()

        if response.status_code == 200:
            print("Customer added successfully!")
            print(f"ID: {data['customer']['customer_id']}")
            print(f"Name: {data['customer']['customer_name']}")
        else:
            print("Failed to add customer:", data.get("detail", data))

    except Exception as e:
        print("Error:", e)



def logincustomer():
    global customer_id
    customer_name = input("Enter user name: ").strip()
    customer_pass = input("Enter user password: ").strip()

    response = requests.post(f"{API_BASE}/login",
        json={"customer_name": customer_name, "customer_password": customer_pass}
    )

    if response.status_code == 200:
        print("login successful")
        if response.status_code == 200:
            data = response.json()
            customer_id = data["customer"]["customer_id"]
            print("login successful")
            #print(data["customer"]["customer_id"] )
            customerBookingpanel(customer_id)                
    else:
        print("not successful")

def customerBookingpanel(customer_id):
    print("1) Book a car")
    print("2) cancel Booked car")
    choice = input("choose between 1 - 2: ")
    if choice == "1":
        customer_menu(customer_id)
    elif choice == "2":
        viewRentedcars(customer_id)

def customer_menu(customer_id):
    print("\n--- CUSTOMER BOOKING ---")

    try:
        response = requests.get(f"{API_BASE}/cars/available")

        if response.status_code != 200:
            print("Could not fetch available cars.")
            return

        data = response.json()
        cars = data.get("cars", [])

        if not cars:
            print("No cars currently available.")
            return
        print(f"\nAvailable Cars: {len(cars)}")
        for car in cars:
            print(f"[ID: {car['car_id']}] {car['car_name']} ({car['car_type']}) - ${car['price']}")

        book_id = input("\nEnter Car ID to book (or press Enter to cancel): ").strip()
        if not book_id:
            print("Cancelled.")
            return
        
        res = requests.post(
            f"{API_BASE}/cars/{book_id}/book/",
            params={"customer_id": customer_id}  
        )

        if res.status_code == 200:
            print("\n Car booked!")
        else:
            print("error:", res.json().get("detail"))

    except Exception as e:
        print("Error:", str(e))



def viewRentedcars(customer_id):
    try:
        response = requests.get(f"{API_BASE}/customers/{customer_id}/bookings")
        data = response.json()

        if "cars" not in data or len(data["cars"]) == 0:
            print("You have not rented any cars yet.")
            return

        print(f"\nYou rented {len(data['cars'])} cars:\n")
        for car in data["cars"]:
            print(f"[ID: {car['car_id']}] {car['car_name']} ({car['car_type']}) - ${car['price']} - Status: {car['status']}")
    except Exception as e:
        print("Error:", e)

def menu():
    print("\n==============================")
    print("   API FUNCTION CONSOLE MENU  ")
    print("==============================")
    print("1. Admin ")
    print("2. Customer ")
    print("3. Exit")
    print("===============================")


def main():
    while True:
        menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            askAdmin()
        elif choice == "2":
            #add_customer()
            customer_panel()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 3.")


if __name__ == "__main__":
    main()
