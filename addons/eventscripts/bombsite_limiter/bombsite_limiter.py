import es
import gamethread
import playerlib
import random
import usermsg
import vecmath

info = es.AddonInfo() 
info.name = 'Bombsite Limiter' 
info.version = '1.0.4' 
info.url = 'http://forums.mattie.info/cs/forums/viewtopic.php?t=23340' 
info.basename = 'bombsite_limiter' 
info.author = 'Sc0pE'
################################################
# Do not edit above this line 
# This script will enforce players to plant at the Default site only when there are a certain
# number of CT's playing or less
################################################
# Configs:

# Maximum number of CT's alive to initiate the DEFAULT site only bomb punishments
cts = 2

# Add  your map on an new line with the same syntax as the others
# If you don't add your map, the default site letter will be A
maplist = {
    #' map name      '( Default site Letter)
    'de_dust2':'A',
    'de_dust':'B',
    'de_aztec':'A',
    'de_cbble':'A',
    'de_chateau':'A',
    'de_inferno':'B',
    'de_nuke':'A',
    'de_piranesi':'A',
    'de_port':'A',
    'de_prodigy':'A',
    'de_russka':'A',
    'de_tides':'A',
    'de_train':'A',
    'de_cpl_mill':'A',
    'de_cpl_strike':'A',
    }
################################################
# Do not edit below this line unless you have read how to change / add a default map
# above ^^
################################################
active = 0
checksites = 0
bombsitesNum = {}
mapsites = {}
coords = []
mapname = 'None'

def load():
    global checksites
    global mapname
    es.set('bombsite_limiter_ver', '1.0.4')
    es.makepublic('bombsite_limiter_ver')
    es.msg('#multi', '#green[#lightgreenBombsite#green-#lightgreenLimiter#lightgreen]#default Loaded...')
    for map in maplist:
        mapsites[map] = bombsites(map, maplist[map])
    mapname = es.getString('eventscripts_currentmap')
    try:
        for userid in es.getUseridList():
            siteCheck()
            if len(bombsitesNum) >= 1:
                gamethread.delayed(0.5, mapsites[mapname].announce, (userid))
            else:
                checksites = 1
    except KeyError:
        mapsites[mapname] = bombsites(mapname, 'A')
        for userid in es.getUseridList():
            gamethread.delayed(0.5, mapsites[mapname].announce, (userid))

def unload():
    es.msg('#multi', '#green[#lightgreenBombsite#green-#lightgreenLimiter#lightgreen]#default Unloaded...')

def es_map_start(ev):
    global checksites, coords
    coords = []
    checksites = 1

def siteCheck():
    bombsitesNum.clear()
    managerindex = es.getentityindex('cs_player_manager')
    if managerindex > 0:
        index = getSiteIndex(vecmath.vector(es.getindexprop(managerindex, 'CCSPlayerResource.m_bombsiteCenterA')))
        if index:
            bombsitesNum['A'] = index
        index = getSiteIndex(vecmath.vector(es.getindexprop(managerindex, 'CCSPlayerResource.m_bombsiteCenterB')))
        if index:
            bombsitesNum['B'] = index

def getSiteIndex(centerpos):
    for index in es.createentitylist('func_bomb_target'):
        current_min = vecmath.vector(es.getindexprop(index, 'CBaseEntity.m_Collision.m_vecMins'))
        current_max = vecmath.vector(es.getindexprop(index, 'CBaseEntity.m_Collision.m_vecMaxs'))
        if vecmath.isbetweenRect(centerpos, current_min, current_max):
             return index
    return 0

def round_start(ev):
    global mapname
    mapname = es.getString('eventscripts_currentmap')

def player_spawn(ev):
    global checksites, coords
    userid = ev['userid']
    try:
        if not checksites:
            mapsites[mapname].announce(userid)
        else:
            if es.getplayersteamid(userid) != 'BOT':
                siteCheck()
                gamethread.delayed(0.5, mapsites[mapname].announce, (userid))
                checksites = 0
    except KeyError:
        mapsites[mapname] = bombsites(mapname, 'A')
        mapsites[mapname].announce(userid)
    if es.getplayerteam(ev['userid']) == 3:
        if not es.getplayerlocation(ev['userid']) in coords:
            coords.append(es.getplayerlocation(ev['userid']))

def bomb_beginplant(ev):
    userid = ev['userid']
    mapname = es.getString('eventscripts_currentmap')
    mapsites[mapname].plant(userid, int(ev['site']), mapname)

class bombsites(object):
    def __init__(self, mapname=None, defaultSiteLetter=None,):
        self.mapname           = mapname
        self.defaultSiteLetter = defaultSiteLetter

    def announce(self, userid):
        global active
        if es.getlivingplayercount(3) <= cts:
            if len(bombsitesNum) >= 1:
                active = 1
                if playerlib.getPlayer(userid).attributes['teamid'] == 2:
                    es.tell(userid, '#multi', '#green[#lightgreenBombsite#green-#lightgreenLimiter#lightgreen]#default Due to the low number of CT\'s this round, you must #lightgreenonly plant at site #green%s#lightgreen!'%self.defaultSiteLetter)
                    gamethread.delayed(1, es.tell, (userid, '#multi', '#green[#lightgreenBombsite#green-#lightgreenLimiter#lightgreen]#default Due to the low number of CT\'s this round, you must #lightgreenonly plant at site #green%s#lightgreen!'%self.defaultSiteLetter))
                    es.centertell(userid, 'You must only plant at %s site!'%self.defaultSiteLetter)
                    gamethread.delayed(1, es.centertell, (userid, 'You must only plant at %s site!'%self.defaultSiteLetter))
                    gamethread.delayed(2, es.centertell, (userid, 'You must only plant at %s site!'%self.defaultSiteLetter))
                    gamethread.delayed(3, es.centertell, (userid, 'You must only plant at %s site!'%self.defaultSiteLetter))
                elif playerlib.getPlayer(userid).attributes['teamid'] == 3:
                    es.tell(userid, '#multi', '#green[#lightgreenBombsite#green-#lightgreenLimiter#lightgreen]#default Due to the low number of CT\'s this round, you must #lightgreenonly protect site #green%s#lightgreen!'%self.defaultSiteLetter)
                    gamethread.delayed(1, es.tell, (userid, '#multi', '#green[#lightgreenBombsite#green-#lightgreenLimiter#lightgreen]#default Due to the low number of CT\'s this round, you must #lightgreenonly protect site #green%s#lightgreen!'%self.defaultSiteLetter))
                    es.centertell(userid, 'You must only protect %s site!'%self.defaultSiteLetter)
                    gamethread.delayed(1, es.centertell, (userid, 'You must only protect %s site!'%self.defaultSiteLetter))
                    gamethread.delayed(2, es.centertell, (userid, 'You must only protect %s site!'%self.defaultSiteLetter))
                    gamethread.delayed(3, es.centertell, (userid, 'You must only protect %s site!'%self.defaultSiteLetter))
        else:
            active = 0

    def plant(self, userid, site, mapname):
        if active:
            if site != bombsitesNum[self.defaultSiteLetter]:
                if es.getplayersteamid(userid) != 'BOT':
                    playerlib.getPlayer(userid).set("push", (0, 300, 1))
                    es.tell(userid, '#multi', '#green[#lightgreenBombsite#green-#lightgreenLimiter#lightgreen]#default Due to the low number of CT\'s this round, you must #lightgreenonly plant at site #green%s#lightgreen!'%self.defaultSiteLetter)
                    es.centertell(userid, 'You must only plant at %s site!'%self.defaultSiteLetter)
                    gamethread.delayed(1, es.centertell, (userid, 'You must only plant at %s site!'%self.defaultSiteLetter))
                else:
                    x, y, z = random.choice(coords)
                    es.server.queuecmd('es_xsetpos %s %s %s %s'%(userid, x, y, z))
                    es.msg('#multi','#green[#lightgreenBombsite#green-#lightgreenLimiter#green]#lightgreen %s #defaultwas teleported for planting at the wrong bombsite and being a bot!' % es.getplayername(userid))