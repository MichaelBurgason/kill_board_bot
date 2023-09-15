import aiohttp
import io

async def async_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.headers.get("Content-Type") == "application/json":
                return await resp.json()
            elif "image/png" in resp.headers.get("Content-Type"):
                image_data = await resp.read()
                return io.BytesIO(image_data)  # Return bytes-like object for the image
            else:
                raise ValueError("Unsupported Content-Type")

async def get_guild_members(guild_id):
        guild_member_endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/guilds/{guild_id}/members'
        guild_data = await async_request(guild_member_endpoint)
        print(f'https://gameinfo.albiononline.com/api/gameinfo/guilds/{guild_id}/members')
        return guild_data

async def get_player_kills(player_id):
        kills_endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/players/{player_id}/kills'
        recent_kill_events = await async_request(kills_endpoint)
        print (f'https://gameinfo.albiononline.com/api/gameinfo/players/{player_id}/kills')
        return recent_kill_events

async def get_player_deaths(player_id):
        deaths_endpoint =f'https://gameinfo.albiononline.com/api/gameinfo/players/{player_id}/deaths'
        recent_deaths_events = await async_request(deaths_endpoint)
        print (f'https://gameinfo.albiononline.com/api/gameinfo/players/{player_id}/deaths')
        return recent_deaths_events

async def search_guild(guild_name):
        guild_search_endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/search?q={guild_name}'
        guild_search =  await async_request(guild_search_endpoint) 
        return guild_search

async def get_item_image(item_id):
      item_render_endpoint =f'https://render.albiononline.com/v1/item/{item_id}&size=120'
      image = await async_request(item_render_endpoint)
      return image



    

