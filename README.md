# fabric-iot
Repo to sample iot data in Microsoft Fabric

I. Create Azure resources
1. Create Azure IoT hub
2. Create Iot with symmetric key auth
3. Note the Hub name, device name and Device key

II. Configure IoT hub
1. In the Routes section create a route for the builtin endpoint for the device telemtry messages
2. In the 

II. Create a Docker container for the sensor simulator
1. create an image from the python code in the Docker folder
2. Make sure to populate the .env file with your IoT Hub and device data to connect to IoT hub
3. Run a Docker container instance and make sure messages are succesfully sent to IoT hub

III. Configure IoT 