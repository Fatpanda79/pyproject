# ============================================
# api_client.py
# ============================================

import requests

API_BASE = "http://127.0.0.1:8000"  # Make sure API is running

def adminPanel():
    print("welcome to admin panel")

def askAdmin():
    try:
        password = input("type the password to access admin panel")
        if password == "admin123":
            adminPanel()
        else:
            print("the password is wrong try again")
            askAdmin()
    except Exception as e:
        print("Error:", e)

def call_square_root():
    try:
        value = int(input("Enter an integer: "))
        response = requests.get(f"{API_BASE}/sqrt", params={"value": value})
        result = response.json()   # Convert API response to dict automatically
        print("\nResponse:", result)
        print("\nResponse input:", result['input'])
        print("\nResponse square_root:", result['square_root'])
    except Exception as e:
        print("Error:", e)

def call_range_sum():
    try:
        from_param = int(input("Enter from_param: "))
        to_param = int(input("Enter to_param: "))
        response = requests.get(f"{API_BASE}/range_sum", params={"from_param": from_param, "to_param": to_param})
        result = response.json()
        print("\nResponse:", result)
        print("\nResponse from:", result['from'])
        print("\nResponse to:", result['to'])
        print("\nResponse sum:", result['sum'])
    except Exception as e:
        print("Error:", e)

def call_process_dict1():
    try:
        data = {}
        data["name"] = input("Enter your name: ")
        data["age"] = input("Enter your age: ")
        
        payload = {"data": data}
        response = requests.post(f"{API_BASE}/process_dict1", json=payload)
        result = response.json()
        
        print("\nResponse:", result)
        print("\nResponse name:", result['received_data']['data']['name'])
        print("\nResponse age:", result['received_data']['data']['age'])
    except Exception as e:
        print("Error:", e)

def call_process_dict2():
    try:
        data = {}
        data["name"] = input("Enter your name: ")
        data["age"] = input("Enter your age: ")
        
        payload = {"data": data}
        response = requests.post(f"{API_BASE}/process_dict2", json=payload)
        result = response.json()
        
        print("\nResponse:", result)
        print("\nResponse name:", result['received_data']['name'])
        print("\nResponse age:", result['received_data']['age'])
    except Exception as e:
        print("Error:", e)

def menu():
    print("\n==============================")
    print("   API FUNCTION CONSOLE MENU  ")
    print("==============================")
    print("1. Admin ")
    print("2. Customer ")
    print("5. Exit")
    print("==============================")

def main():
    while True:
        menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            askAdmin()
        elif choice == "2":
            call_range_sum()
        elif choice == "3":
            call_process_dict1()
        elif choice == "4":
            call_process_dict2()
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please choose between 1 and 4.")

if __name__ == "__main__":
    main()
