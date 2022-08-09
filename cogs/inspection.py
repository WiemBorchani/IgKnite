'''
The `Inspection` cog for IgKnite.
---

MIT License

Copyright (c) 2022 HitBlast

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


# Imports.
import datetime

import disnake
from disnake.ext import commands

import core


# The actual cog.
class Inspection(commands.Cog):
    def __init__(self, bot: commands.AutoShardedInteractionBot) -> None:
        self.bot = bot

    @commands.slash_command(
        name='guildinfo',
        description='Shows all important information about the server.'
    )
    @commands.guild_only()
    async def _guildinfo(self, inter: disnake.CommandInter) -> None:
        embed = core.embeds.ClassicEmbed(inter).add_field(
            name='Birth',
            value=datetime.strptime(str(inter.guild.created_at), '%Y-%m-%d %H:%M:%S.%f%z').strftime('%b %d, %Y'),
        ).add_field(
            name='Owner',
            value=inter.guild.owner.mention
        ).add_field(
            name='Members',
            value=inter.guild.member_count
        ).add_field(
            name='Roles',
            value=len(inter.guild.roles)
        ).add_field(
            name='Channels',
            value=len(inter.guild.text_channels) + len(inter.guild.voice_channels)
        ).add_field(
            name='Identifier',
            value=inter.guild_id
        )

        if not inter.guild.icon:
            embed.set_thumbnail(url=inter.guild.icon)

        await inter.send(embed=embed)


# The setup() function for the cog.
def setup(bot: commands.AutoShardedInteractionBot) -> None:
    bot.add_cog(Inspection(bot))
