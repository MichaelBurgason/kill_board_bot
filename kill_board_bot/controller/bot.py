import discord
import view.image_processing
import controller.network_requests
import controller.guild_services
from discord.ext import tasks, commands

guild_list =[]
guild_manager_list = []



def run_discord_bot():
    #ADD TOKEN PATH HERE
    #TOKEN =
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
                await controller.guild_services.inti_guild_id(guild_name, guild_manager_list)
                await ctx.send(f"Guild '{guild_name}' added successfully!")
            except ValueError:
                await ctx.send(f'There is no Guild by this name')
        else:
            await ctx.send(f"Guild '{guild_name}' is already in the list!")
       
        
                


    @bot.command()
    async def recentkills(ctx):
        #print (f'message from user: {ctx.message}')
        channel = ctx.channel
        
        #event_list = await controller.guild_services.get_recent_events(guild_manager_list)
        event_list = [876724192]
        
        await view.image_processing.render_events(event_list,channel)

    @bot.command()
    async def renderkill(ctx):
        channel = ctx.channel
        eventlist = [872517931]
        await view.image_processing.render_events(eventlist,channel)
        

    @bot.command()
    async def ping(ctx):
        print('im here')
        await ctx.send('pong')

    bot.run(TOKEN)
