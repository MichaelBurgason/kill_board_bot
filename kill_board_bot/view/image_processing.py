import discord
import io
import controller.network_requests
from PIL import Image

def determine_position_based_on_key(key):
    # Define this function to return the (x, y) position where you want to paste the image based on the key
    # As an example:
    positions = {
        "MainHand": (131, 248),
        "OffHand": (387, 248),
        "Head": (259, 136),
        "Armor": (259, 248),
        "Shoes": (259, 362),
        "Bag": (105, 124),
        "Cape": (413, 124),
        "Mount": (259, 472),
        "Potion": (105, 375),
        "Food": (413, 375),
    }
    return positions.get(key, (0, 0))  # Default position is (0, 0) if the key is not found



async def render_events(event_list, channel):
    for event_id in event_list:
        endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/events/{event_id}'
        event_data = await controller.network_requests.async_request(endpoint)

        # Open the background image
        background = Image.open('gear_base.png').copy()  # Use copy() to avoid altering the original

        for key, value in event_data['Killer']['Equipment'].items():
            if value:
                # Fetch the equipment image
                equipment_image = await controller.network_requests.get_item_image(f"{value['Type']}?Count={value['Count']}Quality={value['Quality']}")

                # Convert BytesIO stream to Image object
                equipment_image = Image.open(equipment_image)

                # Determine the position to paste (this part can be adjusted based on your needs)
                x, y = determine_position_based_on_key(key)

                # Paste the equipment image onto the background
                background.paste(equipment_image, (x, y), equipment_image)  # Using the equipment image as a mask for transparency

        # Save the final composite image to an in-memory stream
        final_image_stream = io.BytesIO()
        background.save(final_image_stream, format="PNG")
        final_image_stream.seek(0)  # Important: Reset stream position to the beginning

        # Post the image to Discord
        await channel.send(file=discord.File(final_image_stream, "composite_image.png"))
  

