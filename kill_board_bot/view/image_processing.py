import discord
import io
import controller.network_requests
from PIL import Image, ImageFont, ImageDraw

def determine_position_based_on_key_killer(key):
    # Define this function to return the (x, y) position where you want to paste the image based on the key
    positions = {
        "MainHand": (131, 407),
        "OffHand": (387, 407),
        "Head": (259, 295),
        "Armor": (259, 407),
        "Shoes": (259, 521),
        "Bag": (105, 283),
        "Cape": (413, 283),
        "Mount": (259, 631),
        "Potion": (105, 534),
        "Food": (413, 534),
    }
    return positions.get(key, (0, 0))  # Default position is (0, 0) if the key is not found

def determine_position_based_on_key_victim(key):
    # Define this function to return the (x, y) position where you want to paste the image based on the key
    positions = {
        "MainHand": (743, 407),
        "OffHand": (999, 407),
        "Head": (871, 295),
        "Armor": (871, 407),
        "Shoes": (871, 516),
        "Bag": (717, 283),
        "Cape": (1025, 283),
        "Mount": (871, 632),
        "Potion": (717, 534),
        "Food": (1025, 534),
    }
    return positions.get(key, (0, 0))  # Default position is (0, 0) if the key is not found









async def render_killer(event_data, background):
      for key, value in event_data['Killer']['Equipment'].items():
            if value:
                # Fetch the equipment image
                equipment_image = await controller.network_requests.get_item_image(f"{value['Type']}?Count={value['Count']}Quality={value['Quality']}")

                # Convert BytesIO stream to Image object
                equipment_image = Image.open(equipment_image)

                # Determine the position to paste (this part can be adjusted based on your needs)
                x, y = determine_position_based_on_key_killer(key)

                # Paste the equipment image onto the background
                background.paste(equipment_image, (x, y), equipment_image)  # Using the equipment image as a mask for transparency
      
      return background

async def render_victim(event_data, background):
      for key, value in event_data['Victim']['Equipment'].items():
            if value:
                # Fetch the equipment image
                equipment_image = await controller.network_requests.get_item_image(f"{value['Type']}?Count={value['Count']}Quality={value['Quality']}")

                # Convert BytesIO stream to Image object
                equipment_image = Image.open(equipment_image)

                # Determine the position to paste (this part can be adjusted based on your needs)
                x, y = determine_position_based_on_key_victim(key)

                # Paste the equipment image onto the background
                background.paste(equipment_image, (x, y), equipment_image)  # Using the equipment image as a mask for transparency
      return background


def center_text(center_position, text_width, text_height):
    start_position = (
        center_position[0] - text_width / 2,
        center_position[1] - text_height / 2
    )
    return start_position

def render_text(event_data, background, font ):

    draw = ImageDraw.Draw(background)
    

    # Calculate fame width and height
    font = font.font_variant(size=30)
    fame_width, fame_height = draw.textsize(str(event_data['Killer']['KillFame']), font=font)
    # Calculate start position based on desired center position
    fame_position = center_text([620,385],fame_width, fame_height)
    draw.text(fame_position, str(event_data['Killer']['KillFame']), font=font, fill='black')
    
    #TODO::Silver amount determination


        # Calculate fame width and height
    font = font.font_variant(size=45)
    # Calculate start position based on desired center position
    draw.text([240,180], str(event_data['Killer']['Name']), font=font, fill='black')
    draw.text([850,180], str(event_data['Victim']['Name']), font=font, fill='black')
    font = font.font_variant(size=30)
    draw.text([580,700], 'Killed!', font=font, fill='black')
    return background



async def render_events(event_list, channel):
    for event_id in event_list:
        endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/events/{event_id}'
        event_data = await controller.network_requests.async_request(endpoint)

        # Open the background image
        background = Image.open('gear_base.png').copy()  # Use copy() to avoid altering the original
        font = ImageFont.truetype('albion_font.ttf', 20)
     
        

        await render_killer(event_data, background)
        await render_victim(event_data, background)
        render_text(event_data, background, font)



        # Save the final composite image to an in-memory stream
        final_image_stream = io.BytesIO()
        background.save(final_image_stream, format="PNG")
        final_image_stream.seek(0)  # Important: Reset stream position to the beginning

        # Post the image to Discord
        await channel.send(file=discord.File(final_image_stream, "composite_image.png"))
  

