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
            print(f"{'ID':<5} {'Name':<20} {'Type':<15} {'Price':<10} {'Status'}")
            print("-" * 65)
            for car in cars:
                print(
                    f"{car['car_id']:<5} {car['car_name']:<20} {car['car_type']:<15} {car['price']:<10} {car['status']}")
            print("-" * 65)
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

        if not name or not ctype or not price:
            print("All fields are required!")
            return

        payload = {
            "car_name": name,
            "car_type": ctype,
            "price": price
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


def customer_menu():
    print("\n--- CUSTOMER BOOKING ---")

    try:
        response = requests.get(f"{API_BASE}/cars/available")
        if response.status_code == 200:
            data = response.json()
            cars = data.get("cars", [])

            if not cars:
                print("No cars currently available.")
                return

            print(f"\nAvailable Cars: {len(cars)}")
            for car in cars:
                print(f"[ID: {car['car_id']}] {car['car_name']} ({car['car_type']}) - ${car['price']}/day")

            book_id = input("\nEnter Car ID to book (or press Enter to cancel): ")
            if book_id:
                res = requests.post(f"{API_BASE}/cars/{book_id}/book")
                if res.status_code == 200:
                    print(f"SUCCESS: You have booked the car!")
                else:
                    print(f"Failed: {res.json().get('detail')}")
        else:
            print("Could not fetch available cars.")
    except Exception as e:
        print("Error:", e)


# def call_square_root():
#     try:
#         value = int(input("Enter an integer: "))
#         response = requests.get(f"{API_BASE}/sqrt", params={"value": value})
#         result = response.json()   # Convert API response to dict automatically
#         print("\nResponse:", result)
#         print("\nResponse input:", result['input'])
#         print("\nResponse square_root:", result['square_root'])
#     except Exception as e:
#         print("Error:", e)

# def call_range_sum():
#     try:
#         from_param = int(input("Enter from_param: "))
#         to_param = int(input("Enter to_param: "))
#         response = requests.get(f"{API_BASE}/range_sum", params={"from_param": from_param, "to_param": to_param})
#         result = response.json()
#         print("\nResponse:", result)
#         print("\nResponse from:", result['from'])
#         print("\nResponse to:", result['to'])
#         print("\nResponse sum:", result['sum'])
#     except Exception as e:
#         print("Error:", e)

# def call_process_dict1():
#     try:
#         data = {}
#         data["name"] = input("Enter your name: ")
#         data["age"] = input("Enter your age: ")
#
#         payload = {"data": data}
#         response = requests.post(f"{API_BASE}/process_dict1", json=payload)
#         result = response.json()
#
#         print("\nResponse:", result)
#         print("\nResponse name:", result['received_data']['data']['name'])
#         print("\nResponse age:", result['received_data']['data']['age'])
#     except Exception as e:
#         print("Error:", e)
#
# def call_process_dict2():
#     try:
#         data = {}
#         data["name"] = input("Enter your name: ")
#         data["age"] = input("Enter your age: ")
#
#         payload = {"data": data}
#         response = requests.post(f"{API_BASE}/process_dict2", json=payload)
#         result = response.json()
#
#         print("\nResponse:", result)
#         print("\nResponse name:", result['received_data']['name'])
#         print("\nResponse age:", result['received_data']['age'])
#     except Exception as e:
#         print("Error:", e)

def menu():
    print("\n==============================")
    print("   API FUNCTION CONSOLE MENU  ")
    print("==============================")
    print("1. Admin ")
    print("2. Customer ")
    print("3. Exit")
    print("==============================")


def main():
    while True:
        menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            askAdmin()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 3.")


if __name__ == "__main__":
    main()
