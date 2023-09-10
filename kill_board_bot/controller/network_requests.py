import aiohttp
import requests
import models.player_manager


async def async_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def get_guild_id(guild_list):
    guild_id_list = []
    for guild_name in guild_list:
        endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/search?q={guild_name}'
        guild_info = await async_request(endpoint)
        
        # Extract the ID for the matching guild name
        for guild_data in guild_info['guilds']:
            if guild_data['Name'] == guild_name:
                guild_id_list.append(guild_data['Id'])
                break  # Exit the loop once we've found the guild to avoid appending multiple IDs
    return guild_id_list


async def get_player_id(guild_id_list):
    player_id_list = []    
    for guild_id in guild_id_list:
        endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/guilds/{guild_id}/members'
        member_info = await async_request(endpoint)
        
        for member in member_info:
            player_id = member['Id']
            player_id_list.append(player_id)
    return player_id_list


async def get_recent_kills(player_id_list, player_manager):
    recent_kill_list = []
    for ids in player_id_list:
        player = player_manager.get_or_create_player(ids)
        #TODO: optimize how many people we are checking, maybe try to see if they are online, or increese kill/deathfame (maybe total guild fame)
        endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/players/{player.get_player_id()}/kills'
        kill_data = await async_request(endpoint)
        
        last_known_kill_event_id = player.get_recent_kill()
        
        for event in kill_data:
            if event['EventId'] == last_known_kill_event_id:
                break
            recent_kill_list.append(event['EventId'])
        if kill_data and kill_data[0]['EventId'] != last_known_kill_event_id:
            player.set_recent_kill(kill_data[0]['EventId'])
            
    print('number of kills:', len(recent_kill_list))
    return recent_kill_list


async def get_recent_deaths(player_id_list, player_manager):
    recent_death_list = []
    for ids in player_id_list:
        player = player_manager.get_or_create_player(ids)
        endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/players/{player.get_player_id()}/deaths'
        death_data = await async_request(endpoint)
        
        last_known_death_event_id = player.get_recent_death()
        for event in death_data:
            if event['EventId'] == last_known_death_event_id:
                break
            recent_death_list.append(event['EventId'])
        if death_data and death_data[0]['EventId'] != last_known_death_event_id:
            player.set_recent_death(death_data[0]['EventId'])
            
    print('number of deaths:', len(recent_death_list))
    return recent_death_list  


async def inti_guild_id(guild_name):
    guild_id_list =[]
    endpoint = f'https://gameinfo.albiononline.com/api/gameinfo/search?q={guild_name}'
    guild_info =  await async_request(endpoint)

    for guild_data in guild_info['guilds']:
        if guild_data['Name'] == guild_name:
            
            #TODO:when init a guild make a guild object, filled with player objects.
            get_player_id() 




            return guild_data['Id']
    raise ValueError("There is no guild by this name")