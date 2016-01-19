import sopel.module
import sopel.formatting



@sopel.module.rule('$nick' '(?i)(help|doc) +([A-Za-z]+)(?:\?+)?$')
@sopel.module.example('.help tell')
@sopel.module.commands('nchelp', 'commands')
@sopel.module.priority('low')
def help(bot, trigger):
    """Shows a command's documentation, and possibly an example."""
    bot.say('Hi! I\'m a bot! My commands will be messaged to you in private.')
    bot.say('If you encounter any issues, I belong to tevoska', trigger.nick)
    bot.say('!raid : This warns everyone in the channel of a raid', trigger.nick)
    bot.say('!bash : This tells everyone in the channel to bash', trigger.nick)
    bot.say('!kill/!active <alt> : This tells everyone in the channel to kill the <alt>', trigger.nick)
    bot.say('!forts : This tells everyone in the channel to bring down the forts', trigger.nick)
    bot.say('!nctime : This tells you NCs game time and whether it\' day or night', trigger.nick)
    bot.say('!sm <minutes> : This reminds people in <minutes> when you are healable', trigger.nick)
    bot.say('!ping <message> : This pings everyone in the channel and tells them <message>', trigger.nick)
    bot.say('data: tell <nick> <message> : This will tell <nick> your <message> when they are active again', trigger.nick)
    bot.say('Hunt Game Commands:', trigger.nick)
    bot.say('!angelhunt : Starts an Angel hunt. Angels will spawn randomly based on channel settings or defaults (default is onceish every four hours)', trigger.nick)
    bot.say('!bang : This shoots the damn thing! 50% chance in first ten seconds, 100% after that', trigger.nick)
    bot.say('!stophunt : Stops the hunt. Boooooo.', trigger.nick)
    bot.say('!angelkills : Displays top five angel kills for your channel', trigger.nick)
    bot.say('!mykills : Displays your kills for that channel.', trigger.nick)
