import os
from dotenv import load_dotenv
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import json
import random
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Read environment variables
IOT_HUB_NAME = os.getenv('IOT_HUB_NAME')
DEVICE_ID = os.getenv('DEVICE_ID')
SHARED_ACCESS_KEY = os.getenv('SHARED_ACCESS_KEY')

# Construct the IoT Hub connection string using the environment variables
CONNECTION_STRING = f"HostName={IOT_HUB_NAME}.azure-devices.net;DeviceId={DEVICE_ID};SharedAccessKey={SHARED_ACCESS_KEY}"

# Initialize the last_c2d_message variable
last_c2d_message = None


async def receive_c2d_message(device_client):
    global last_c2d_message
    print("Listening for C2D messages...")
    while True:
        c2d_message = await device_client.receive_message()
        data = c2d_message.data.decode('utf-8')
        print(f"Received C2D message: {data}")
        try:
            last_c2d_message = json.loads(data)  # Try parsing the message as JSON
        except json.JSONDecodeError:
            print(f"Error when receiving C2D message: Invalid JSON - {data}")
            # You can decide how to handle non-JSON messages here
            # For example, you could store them as plain text:
            last_c2d_message = data


async def main():
    # Create instance of the device client using the connection string
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # Connect the device client.
    await device_client.connect()

    # Start the C2D message listener as a background task
    c2d_message_listener_task = asyncio.create_task(receive_c2d_message(device_client))

    # Send telemetry data in a loop
    try:
        global last_c2d_message
        while True:
            telemetry_data = {
                "temperature": random.uniform(20, 25),
                "humidity": random.uniform(40, 60),
                "pressure": random.uniform(950, 1050),
                "altitude": random.uniform(100, 120),
                "luminosity": random.uniform(100, 300),
                "motion": random.choice([True, False]),
                "battery_level": random.uniform(0, 100)
            }
            telemetry_data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        # Handle the inclusion of the last received C2D message in the telemetry data  
            if last_c2d_message is not None:  
                if isinstance(last_c2d_message, str):  
                    telemetry_data["c2d_message"] = last_c2d_message  # Plain text message  
                else:  
                    telemetry_data["c2d_message"] = last_c2d_message  # JSON message  
            else:  
                telemetry_data["c2d_message"] = "No message received yet." 

            message = Message(json.dumps(telemetry_data))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            # Send the message
            print(f"Sending message: {message}")
            await device_client.send_message(message)
            print("Message successfully sent!")

            # Wait for a short period before sending the next telemetry data
            await asyncio.sleep(5)

    except KeyboardInterrupt:
        print("Telemetry loop stopped by user")
    finally:
        # Cancel the C2D message listener task before shutting down
        c2d_message_listener_task.cancel()
        if device_client:
            await device_client.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
