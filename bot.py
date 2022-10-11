import asyncio
import contextlib

from pathlib import Path
from amiyabot import AmiyaBot, MultipleAccounts
from amiyabot.adapters.mirai import mirai_api_http

from main import BotConfig
from core.log import logger
from core.announcement import base_telemetry

logger.info("BBot is starting...")

base_telemetry()

host = str(BotConfig.Mirai.mirai_host.host)
port = int(BotConfig.Mirai.mirai_host.port)

accounts = (
    AmiyaBot(
        appid=BotConfig.Mirai.account,
        token=BotConfig.Mirai.verify_key,
        adapter=mirai_api_http(
            host=host,
            ws_port=port,
            http_port=port,
        ),
    ),
)

bot = MultipleAccounts(*accounts)

# if BotConfig.Bilibili.use_browser:
#     app.launch_manager.add_service(
#         PlaywrightService(
#             user_data_dir=Path("data").joinpath("browser"),
#             device_scale_factor=2 if BotConfig.Bilibili.mobile_style else 1.25,
#             user_agent=(
#                 "Mozilla/5.0 (Linux; Android 10; RMX1911) AppleWebKit/537.36 "
#                 "(KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"
#             )
#             if BotConfig.Bilibili.mobile_style
#             else "",
#         )
#     )


with contextlib.suppress(KeyboardInterrupt, asyncio.exceptions.CancelledError):
    asyncio.run(bot.start())

logger.info("BBot is shutting down...")
