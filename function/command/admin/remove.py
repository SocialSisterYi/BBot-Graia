import re

from amiyabot import Message, Chain

from bot import bot
from bot import BotConfig
from core.control import Permission


message_re = re.compile(r"移除管理员 ?(.*)")


@bot.on_message(keywords=[message_re])
async def main(ctx: Message):
    Permission.manual(ctx.user_id, Permission.MASTER)
    if message := message_re.match(ctx.text):
        if not (say_qq := message[1]):
            return Chain(ctx, True, True).text("未输入账号")
        if not say_qq.isdigit():
            return Chain(ctx, True, True).text("管理员账号仅可为数字")
        if int(say_qq) not in BotConfig.admins:
            return Chain(ctx, True, True).text("该用户不是管理员了")
        BotConfig.admins.remove(int(say_qq))
        BotConfig.save()
        return Chain(ctx, True, True).text("成功将该用户移除管理员")
