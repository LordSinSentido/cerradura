from dotenv import load_dotenv
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
import threading as th
import json
import os
import asyncio


async def Main():
    client = IoTHubDeviceClient.create_from_connection_string(os.environ['CONNECTION_STRING'])
    await client.connect()

    def message_received_handler(message):
        data = json.loads(message.data)
        print(data['message'])


    async def method_request_handler(method_request):
        if method_request.name == "open_gate":
            payload = {"result": True, "data": "some data"}  # set response payload
            status = 200  # set return status code
            print("executed method1")
            print(method_request)
            print("")
        elif method_request.name == "close_gate":
            pass
        else:
            pass
        
        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        await client.send_method_response(method_response)
    

    def stdin_listener():
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                print("Quitting...")
                break

    client.on_message_received = message_received_handler
    client.on_method_request_received = method_request_handler

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for messages
    await user_finished

    # Finally, shut down the client
    await client.shutdown()


if __name__ == '__main__':
    try:
        load_dotenv()
        asyncio.run(Main())
    except KeyboardInterrupt:
        print("Saliendo")
    finally:
        print("El programa ha sido detenido")
