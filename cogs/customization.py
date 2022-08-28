'''
The `Customization` cog for IgKnite.
---

MIT License

Copyright (c) 2022 IgKnite

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
import discord
from discord import app_commands
from discord.ext import commands

import core
from core.datacls import LockRoles


# The actual cog.
class Customization(commands.Cog):
    def __init__(self, bot: core.IgKnite) -> None:
        self.bot = bot

    # makerole
    @app_commands.command(
        name='makerole',
        description='Create a new role.'
    )
    @app_commands.describe(
        name='Name of the role.'
    )
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(LockRoles.admin)
    async def _makerole(
        self,
        inter: discord.Interaction,
        name: str
    ) -> None:
        await inter.guild.create_role(name=name)
        await inter.response.send_message(f'Role **@{name}** has been created!')

    # assignrole
    @app_commands.command(
        name='assignrole',
        description='Assign a role to a server member.'
    )
    @app_commands.describe(
        member='Mention the server member.',
        role='Role to be assigned.'
    )
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(LockRoles.admin)
    async def _assignrole(
        self,
        inter: discord.Interaction,
        member: discord.Member,
        role: discord.Role
    ) -> None:
        await member.add_roles(role)
        await inter.response.send_message(f'Role <@&{role.id}> has been assigned to **{member.name}**!')

    # removerole
    @app_commands.command(
        name='removerole',
        description='Remove a role from the server.'
    )
    @app_commands.describe(
        role='Mention the role.'
    )
    @app_commands.checks.has_any_role(LockRoles.admin)
    async def _removerole(
        self,
        inter: discord.Interaction,
        role: discord.Role
    ) -> None:
        await role.delete()
        await inter.response.send_message(f'Role **@{role.name}** has been removed!')

    # makeinvite
    @app_commands.command(
        name='makeinvite',
        description='Create an invitation link to the server.'
    )
    @app_commands.describe(
        max_age='How long the invite should last in seconds. Default is unlimited.',
        max_uses='How many users can use this invite. Default is unlimited.',
        reason='The reason behind creating the invite.',
    )
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(LockRoles.mod, LockRoles.admin)
    @core.decor.long_running_command
    async def _makeinvite(
        self,
        inter: discord.Interaction,
        max_age: int = 0,
        max_uses: int = 0,
        reason: str = 'No reason provided'
    ) -> None:
        invite = await inter.channel.create_invite(max_age=max_age, max_uses=max_uses, reason=reason)
        embed = core.embeds.ClassicEmbed(inter).add_field(
            name='Link',
            value=f'https://discord.gg/{invite.code}'
        ).add_field(
            name='Code',
            value=f'`{invite.code}`'
        ).add_field(
            name='Lifetime',
            value='Unlimited' if max_age == 0 else f'{max_age} Seconds'
        )

        embed.title = 'Created a new invite!'

        await inter.followup.send(embed=embed)

    # nick
    @app_commands.command(
        name='nick',
        description='Change nickname of a member.'
    )
    @app_commands.describe(
        member='Mention the member.',
        nickname='New nickname for the member.'
    )
    @app_commands.guild_only()
    @app_commands.checks.has_any_role(LockRoles.mod, LockRoles.admin)
    async def _nick(
        self,
        inter: discord.Interaction,
        member: discord.Member,
        nickname: str
    ) -> None:
        await member.edit(nick=nickname)
        await inter.response.send_message(f'User <@{member.id}> has been renamed to **{nickname}**!')


# The setup() function for the cog.
async def setup(bot: core.IgKnite) -> None:
    await bot.add_cog(Customization(bot))
