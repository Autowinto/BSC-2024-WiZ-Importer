import asyncio

from pywizlight import wizlight, PilotBuilder, discovery

async def main():

    bulbs = await discovery.discover_lights(broadcast_space="10.10.255.255")

    for bulb in bulbs:
      print(await bulb.getUserConfig())
      print("Current Power Usage for " + str(bulb.ip) + " "  + str(await bulb.get_power()))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())