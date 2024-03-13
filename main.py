import asyncio
import requests
from dotenv import load_dotenv
from datetime import datetime
import os

from pywizlight import wizlight, PilotBuilder, discovery

load_dotenv()

API_ENDPOINT = "http://" + str(os.getenv('SERVER_HOST_URL')) + "/meters"

measurement_delay = int(os.getenv('MEASUREMENT_DELAY'))
discover_delay = int(os.getenv('DISCOVER_DELAY'))
ready_to_discover = True

async def main():
   await discover_bulbs()

   while True:
      for i in range(1, discover_delay//measurement_delay):
         await asyncio.sleep(measurement_delay)
         await measure(bulbs, API_ENDPOINT)  
      await discover_bulbs()
   
async def discover_bulbs():
   #update bulbs list
   print("Discovering bulbs")
   global bulbs
   bulbs = await discovery.discover_lights(broadcast_space="10.10.255.255")

async def measure(bulbs, api_endpoint):
   print()
   print("Measuring bulbs")
   for bulb in bulbs:
      try :
         await send_data(bulb, api_endpoint)
      except :
         print("Error sending data")
         pass

async def send_data(bulb, api_endpoint):
   print("Sending data")
   #timestamp in iso format
   timestamp = datetime.now().isoformat()
   bulb_power = await bulb.get_power()
   data = {
      'bulpMac': str(bulb.mac),
      'wattage': bulb_power,
      'timestamp': timestamp
   }
   r = await requests.post(url = api_endpoint, json = data)
      
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
