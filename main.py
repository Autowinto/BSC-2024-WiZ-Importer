import asyncio
import requests
from dotenv import load_dotenv
from datetime import datetime
import os

from pywizlight import wizlight, PilotBuilder, discovery

load_dotenv()

API_ENDPOINT = str(os.getenv('API_URL'))
if not API_ENDPOINT:
   print("API_URL not found")
   exit()

measurement_delay = int(os.getenv('MEASUREMENT_DELAY'))
discover_delay = int(os.getenv('DISCOVER_DELAY'))
ready_to_discover = True

async def main():
   print("Starting Wiz Importer")
   try:
      await discover_bulbs()
   except Exception as e:
      pass

   while True:
      for i in range(1, discover_delay//measurement_delay):
         await asyncio.sleep(measurement_delay)
         try:
            await measure(bulbs, API_ENDPOINT+"/measurements")  
         except Exception as e:
            pass
      try:
         await discover_bulbs()
      except Exception as e:
         pass

async def discover_bulbs():
   #update bulbs list
   print("Discovering bulbs")
   global bulbs
   bulbs = await discovery.discover_lights(broadcast_space="10.10.255.255")
   for bulb in bulbs:
      r = requests.post(url = API_ENDPOINT+"/smartPlugs", json = {'id': str(bulb.mac), 'name': str(bulb.mac)})
      #check error code
      if r.status_code == 200:
         print("Bulb already in database")
      elif r.status_code == 201:
         print("Bulb added to database")
      else:
         print("Error adding bulb to database")
         print(r.status_code)
         print(r.text)
         pass

async def measure(bulbs, api_endpoint):
   print()
   print("Measuring bulbs")
   for bulb in bulbs:
      try :
         await send_data(bulb, api_endpoint)
      except Exception as e:
         pass

async def send_data(bulb, api_endpoint):
   print("Sending data")
   #timestamp in iso format
   timestamp = datetime.now().isoformat()
   bulb_power = await bulb.get_power()
   data = {
      'smartPlugId': str(bulb.mac),
      'wattage': bulb_power,
      'timestamp': timestamp
   }
   r = requests.post(url = api_endpoint, json = data)
      
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
