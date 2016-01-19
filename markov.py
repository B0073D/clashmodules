import sopel.module
import sopel.formatting
import time
import random
from operator import itemgetter
import numpy.random as nprandom


@sopel.module.thread(False)
@sopel.module.rule('(.*)')
@sopel.module.priority('low')
def markov_note(bot, trigger):
    MARKOV_VERSION = 7
    if not trigger.is_privmsg and trigger[0] != bot.config.core.prefix[1]:
        message = trigger.split(' ')
        markov_words = bot.db.get_nick_value(trigger.nick, 'markov_words')
        markov_version = bot.db.get_nick_value(trigger.nick, 'markov_version')
        if markov_words == None or markov_version != MARKOV_VERSION:
            markov_words = {}
        count = 0
        for word in message:
            # print 'Message word count: ' + str(len(message))
            if count + 1 == len(message):  # Added one to count to match actual length not array index
                if word not in markov_words:
                    markov_words[word] = {}
                    markov_words[word]['\n'] = 1
                elif '\n' not in markov_words[word]:
                    markov_words[word]['\n'] = 1
                else:
                    markov_words[word]['\n'] += 1
            else:
                if word not in markov_words:
                    markov_words[word] = {}
                    # print count
                    # print message[count]
                    markov_words[word][message[count+1]] = 1  # Count is now index...
                else:
                    if message[count+1] not in markov_words[word]:
                        markov_words[word][message[count+1]] = 1
                    else:
                        markov_words[word][message[count+1]] += 1
            count += 1

        bot.db.set_nick_value(trigger.nick, 'markov_words', markov_words)
        bot.db.set_nick_value(trigger.nick, 'markov_version', MARKOV_VERSION)


@sopel.module.rate(120)
@sopel.module.commands('clone')
def markov_clone(bot, trigger):
    if trigger.group(2) is None:
        bot.say('Usage: !clone <username>')
        return
    command = trigger.group(2).rstrip(' ').split(' ')
    clonenick = command[0]
    if len(command) > 1:
        startword = command[1]
    else:
        startword = None
    markov_words = bot.db.get_nick_value(clonenick, 'markov_words')
    if markov_words is not None:
        if len(markov_words) < 20:
            bot.say(clonenick + ' has not said enough!')
            return
    else:
        bot.say(clonenick + ' has not said enough!')
        return

    if startword not in markov_words and startword != None:
        bot.say('Choose another starting word')
        return
    clone_words = []
    count = 1
    while len(clone_words) < 10:
        if count > 50:
            bot.say('Apparently ' + clonenick + ' doesn\'t like long sentences...')
            return
        clone_words = []
        if startword == None:
            nextword = random.choice(markov_words.keys())
        else:
            nextword = startword
        while nextword != '\n':
            clone_words.append(nextword)
            if len(clone_words) > 50:
                bot.say('Ow that hurt...Too many words...')
                return
            nextword = markov_result(markov_words[clone_words[-1]])
        count += 1

    bot.say('Clone ' + clonenick + ' says: ' + ' '.join(clone_words))


@sopel.module.commands('debugmarkov')
def markov_debug(bot, trigger):
    if trigger.group(2) is None:
        bot.say('Usage: !debugmarkov <username>')
        return
    markov_words = bot.db.get_nick_value(trigger.group(2).rstrip(' '), 'markov_words')
    print markov_words


def markov_result(word):
    number_of_choices = sum(word.values())
    words = []
    word_chances = []
    for key in word.keys():
        words.append(key)
        word_chances.append(float(word[key])/float(number_of_choices))

    return nprandom.choice(words, p=word_chances)
