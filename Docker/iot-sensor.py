import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import json
import random
from datetime import datetime  

# Read environment variables
IOT_HUB_NAME = os.getenv('IOT_HUB_NAME')
DEVICE_ID = os.getenv('DEVICE_ID')
SHARED_ACCESS_KEY = os.getenv('SHARED_ACCESS_KEY')

# Construct the IoT Hub connection string using the environment variables
CONNECTION_STRING = f"HostName={IOT_HUB_NAME}.azure-devices.net;DeviceId={DEVICE_ID};SharedAccessKey={SHARED_ACCESS_KEY}"

async def main():
    # Create instance of the device client using the authentication provider
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # Connect the device client.
    await device_client.connect()

    # Send telemetry data in a loop
    try:
        while True:
            # Simulate telemetry data
            telemetry_data = {
                "temperature": random.uniform(20, 25),  # Replace with real sensor data
                "humidity": random.uniform(40, 60),     # Replace with real sensor data
                "pressure": random.uniform(950, 1050),  # Hypothetical air pressure in hPa
                "altitude": random.uniform(100, 120),   # Hypothetical altitude in meters
                "luminosity": random.uniform(100, 300), # Hypothetical luminosity in lux
                "motion": random.choice([True, False]), # Hypothetical motion sensor (True/False)
                "battery_level": random.uniform(0, 100) # Hypothetical battery level in percent
            }
            # Add a timestamp to the telemetry data (ISO 8601 format)  
            telemetry_data["timestamp"] = datetime.utcnow().isoformat() + "Z"  

            message = Message(json.dumps(telemetry_data))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"
            
            # Send the message
            print(f"Sending message: {message}")
            await device_client.send_message(message)
            print("Message successfully sent!")

            # Wait for a short period before sending the next telemetry data
            await asyncio.sleep(5)  # Interval in seconds between messages
            
    except KeyboardInterrupt:  
        print("Telemetry loop stopped by user")  
    finally:  
        # Ensure the device client is properly shut down  
        if device_client:  
            await device_client.shutdown() 

if __name__ == "__main__":
    asyncio.run(main())
