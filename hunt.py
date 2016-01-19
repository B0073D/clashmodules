import sopel.module
import sopel.formatting
import time
import random
from operator import itemgetter


"""

Hunt types:
None/0: No hunt
angel: Angel hunt
mortal: Mortal hunt
demon: Demon hunt

"""


@sopel.module.require_owner
@sopel.module.commands('resetkills')
def hunt_reset(bot, trigger):
    bot.db.set_channel_value(trigger.sender, 'kills', {})
    bot.db.set_channel_value(trigger.sender, 'channel_kills', {})
    bot.say('Kills reset...')


@sopel.module.commands('bang')
def bang_basic(bot, trigger):
    """Fires at something if it is there, if nothing is there, will abuse user"""
    spawned = bot.db.get_channel_value(trigger.sender, 'spawned')
    spawntype = bot.db.get_channel_value(trigger.sender, 'hunt')
    channel_kills = bot.db.get_channel_value(trigger.sender, 'channel_kills')
    if spawntype == 'angel':
        spawntypetext = 'an Angel'
    elif spawntype == 'mortal':
        spawntypetext = 'a Mortal'
    elif spawntype == 'demon':
        spawntypetext = 'a Demon'
    if spawned == None or spawned == 0:
        nothingthere = [
            'What are you shooting at you imbecile!',
            'LOUD NOISES',
            'Errr... Are you not deaf enough?',
            'Hey! Don\'t shoot the spoon! What did the spoon do to you??',
            'You really just like making a lot of noise don\'t you',
            'WHY would you DO that!?',
            'Calm down Terminator, there\'s nothing there.',
            'Do I need to confiscate that?',
            'What are you shooting at you dolt!'
        ]
        bot.say(random.choice(nothingthere))
    else:
        kills = bot.db.get_channel_value(trigger.sender, 'kills')
        if kills == None:
            kills = {}
        if trigger.nick not in kills:
            kills[str(trigger.nick).lower()] = {}
        if spawntype not in kills[str(trigger.nick).lower()]:
            kills[str(trigger.nick).lower()][spawntype] = 0

        if channel_kills == None or channel_kills == {}:
            channel_kills = {}
            channel_kills['angel'] = 0
            channel_kills['mortal'] = 0
            channel_kills['demon'] = 0
            
        spawndif = int(time.time()) - spawned
        if spawndif < 10:
            if random.randint(1, 2) == 1:
                kills[str(trigger.nick).lower()][spawntype] += 1
                channel_kills[spawntype] += 1
                bot.say('You shot ' + spawntypetext + ' in ' + str(spawndif) + ' seconds! You have killed ' + str(kills[str(trigger.nick).lower()][spawntype]) + ' of these in ' + trigger.sender)
                bot.db.set_channel_value(trigger.sender, 'kills', kills)
                bot.db.set_channel_value(trigger.sender, 'spawned', 0)  # This 'kills' the unit.
            else:
                misstext = [
                    'You missed!',
                    'Your weapon jammed!',
                    'You suddenly realise that you are not in fact holding a rifle, but a rather small squid!',
                    'Your pointy stick does nothing but look back up at you in dismay because it\'s a stick, not a gun',
                    'You make a \'bang\' sound and everyone laughs at you',
                    'You miss and instead hit the spoon on the table, YOU MONSTER!',
                    'You miss!',
                    'You missed!',
                    'You shot yourself in the foot!',
                    'Your weapon misfires and explodes in your hand! You now have one less hand.'
                ]
                bot.say(random.choice(misstext))
        else:
            channel_kills[spawntype] += 1
            kills[str(trigger.nick).lower()][spawntype] += 1
            bot.say('You shot ' + spawntypetext + ' in ' + str(spawndif) + ' seconds! You have killed ' + str(kills[str(trigger.nick).lower()][spawntype]) + ' of these in ' + trigger.sender)
            bot.db.set_channel_value(trigger.sender, 'kills', kills)
            bot.db.set_channel_value(trigger.sender, 'spawned', 0)


@sopel.module.commands('angelhunt')
def hunt_angel(bot, trigger):
    """Starts an Angel Hunt"""
    hunttype = bot.db.get_channel_value(trigger.sender, 'hunt')
    if hunttype == None or hunttype == 0:
        bot.db.set_channel_value(trigger.sender, 'hunt', 'angel')
        bot.say('Angels have been spotted nearby!')
    else:
        bot.say('A hunt is already on! You must stop the hunt with !stophunt before you can start another one.')


@sopel.module.commands('mortalhunt')
def hunt_mortal(bot, trigger):
    bot.say('Mortals have been spotted nearby!')


@sopel.module.commands('demonhunt')
def hunt_demon(bot, trigger):
    bot.say('Demons have been spotted nearby!')


@sopel.module.commands('stophunt')
def hunt_stop(bot, trigger):
    """Stops the hunt"""
    bot.db.set_channel_value(trigger.sender, 'hunt', 0)
    bot.db.set_channel_value(trigger.sender, 'spawned', 0)
    bot.say('Hunt has been stopped, the enemy has retreated... Boooo....')


@sopel.module.require_admin
@sopel.module.commands('huntinterval')
def hunt_set_interval(bot, trigger):
    """Sets or returns the hunt interval for that channel in minutes. Admin only."""
    try:
        huntint = int(trigger.group(2).rstrip(' '))
        bot.db.set_channel_value(trigger.sender, 'huntinterval', huntint)
        bot.say('Hunt interval has been set to one in every ' + str(huntint) + ' minutes or so')
    except:
        huntintset = bot.db.get_channel_value(trigger.sender, 'huntinterval')
        if huntintset == None:
            bot.say('Hunt interval not set. Using default')
        else:
            bot.say('Hunt interval is set to once every ' + str(huntintset) + 'minutes or so.') 


@sopel.module.commands('angelkills')
def hunt_angelkills(bot, trigger):
    """Lists top angel kills for that channel"""
    kills = bot.db.get_channel_value(trigger.sender, 'kills')
    highscore = []
    for murderer in kills:
        highscore.append([murderer, kills[murderer]['angel']])
    sorted_highscore = sorted(highscore, key=itemgetter(1), reverse=True)
    if len(sorted_highscore) > 5:
        sorted_highscore = sorted_highscore[:5]
    highscore_text = ''
    for score in sorted_highscore:
        highscore_text += score[0] + ': ' + str(score[1]) + ' . '
    bot.say('Top 5 angel kills in ' + trigger.sender + ' : ' + highscore_text)


@sopel.module.commands('mykills')
def hunt_mykills(bot, trigger):
    """ Returns your own kills """
    kills = bot.db.get_channel_value(trigger.sender, 'kills')
    if str(trigger.nick).lower() not in kills:
        bot.say('You have not killed anything yet! READY YOUR WEAPON!')
    else:
        bot.say('You have killed ' + str(kills[str(trigger.nick).lower()]['angel']) + ' angels.')

    
@sopel.module.interval(60)
def hunt_runner(bot):
    """ This runs the hunt. """
    default_spawn_chance = 240
    for channel in bot.channels:
        channel_hunt = bot.db.get_channel_value(channel, 'hunt')
        channel_spawned = bot.db.get_channel_value(channel, 'spawned')
        if not (channel_hunt == None or channel_hunt == 0):
            angeltexts = [
                'A bright light suddenly appears! Angelic music is heard! An Angel! BRING IT DOWN!',
                'With a huge crash an Angel lands in your midsts! It raises it\'s sword! KILL IT!',
                'The sky suddenly brightens as a bright figure speeds towards you! An Angel! MAKE IT PAY!',
                'Suddenly a loud booming voice says "I WILL BRING YOU TO JUSTICE". An Angel DARES enter this realm? Show it who rules this place!'
                ]
            if channel_hunt == 'angel' and (channel_spawned == None or channel_spawned == 0):
                spawn_chance = bot.db.get_channel_value(channel, 'huntinterval')
                if spawn_chance == None:
                    spawn_chance = default_spawn_chance
                if random.randint(1, spawn_chance) == 1:
                    bot.db.set_channel_value(channel, 'spawned', int(time.time()))
                    bot.msg(channel, random.choice(angeltexts))
