

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.recent_kill_event = 0
        self.recent_death_event = 0
        
    def set_recent_kill(self, event_id):
        self.recent_kill_event = event_id
    def get_recent_kill(self):
        return self.recent_kill_event
    def set_recent_death(self, event_id):
        self.recent_death_event = event_id
    def get_recent_death(self):
        return self.recent_death_event
    def get_player_id(self):
        return self.player_id
 

class PlayerManager:
    def __init__(self):
        self.players ={}
        
    def get_or_create_player(self, player_id):
        if player_id not in self.players:
            self.players[player_id] = Player(player_id)
        
        return self.players[player_id]
    
    def count(self):
        return len(self.players)