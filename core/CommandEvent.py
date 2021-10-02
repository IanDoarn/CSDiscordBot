import discord


class CommandEvent:
    def __init__(self, message, command, arguments, bot):
        self.message = message
        self.command = command
        self.arguments = arguments
        self.bot = bot

    async def execute_checks(self):
        embed_builder = discord.Embed(color=discord.Color.blue())
        if len(self.arguments) < self.command.required_arguments:
            embed_builder.description = "Not enough arguments, expected " + str(self.command.required_arguments)
            await self.message.channel.send(embed=embed_builder)
            return  # argument check
        if self.command.mod_command and self.message.author.id not in self.bot.admins:
            embed_builder.description = "This command is only for bot admins"
            await self.message.channel.send(embed=embed_builder)
            return  # mod command check
        if self.command.required_role is not None:
            role = discord.utils.find(lambda r: r.name == self.command.required_role, self.message.guild.roles)
            if role not in self.message.author.roles:
                embed_builder.description = "You don't have permission to use this command"
                await self.message.channel.send(embed=embed_builder)
                return  # mod command check
        await self.command.execute(self.message, self.bot, self.arguments)
