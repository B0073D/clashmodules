import sopel.module
import sopel.formatting
import time
import calendar
from threading import Timer
import urllib
import json


@sopel.module.commands('sm')
@sopel.module.example('!sm 45', '<username> cannot be healed for 45 minutes')
def notify_sm(bot, trigger):
    """Notifies once SM count (minutes) is over."""
    try:
        sm_count = int(trigger.group(2).rstrip(' '))
    except:
        bot.say('You need to specify minutes, eg !sm 10')
        return
    bot.say(trigger.nick + ' can\'t be healed for ' + str(sm_count) + ' minutes due to SM')

    Timer(sm_count * 60, bot.say, [trigger.nick + ' can now be healed!']).start()


@sopel.module.commands('ping')
@sopel.module.example('!ping <message>', 'channeluser1 channeluser2 <message>')
def notify_ping(bot, trigger):
    """Pings everyone in the channel and tells them a message"""
    if trigger.group(2) is None:
        bot.say('Usage: !ping <message>')
        return
    if trigger.sender[0] == '#':
        nicks_in_channel = ''
        for nick in bot.privileges[trigger.sender]:
            nicks_in_channel += nick + ' '
        bot.say(nicks_in_channel)
        bot.say(sopel.formatting.color(trigger.group(2), fg='YELLOW', bg='BLACK'))


@sopel.module.commands('nctime')
@sopel.module.example('!nctime', 'It is DAY and 15:12 in the Nexus')
def notify_time(bot, trigger):
    """Spits out gametime and whether or not it is day or night."""
    hour = int(time.strftime('%H', time.gmtime()))
    if hour % 2 == 0:
        bot.say('It is ' + sopel.formatting.color('NIGHT', fg='BLACK', bg='GREY') + ' and ' + time.strftime('%H:%M', time.gmtime()) + ' in the Nexus')
    else:
        bot.say('It is ' + sopel.formatting.color('DAY', fg='BLACK', bg='YELLOW') + ' and ' + time.strftime('%H:%M', time.gmtime()) + ' in the Nexus')


@sopel.module.commands('setraid')
@sopel.module.example('!setraid 20 01 16 02 30', 'Raid time set to 20 Jan 02:30 which is in 14 hours and 13 minutes')
def raid_set(bot, trigger):
    """Sets the raid time in DD MM YY HH MM format."""
    try:
        rawnewraidtime = trigger.group(2).rstrip(' ')
        newraidtime = time.strptime(rawnewraidtime, '%d %m %y %H %M')
    except:
        bot.say('Usage: !setraid DD MM YY HH MM')
        return
    timediffinhours = (calendar.timegm(newraidtime) - calendar.timegm(time.gmtime())) / 60 / 60
    remaindermins = ((calendar.timegm(newraidtime) - calendar.timegm(time.gmtime())) / 60) % 60

    if (calendar.timegm(newraidtime) - calendar.timegm(time.gmtime())) < 0:
        bot.say('You can\'t raid in the past!')
        return

    bot.db.set_channel_value(trigger.sender, 'raidtime', calendar.timegm(newraidtime))
    bot.say(
            'Raid time set to '
            + time.strftime('%d %b %H:%M', newraidtime)
            + ' which is in '
            + str(timediffinhours)
            + ' hours and '
            + str(remaindermins)
            + ' minutes'
            )


@sopel.module.commands('char')
@sopel.module.example('!char Ygritte', 'NAME: Ygritte - LVL: 19 - CLASS: Sorcerer - STATUS: alive - FACTION: Oblivion Squadron http://www.nexusclash.com/modules.php?name=Game&op=character&id=8104')
def get_char(bot, trigger):
    """ Looks up NC character, if found, returns summary and link """
    if trigger.group(2) == None:
        bot.say('Usage: !char <alt name>')
        return
    get_char_url = 'http://www.nexusclash.com/modules.php?name=Character&charname=' + trigger.group(2).rstrip(' ').replace(' ', '%20') + '&format=json'
    response = urllib.urlopen(get_char_url)
    data = json.loads(response.read())
    if not data['result']['character']['name']['name'] == '':
        char_lvl = str(data['result']['character']['level'])
        char_name = data['result']['character']['name']['name']
        char_class = data['result']['character']['classes'][-1]
        char_id = str(data['result']['character']['id'])
        if data['result']['character']['status']['alive'] == True:
            char_status = 'alive'
        else:
            char_status = 'dead'
        char_string = 'NAME: ' + char_name + ' - LVL: ' + char_lvl + ' - CLASS: ' + char_class + ' - STATUS: ' + char_status
        if data['result']['character']['faction']['id'] != 0:
            char_string += (' - FACTION: ' + data['result']['character']['faction']['name'])
        char_string += ' http://www.nexusclash.com/modules.php?name=Game&op=character&id=' + char_id

        bot.say(char_string)
    else:
        bot.say('Not found. Are you sure the name is correct?')


@sopel.module.commands('whenraid')
@sopel.module.example('!whenraid', 'Next raid is at 20 Jan 02:30 which is in 12 hours and 31 minutes')
def raid_when(bot, trigger):
    """Returns the time raid was set using !setraid"""
    raidtimeseconds = bot.db.get_channel_value(trigger.sender, 'raidtime')
    if raidtimeseconds != None:
        raidtime = time.gmtime(raidtimeseconds)
    else:
        bot.say('No raid time set')
        return

    timediffinhours = (raidtimeseconds - calendar.timegm(time.gmtime())) / 60 / 60
    remaindermins = ((raidtimeseconds - calendar.timegm(time.gmtime())) / 60) % 60
    bot.say(
            'Next raid is at '
            + time.strftime('%d %b %H:%M', raidtime)
            + ' which is in '
            + str(timediffinhours)
            + ' hours and '
            + str(remaindermins)
            + ' minutes'
            )


@sopel.module.thread(False)
@sopel.module.rule('(.*)')
@sopel.module.priority('low')
def character_lookup_auto(bot, trigger):
    """ Checks for NC character link, if found, returns summary """
    possible_url_array = trigger.rstrip(' ').split('=')
    if len(possible_url_array) < 3:
        return
    if possible_url_array[-2] == 'character&id':
        get_char_url = 'http://www.nexusclash.com/modules.php?name=Character&id=' + possible_url_array[-1] + '&format=json'
        response = urllib.urlopen(get_char_url)
        data = json.loads(response.read())
        if not data['result']['character']['name']['name'] == '':
            char_lvl = str(data['result']['character']['level'])
            char_name = data['result']['character']['name']['name']
            char_class = data['result']['character']['classes'][-1]
            if data['result']['character']['status']['alive'] == True:
                char_status = 'alive'
            else:
                char_status = 'dead'
            char_string = 'NAME: ' + char_name + ' - LVL: ' + char_lvl + ' - CLASS: ' + char_class + ' - STATUS: ' + char_status
            if data['result']['character']['faction']['id'] != 0:
                char_string += (' - FACTION: ' + data['result']['character']['faction']['name'])
            bot.say(char_string)
