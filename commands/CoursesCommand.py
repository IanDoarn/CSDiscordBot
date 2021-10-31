from core.Command import Command


class CoursesCommand(Command):
    def __init__(self):
        self.name = "courses"
        self.help = "Lists all core Computer Science courses"
        self.category = "School"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["classes"]

    @staticmethod
    async def execute(message, bot, args, embed):
        courses = bot.courses
        embed.title = "Computer Science (Major) Courses"
        embed.description = "A list of the required courses for the CS Major"
        for course in courses:
            embed.add_field(name=course.code, value=course.name, inline=True)
        await message.channel.send(embed=embed)
