import models.player_manager

def event_compair (guild, player_id, recent_kill_list= None, recent_death_list= None, event_list = None):
    player = guild.get_player(player_id)
    
    
    def update_event_list(recent_list, get_recent_event, set_recent_event):
        stored_event = get_recent_event()
        if recent_list:
            for event in recent_list:
                if event['EventId'] == stored_event:
                    #this means they've gotten an assit:
                    #TODO: battle reports, exmaple api call: 
                    #https://gameinfo.albiononline.com/api/gameinfo/battles?range=week&offset=0&limit=4&sort=recent&guildId=8IGjgklLRE2Bvqof6ABfnw
                    break
                event_list.append(event['EventId'])
            if recent_list[0]['EventId'] != stored_event:
                set_recent_event(recent_list[0]['EventId'])

    if recent_kill_list:
        update_event_list(recent_kill_list, player.get_recent_kill, player.set_recent_kill)

    if recent_death_list:
        update_event_list(recent_death_list, player.get_recent_death, player.set_recent_death)

    return event_list
      

