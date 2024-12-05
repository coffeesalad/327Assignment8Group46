import socket
import threading
from pymongo import MongoClient
from datetime import datetime, timedelta
#from pytz import timezone, utc

def db_connection():
    try:
        client = MongoClient("mongodb+srv://cmurray901:Mccade1102@327database.wv31l.mongodb.net/?retryWrites=true&w=majority&appName=327Database")
        db = client["test"]
        return db
    except Exception as e:
        print(f"error connecting to database: {e}")
        return None
        
"""
def convert_to_pst(utc_time):
    pacific = timezone('US/Pacific')
    utc_dt = utc.localize(utc_time)
    pst_dt = utc_dt.astimezone(pacific)
    return pst_dt
"""
    
def query_processes(query, db):
    try:
        if query == '1':
            fridgeObj = db.MongoData_metadata.find_one({"customAttributes.name": "Smart Fridge"})
            if not fridgeObj:
                return "Error: No metadata found for Smart Fridge."
            fridgeId = fridgeObj["assetUid"]

            three_hours_ago = datetime.utcnow() - timedelta(hours=3)
            data = db.MongoData_virtual.find({"payload.parent_asset_uid": fridgeId, "time": {"$gte": three_hours_ago}})
            if not data:
                return "Error: No recent data found for Smart Fridge."

            count = 0
            total = 0
            for item in data:
                count += 1
                total += float(item["payload"].get("FridgeMoisture", 0))

            if count == 0:
                return "Error: No valid moisture data in the past 3 hours."
            avg_moisture = total / count
            return f"Average moisture level over the last 3 hours: {round(avg_moisture, 1)}% Relative Humidity"

        elif query == '2':
            dishObj = db.MongoData_metadata.find_one({"customAttributes.name": "Dishwasher"})
            if not dishObj:
                return "Error: No metadata found for Dishwasher."
            dishId = dishObj["assetUid"]

            data = db.MongoData_virtual.find({"payload.parent_asset_uid": dishId})
            if not data:
                return "Error: No data found for Dishwasher."

            count = 0
            total = 0
            for item in data:
                count += 1
                total += float(item["payload"].get("DWWater", 0))

            if count == 0:
                return "Error: No valid water consumption data."
            avg_consumption = (total / count)
            return f"Average water consumption per cycle: {round(avg_consumption, 1)} gallons per cycle"

        elif query == '3':
            devices = [
                {"name": "Smart Fridge", "sensor": "FridgePower"},
                {"name": "Dishwasher", "sensor": "DWPower"},
                {"name": "Garage Fridge", "sensor": "GaragePower"}
            ]

            power_consumption = {}
            for device in devices:
                obj = db.MongoData_metadata.find_one({"customAttributes.name": device["name"]})
                if not obj:
                    return f"Error: No metadata found for {device['name']}."
                deviceId = obj["assetUid"]

                data = db.MongoData_virtual.find({"payload.parent_asset_uid": deviceId})
                total_power = 0
                for item in data:
                    total_power += float(item["payload"].get(device["sensor"], 0))
                if device["name"] == "Smart Fridge" or "Garage Fridge":
                    power_consumption[device["name"]] = total_power * 10
                else:
                    power_consumption[device["name"]] = total_power * 100

            highest_consumer = max(power_consumption, key=power_consumption.get)
            return f"Highest consumer: {highest_consumer} ({round(power_consumption[highest_consumer], 1)} Watts)"
        else:
            return "Invalid query. Valid queries: 1, 2, 3."
    except Exception as e:
        return f"Error processing query: {str(e)}"





def start_server():
    db = db_connection()

    host = input("Enter server IP address (e.g., '0.0.0.0' for all interfaces): ")
    port = int(input("Enter server port: "))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is up and running on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected to client {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, db)).start()

def handle_client(client_socket, db):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if data.lower() == "exit":
                print("Client disconnected.")
                break
            print(f"Received from client: {data}")
            response = query_processes(data, db)
            client_socket.sendall(response.encode())
    finally:
        client_socket.close()

def start_client():
    server_ip = input("Please enter the server's IP address: ")
    server_port = int(input("Please enter the server's port: "))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("Connected to the server.")

    valid_queries = {
        "1": "What is the average moisture inside my kitchen fridge in the past three hours?",
        "2": "What is the average water consumption per cycle in my smart dishwasher?",
        "3": "Which device consumed more electricity among my three IoT devices?",
    }
    try:
        while True:
            print("Valid queries:")
            for key, query in valid_queries.items():
                print(f"{key}: {query}")
            user_input = input("Enter query number (or type 'exit' to quit): ")
            if user_input.lower() == "exit":
                print("Exiting...")
                break
            if user_input not in valid_queries:
                print("Invalid input. Please try one of the valid queries.")
                continue
            client_socket.sendall(user_input.encode())
            response = client_socket.recv(1024).decode()
            print(f"Server's reply: {response}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    mode = input("Do you want to run as a (s)erver or (c)lient? ").strip().lower()
    if mode == "s":
        start_server()
    elif mode == "c":
        start_client()
    else:
        print("Invalid input. Please choose 's' for server or 'c' for client.")
