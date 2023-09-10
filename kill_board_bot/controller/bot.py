import discord
import view.utils
import controller.network_requests
import models.player_manager
from discord.ext import tasks, commands

guild_list =[]
player_manager = models.player_manager.PlayerManager()



def run_discord_bot():
    TOKEN = 'MTE0OTg2NDYyNTk0OTY1NTA0MA.GVvLkq.B8xT89PGx0Th-mhpVC6FBXFIuLNAK7Rg6gAOko'
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
 


    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!' )



    @bot.command()
    async def addguild(ctx, *, guild_name):  # Using * to capture the entire message as a single argument
        
        #TODO:initilize player objects to their current kill, therfor not bombing a discord the first time it is run
        if guild_name not in guild_list:
            guild_list.append(guild_name)
            try:
                guild_id= await controller.network_requests.inti_guild_id(guild_name)
                player_id_list = await controller.network_requests.get_player_id([guild_id])
                recent_kills_list = await controller.network_requests.get_recent_kills(player_id_list, player_manager)
                recent_deaths_list = await controller.network_requests.get_recent_deaths(player_id_list, player_manager)
                print('Number of players in the guild:')
                print(player_manager.count())
                await ctx.send(f"Guild '{guild_name}' added successfully!")
            except ValueError:
                await ctx.send(f'There is no Guild by this name')
        else:
            await ctx.send(f"Guild '{guild_name}' is already in the list!")
       
        
                


    @bot.command()
    async def recentkills(ctx):
        #print (f'message from user: {ctx.message}')
        channel = ctx.channel
            #make list of guild uids
        guild_id_list = await controller.network_requests.get_guild_id(guild_list)
            #make list of player uids
        player_id_list = await controller.network_requests.get_player_id(guild_id_list)
            #make a list of recent kill events
        recent_kills_list = await controller.network_requests.get_recent_kills(player_id_list, player_manager)
            #make a list of recent death events
        recent_deaths_list = await controller.network_requests.get_recent_deaths(player_id_list, player_manager)
        
        
        await view.utils.render_kills(recent_kills_list,channel)

    @bot.command()
    async def ping(ctx):
        print('im here')
        await ctx.send('pong')

    bot.run(TOKEN)
