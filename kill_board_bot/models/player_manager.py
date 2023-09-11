
import controller.network_requests


class Player:
    """
    Represents a player in the game, including their ID, fame statistics, and recent events.

    :param player_id: Unique identifier for the player.
    :type player_id: str
    :param kill_fame: Player's kill fame score.
    :type kill_fame: int
    :param death_fame: Player's death fame score.
    :type death_fame: int
    :param recent_kill_event: ID of the player's most recent kill event.
    :type recent_kill_event: int
    :param recent_death_event: ID of the player's most recent death event.
    :type recent_death_event: int
    """
    def __init__(self, player_id, kill_fame, death_fame, recent_kill_event, recent_death_event):
        self.player_id = player_id
        self.kill_fame = kill_fame
        self.death_fame = death_fame
        self.recent_kill_event = recent_kill_event
        self.recent_death_event = recent_death_event
        
    def set_recent_kill(self, event_id):
        """
        Set the recent kill event ID for the player.

        :param event_id: Unique identifier for the kill event.
        :type event_id: int
        """
        self.recent_kill_event = event_id
    def get_recent_kill(self):
        """
        Retrieve the recent kill event ID for the player.

        :return: Recent kill event ID.
        :rtype: int
        """
        return self.recent_kill_event
    

    def set_recent_death(self, event_id):
        """
        Set the recent death event ID for the player.

        :param event_id: Unique identifier for the death event.
        :type event_id: int
        """
        self.recent_death_event = event_id
    def get_recent_death(self):
        """
        Retrieve the recent death event ID for the player.

        :return: Recent death event ID.
        :rtype: int
        """
        return self.recent_death_event
    
    def set_kill_fame(self, kill_fame):
        """
        Set the kill fame score for the player.

        :param kill_fame: Player's kill fame score.
        :type kill_fame: int
        """
        self.kill_fame = kill_fame
    def get_kill_fame(self):
        """
        Retrieve the kill fame score for the player.

        :return: Kill fame score.
        :rtype: int
        """
        return self.kill_fame
    
    def set_death_fame(self, death_fame):
        """
        Set the death fame score for the player.

        :param death_fame: Player's death fame score.
        :type death_fame: int
        """
        self.death_fame = death_fame    
    def get_death_fame(self):
        """
        Retrieve the death fame score for the player.

        :return: Death fame score.
        :rtype: int
        """
        return self.death_fame
        
    def get_player_id(self):
        """
        Retrieve the unique ID of the player.

        :return: Player's unique ID.
        :rtype: str
        """
        return self.player_id
 

class GuildManager:
    """
    A manager class to handle operations related to guild players.

    Attributes:
        guild_id (str): The ID of the guild.
        players (dict): A dictionary to store player objects, with player IDs as keys.
    """
    
    def __init__(self, guild_id):
        """
        Initialize the GuildManager with a given guild ID.

        :param guild_id: The ID of the guild.
        :type guild_id: str
        """
        self.guild_id = guild_id
        self.players ={}
        


    async def create_player(self, player_id, kill_fame, death_fame):
        """
        Create a new player object and add it to the manager.

        :param player_id: The ID of the player to create or retrieve.
        :type player_id: str
        :param kill_fame: The initial kill fame of the player.
        :type kill_fame: int
        :param death_fame: The initial death fame of the player.
        :type death_fame: int
        :return: none.
        :rtype: none.
        """
        if player_id not in self.players:
            #using player ID get recent kills and death event Id's, this is because 
            #fame will always be passed, but if a new guild memeber joins we will need to "load" them in
            #and we do not have that information passed

            player_recent_kill_event = None
            player_recent_death_event = None
            
            recent_kill_events = await controller.network_requests.get_player_kills(player_id)
            recent_death_events = await controller.network_requests.get_player_deaths(player_id)
            
            
            # Check if the list is not empty and if the 'EventId' key exists and has a value
            if recent_kill_events and 'EventId' in recent_kill_events[0] and recent_kill_events[0]['EventId']:
                player_recent_kill_event = recent_kill_events[0]['EventId']
    
            # Similarly for deaths
            if recent_death_events and 'EventId' in recent_death_events[0] and recent_death_events[0]['EventId']:
                player_recent_death_event = recent_death_events[0]['EventId']
            
            new_player = Player(player_id, kill_fame, death_fame, player_recent_kill_event, player_recent_death_event)
            self.players[player_id] = new_player
            
        return
        

    async def check_player_fame(self, player_id, kill_fame, death_fame):
        """
        Retrieve a player object based on the player ID, or create one if it does not exist.
        Then, it checks the stored fame stats against the provided stats, updates them if necessary,
        and returns a corresponding code to indicate which stats (if any) have changed.

        :param player_id: The ID of the player to retrieve or create.
        :type player_id: str
        :param kill_fame: The current kill fame of the player.
        :type kill_fame: int
        :param death_fame: The current death fame of the player.
        :type death_fame: int
        :return: An integer code indicating the status of fame updates:
                 0 - No changes in fame stats.
                 1 - Both kill and death fame have been updated.
                 2 - Only kill fame has been updated.
                 3 - Only death fame has been updated.
        :rtype: int
        """
        #if player is not created, create it, use the current info as its startign point (will not post kills before they joined the guild)
        if player_id not in self.players:
            await self.create_player(player_id, kill_fame, death_fame)
            
        #retreive store player kill and death fame.
        player = self.players[player_id]
        stored_kill_fame = player.get_kill_fame()
        stored_death_fame = player.get_death_fame()
        print(f'checking player {player_id}')
        
        #if neither have changed, return 0
        if stored_kill_fame == kill_fame and stored_death_fame == death_fame:
            return 0
        #if both have changed, update both, and return 1
        if stored_kill_fame != kill_fame and stored_death_fame != death_fame:
            player.set_kill_fame(kill_fame)
            player.set_death_fame(death_fame)
            return 1
        #if only kill fame has changed, update kill fame, and return 2
        if stored_kill_fame != kill_fame:
            player.set_kill_fame(kill_fame)
            return 2
        #if only death fame has changed, update death fame, and return 3
        if stored_death_fame != death_fame:
            player.set_death_fame(death_fame)
            return 3
            
    def get_player(self, player_id):
        return self.players[player_id]
    
    def get_guild_id(self):
        return self.guild_id
    
    
    def count(self):
        """
        Get the number of players managed by this GuildManager.

        :return: The number of players.
        :rtype: int
        """
        return len(self.players)