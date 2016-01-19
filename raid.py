import sopel.module
import sopel.formatting
import time
from threading import Timer

@sopel.module.commands('raid')
@sopel.module.example('!raid', 'RAID! <nicknames>')
def notify_raid(bot, trigger):
    """Pings everyone in the channel and tells them we are being raided"""
    if trigger.sender[0] == '#':
        nicks_in_channel = ''
        for nick in bot.privileges[trigger.sender]:
            nicks_in_channel += nick + ' '
        bot.say(sopel.formatting.color('RAID!!!', fg='RED', bg='BLACK') + ' ' + nicks_in_channel)
        bot.say(sopel.formatting.color('WE ARE BEING RAIDED', fg='RED', bg='BLACK'))
	Timer(10, bot.say, [sopel.formatting.color('RAID!!!', fg='RED', bg='BLACK') + ' ' + nicks_in_channel]).start()

@sopel.module.commands('bash')
@sopel.module.example('!bash', 'BASH! <nicknames>')
def notify_bash(bot, trigger):
    """Pings everyone in the channel and tells them to bash the wards"""
    if trigger.sender[0] == '#':
        nicks_in_channel = ''
        for nick in bot.privileges[trigger.sender]:
            nicks_in_channel += nick + ' '
        bot.say(nicks_in_channel)
        bot.say(sopel.formatting.color('BASH PEONS, BASH!', fg='YELLOW', bg='BLACK'))


@sopel.module.commands('forts')
@sopel.module.example('!forts', 'BRING DOWN THEIR FORTS! <nicknames>')
def notify_forts(bot, trigger):
    """Pings everyone in the channel and tells them to bring down the forts"""
    if trigger.sender[0] == '#':
        nicks_in_channel = ''
        for nick in bot.privileges[trigger.sender]:
            nicks_in_channel += nick + ' '
        bot.say(nicks_in_channel)
        bot.say(sopel.formatting.color('BRING DOWN THEIR FORTS!', fg='YELLOW', bg='BLACK'))


@sopel.module.commands('active')
@sopel.module.commands('actives')
@sopel.module.commands('kill')
@sopel.module.example('!kill <character>', 'KILL <character>')
def notify_kill(bot, trigger):
    """Notifies channel of actives"""
    if trigger.group(2) is None:
        bot.say('Usage: !kill <alt>')
        return
    if trigger.sender[0] == '#':
        nicks_in_channel = ''
        for nick in bot.privileges[trigger.sender]:
            nicks_in_channel += nick + ' '
        bot.say(nicks_in_channel)
        bot.say(sopel.formatting.color('KILL ACTIVES: ' + trigger.group(2), fg='RED', bg='BLACK'))

