import controller.network_requests
import controller.data_processing
import models.player_manager

async def build_guild_manager(guild_id):

    #First get api for all member list
    
    member_info = await controller.network_requests.get_guild_members(guild_id)
    
    #make a manager for this guild
    guild_manager = models.player_manager.GuildManager(guild_id)
    
    #for each member, create the player object using the guild_manager, with the id, kill fame, and death fame
    for member in member_info:
        player_id = member['Id']
        print(player_id)
        player_killfame = member['KillFame']
        player_deathfame = member['DeathFame']
        

        #use all the info we gathered to create the player and assign them to the guild
        await guild_manager.create_player(player_id, player_killfame, player_deathfame)


    return guild_manager

async def get_recent_events(guild_manager_list):
    event_list = []
    
    #for each guild, check their member list, and compair the current fame to the 
    for guild in guild_manager_list:
        
        guild_id = guild.get_guild_id()
        guild_data = await controller.network_requests.get_guild_members(guild_id)
        
        for member in guild_data:
            player_id = member['Id']
            kill_fame = member['KillFame']
            death_fame = member['DeathFame']
            
            #return: An integer code indicating the status of fame updates:
            #     0 - No changes in fame stats.
            #     1 - Both kill and death fame have been updated.
            #     2 - Only kill fame has been updated.
            #     3 - Only death fame has been updated.
            event_status = await  guild.check_player_fame(player_id, kill_fame, death_fame)
            print(event_status)
            if event_status == 0:
                continue
            elif event_status == 1:
                kill_data = await controller.network_requests.get_player_kills(player_id)
                death_data = await controller.network_requests.get_player_deaths(player_id)
                controller.data_processing.event_compair(guild, player_id, kill_data, death_data, event_list)
            elif event_status == 2:
                kill_data = await controller.network_requests.get_player_kills(player_id)
                controller.data_processing.event_compair(guild, player_id, kill_data, None, event_list)
            elif event_status == 3:
                death_data = await controller.network_requests.get_player_deaths(player_id)
                controller.data_processing.event_compair(guild, player_id, None, death_data, event_list)
                
    return event_list    

async def inti_guild_id(guild_name, guild_manager_list):
    guild_search =  await controller.network_requests.search_guild(guild_name)

    for guild_data in guild_search['guilds']:
        if guild_data['Name'] == guild_name:

            #TODO:when init a guild make a guild object, filled with player objects.
            guild_manager = await build_guild_manager(guild_data['Id'])
            guild_manager_list.append(guild_manager)
            return guild_manager_list


    raise ValueError("There is no guild by this name")