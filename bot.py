import discord
import apihandler
import anilist
import random

client = discord.Client()

@client.event
async def on_ready():
    print('Logged on as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!lookup'):
        searchTerm = message.content.split(' ', 1)[1]
        await lookup(searchTerm, message.channel)

    if message.content.startswith('!hello'):
        await message.channel.send('Please don\'t talk to me, {}, you filthy weeb.'.format(message.author))

#    for word in message.contet.split(''):
#        if word in weebWords:
#            await message.channel.send(random.choice(weebResponses))


async def lookup(term, channel):
    response = None
    try:
        response = apihandler.search(term)
    except Exception as e:
        await channel.send(e)
    
    if len(response) > 1:
        msg = 'Please select an anime by responding with its number:\n'
        n = 1
        for anime in response:
            msg += '{}: {} ({})\n'.format(n, anime['title'], anime['year'])
            n += 1

        botmsg = await channel.send(msg) 
        reply = await client.wait_for('message')

        try:
            await channel.delete_messages([reply, botmsg])
            animeId = response[int(reply.content) - 1]['id']
            anime = apihandler.getAnime(animeId)
            await channel.send(embed=anime.toEmbed())
        except Exception as e:
            await channel.send('error: {}'.format(e))
    else:
        await channel.send(embed=response[0].toEmbed())

if __name__ == '__main__':
    client.run('')