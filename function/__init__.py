import function.command.add_talk
import function.command.announcement
import function.command.init
import function.command.quit_group
import function.command.status
import function.command.video_resolve
import function.command.vive_dynamic
import function.command.admin.add
import function.command.admin.remove
import function.command.configure.atall
import function.command.configure.nick
import function.command.menu
import function.command.subgroup.add_up
import function.command.subgroup.add
import function.command.subgroup.get_subgroup
import function.command.subgroup.remove_up
import function.command.subgroup.remove
import function.command.up.get_subscribe
import function.command.up.subscribe
import function.command.up.unsubscribe
import function.command.vip.add
import function.command.vip.remove
import function.command.whitelist.add
import function.command.whitelist.close
import function.command.whitelist.open
import function.command.whitelist.remove
import function.command.web_auth
import function.event.bot_launch
import function.event.exception
import function.event.invited_join_group
import function.event.join_group
import function.event.leave_group
import function.event.mute
import function.event.offline
import function.event.new_friend
import function.event.prem_change
import function.pusher.init
import function.pusher.dynamic
import function.pusher.live  # noqa

# import function.scheduler.refresh_token  # noqa

from loguru import logger

logger.success("[function] 加载完成")
