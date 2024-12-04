# 327Assignment8Group46

Nay Oo & Carter Murray

The project was collaboratively developed using **Replit**, an online IDE that allowed us to share and test the code in real time.


## Prerequisites
- Python 3.x

Required Python Libraries:
pip install pymongo


To Run this project as a server  

1. Save the provided Python script (iot_server_client.py)
2.Open a terminal and navigate to the directory where the script is saved.
Run the following command: python iot_server_client.py
When prompted "Do you want to run as a (s)erver or (c)lient? " choose s to start the server: S
Enter server IP address: localhost
Enter server port: 5000
3. The server will now listen for incoming client connections.

For Client 
1. Open a new terminal and navigate to the same directory.
2. Run the following command: python iot_server_client.py
3. When prompted "Do you want to run as a (s)erver or (c)lient? " choose c to start the server: c
4. Please enter the server's IP address: localhost
5. Please enter the server's port: 5000
       Choose from the valid query options:
		1: Average moisture inside the Smart Fridge in the past three hours.
		2: Average water consumption per cycle in the Dishwasher.
		3: IoT device with the highest electricity consumption.
Type the query number (e.g., 1) and press Enter to see the result.
