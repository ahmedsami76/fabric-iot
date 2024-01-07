# fabric-iot
Repo to sample iot data in Microsoft Fabric

I. Create Azure resources
1. Create Azure IoT hub
2. Create Iot with symmetric key auth
3. Note the Hub name, device name and Device key
4. create adls gen2 with a container name it "rawiot"

II. Configure IoT hub
1. In the Routes section create a route for the builtin endpoint for the device telemtry messages
2. In the Routes section create a route for the storage endpoint for the device telemtry messages sending to adlsgen2
3. create another consumer group called "fabric-streaming"

II. Create a Docker container for the sensor simulator
1. create an image from the python code in the Docker folder
2. Make sure to populate the .env file with your IoT Hub and device data to connect to IoT hub
3. Run a Docker container instance and make sure messages are succesfully sent to IoT hub

III. Configure IoT 