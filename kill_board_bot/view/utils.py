import random
import discord
import requests
import json
import controller.network_requests
from PIL import Image


async def render_events(event_list, channel):
    # to this pass a list of event Id's
    for event_id in event_list:  # Simplified iteration
        endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/events/{event_id}'
        event_data = await controller.network_requests.async_request(endpoint)  # Using your async_request function
        
        
        # open the backround image
        backround = Image.open('gear_base.png')
        for key, value in event_data['Killer']['Equipment'].items():
            if value:
                print(value)
                image = await controller.network_requests.get_item_image(f"{value['Type']}?Count={value['Count']}Quality={value['Quality']}")
                await channel.send(file=discord.File(image, "image.png"))

