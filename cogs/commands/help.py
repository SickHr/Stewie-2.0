import discord
from discord.ext import commands
from discord.commands import slash_command


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.current_page = 0
        self.message = None  # Initialisieren Sie self.message mit None

        self.commands = [
            {
                "title": "Bot Commands - Moderation",
                "description": "",
                "commands": {
                    "/kick": "Kickt den Benutzer. (kick_members Berechtigung erforderlich)",
                    "/ban": "Bannt den Benutzer. (ban_members Berechtigung erforderlich)",
                    "/unban": "Entbannt den Benutzer. (ban_members Berechtigung erforderlich)",
                    "/clear": "Löscht die angegebene Anzahl an Nachrichten. (manage_message Berechtigung erforderlich)",
                    "/purge": "Löscht alle Nachrichten im aktuellen Channel. (manage_messages Berechtigung erforderlich)",
                    "/slowchat": "Setzt den Slowmode auf den angegebenen Wert. (manage_messages Berechtigung erforderlich)",

                }
            },
            {
                "title": "Bot Commands - Economy",
                "description": "",
                "commands": {
                    "Placeholder": "Placeholder",

                }
            },
            {
                "title": "Bot Commands - Fun",
                "description": "",
                "commands": {
                    "/roll": "Würfle mit der angegebenen Anzahl an Seiten.",
                    "/ratezahl": "Errate die Zahl.",
                    "/miesmuschel": "Frag die Magische Miesmuschel",
                    "/gif": "Suche nach einem GIF.",
                    "/avatar": "Schau dir das Profilbild eines Benutzers an.",

                }
            },
            {
                "title": "Bot Commands - Server",
                "description": "",
                "commands": {
                    "Placeholder": "Placeholder",
                    # ... Weitere Befehle hier
                }
            }
        ]

    @slash_command(description="Zeigt dir alle vorhandenen Commands an")
    async def help(self, ctx):
        self.current_page = 0
        embed = self.build_embed(self.current_page)
        self.message = await ctx.send(embed=embed)
        await self.add_reactions()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user != self.client.user and reaction.message == self.message:
            if str(reaction.emoji) == '➡':
                self.current_page = (self.current_page + 1) % len(self.commands)
            elif str(reaction.emoji) == '⬅':
                self.current_page = (self.current_page - 1) % len(self.commands)

            embed = self.build_embed(self.current_page)
            await self.message.edit(embed=embed)
            await reaction.remove(user)

    def build_embed(self, page):
        command_dict = self.commands[page]
        embed = discord.Embed(title=command_dict["title"], description=command_dict["description"],
                              color=discord.Color.blue())
        for command, description in command_dict["commands"].items():
            embed.add_field(name=command, value=description, inline=False)
        return embed

    async def add_reactions(self):
        await self.message.add_reaction('⬅')
        await self.message.add_reaction('➡')


def setup(client):
    client.add_cog(Help(client))
