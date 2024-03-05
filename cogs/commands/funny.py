import asyncio
import random

import discord
from discord import slash_command, option
from discord.ext import commands

active_games = {}  # Leeres Dictionary zum Speichern der aktiven Spiele
class Funny(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(description="Würfel einen Würfel")
    async def roll(self, ctx):
        roll = random.randint(1, 6)
        embed = discord.Embed(title="🎲 Würfeln", description=f"Du hast eine **{roll}** gewürfelt!")
        await ctx.respond(embed=embed)


    @slash_command(description="Errate die richtige Zahl")
    async def ratezahl(self, ctx):
        author_id = str(ctx.author.id)  # Konvertiere die Benutzer-ID in einen String

        if author_id in active_games:
            embed = discord.Embed(title="🚫 Spiel läuft bereits",
                                  description="Du hast bereits ein Ratespiel laufen. Bitte beende das aktuelle Spiel, bevor du ein neues startest.",
                                  color=discord.Color.red())
            await ctx.respond(embed=embed)
            return

        active_games[author_id] = True  # Speichere den Spielstatus für den Benutzer

        number = random.randint(1, 100)
        embed = discord.Embed(title="🔢 Rate die Zahl",
                              description=f"Ich habe eine Zahl zwischen **1** und **100** ausgewählt.\nVersuche, sie zu erraten!")
        await ctx.respond(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while active_games[author_id]:
            try:
                guess = await self.client.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                embed = discord.Embed(title="🔢 Zeit abgelaufen!",
                                      description="Tut mir leid, du hast zu lange gebraucht, um die Zahl zu erraten.",
                                      color=discord.Color.red())
                await ctx.respond(embed=embed)
                del active_games[author_id]  # Entferne den Spielstatus für den Benutzer
                break

            if int(guess.content) == number:
                embed = discord.Embed(title="🎉 Gewonnen!",
                                      description=f"Gut gemacht! Du hast die Zahl **{number}** richtig erraten.",
                                      color=discord.Color.green())
                await ctx.respond(embed=embed)
                del active_games[author_id]  # Entferne den Spielstatus für den Benutzer
                break
            elif int(guess.content) < number:
                embed = discord.Embed(title="🔢 Zu niedrig",
                                      description="Die gesuchte Zahl ist höher. Versuche es noch einmal!",
                                      color=discord.Color.random())
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(title="🔢 Zu hoch",
                                      description="Die gesuchte Zahl ist niedriger. Versuche es noch einmal!",
                                      color=discord.Color.random())
                await ctx.respond(embed=embed)

    @slash_command(name="miesmuschel", description="Lasse den Bot eine Frage mit Ja oder Nein beantworten")
    @option(name="frage", description="Frage", required=True)
    async def miesmuschel(self, ctx, *, frage):
        responses = [
            "Es ist sicher",
            "Es ist entschieden so",
            "Ohne Zweifel",
            "Definitiv",
            "Du kannst dich darauf verlassen",
            "Wie ich die Sache sehe, ja",
            "Höchstwahrscheinlich",
            "Gute Aussichten",
            "Ja",
            "Die Zeichen deuten auf ja",
            "Antwort ist unklar, versuche es später noch einmal",
            "Besser, ich sage dir das jetzt nicht",
            "Kann ich jetzt nicht vorhersagen",
            "Konzentriere dich und frage nochmal",
            "Verlasse dich nicht darauf",
            "Meine Antwort ist nein",
            "Meine Quellen sagen nein",
            "Aussichten sind nicht so gut",
            "Sehr zweifelhaft"
        ]

        embed = discord.Embed(
            title=f"🐚 Magische Miesmuschel\n -  -  -  -  -  -  -  -  -  -  -  -  -",
            description=f"Frage: {frage}",
            color=discord.Color.blue()
        )

        response = random.choice(responses)
        embed.add_field(
            name="",
            value=f"Antwort: {response}",
            inline=False
        )

        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(Funny(client))