import re

from amiyabot import Message, Chain

from library import set_atall
from bot import BotConfig, bot
from core.control import Permission
from library.uid_extract import uid_extract


message_re = re.compile(r"^(开启|关闭)@?全体(成员)? ?(.*)$")


@bot.on_message(keywords=[message_re])
async def main(ctx: Message):
    Permission.manual(ctx.user_id, Permission.GROUP_ADMIN)
    regex_result = message_re.match(ctx.text)
    if uid := regex_result[3]:  # type: ignore
        uid = await uid_extract(uid, ctx.channel_id)
        if uid:
            if regex_result[1] == "开启":  # type: ignore
                if ctx.is_admin or ctx.user_id in BotConfig.admins:  # type: ignore
                    msg = (
                        f"{uid} @全体开启成功"
                        if set_atall(uid, ctx.channel_id, True)
                        else "该群未关注此 UP"
                    )
                else:
                    msg = "Bot 权限不足，无法开启@全体，请赋予 Bot 管理员权限或更高"
            else:
                msg = f"{uid} @全体关闭成功" if set_atall(uid, ctx.channel_id, False) else "该群未关注此 UP"
        else:
            msg = "请输入正确的 UID"
    else:
        msg = "请输入正确的 UID"

    return Chain(ctx).text(msg)
