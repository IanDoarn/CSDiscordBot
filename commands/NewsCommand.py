import feedparser
from bs4 import BeautifulSoup

from core.Command import Command
from utils import JsonUtils


def strip_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.getText()


def get_news(course_name, rss_dict, embed):
    embed.title = course_name.upper() + " News"
    key = rss_dict[course_name]  # retrieves the rss feed value
    if key == "n/a":
        embed.description = "No news data is available for this course. If you would like to receive news, please contact Adam or Marshall"
        return embed
    # if the key is available, do stuff
    news = feedparser.parse(
        "https://elearn.memphis.edu/d2l/le/news/rss/" + key + "/course?token=ax72b4q7smuiounj1185cb")
    entries = news.entries
    # print(news.headers.get(""))
    if len(entries) == 0:
        embed.description = "No news has been recently posted for this course."
        return embed
    for entry in entries:
        num_of_fields = len(entry) // 1024 + 1
        for i in range(num_of_fields):
            embed.add_field(name="**" + entry.title + "**", value=strip_text(entry.summary[i*1024:i+1*1024]), inline=False)
    return embed


class NewsCommand(Command):
    def __init__(self):
        self.name = "news"
        self.help = "Pulls news data from ecourseware"
        self.category = "School"
        self.required_arguments = 0
        self.required_role = None
        self.mod_command = False
        self.user_permissions = None
        self.bot_permissions = None
        self.cooldown = 0
        self.aliases = ["updates", "newsfeed"]

    @staticmethod
    async def execute(message, bot, args, embed):
        rss_dict = JsonUtils.get_rss_dict(bot)
        name = message.channel.name
        if args:
            name = args[0]
        name = name.upper().replace("-", "")
        if "COMP" not in name or name not in rss_dict:
            embed.description = "No data is available for this course"
            await message.channel.send(embed=embed)
            return
        await message.channel.send(embed=get_news(name, rss_dict, embed))