import time
import contextlib

from pathlib import Path
from loguru import logger
from graia.ariadne import Ariadne
from sentry_sdk import capture_exception
from dynamicrendergrpc.Core.Dynamic import Render
from playwright.async_api._generated import Request
from playwright._impl._api_types import TimeoutError
from graiax.playwright.interface import PlaywrightContext
from bilireq.grpc.protos.bilibili.app.dynamic.v2.dynamic_pb2 import DynamicItem

from bot import BotConfig


error_path = Path("data").joinpath("error")
error_path.mkdir(parents=True, exist_ok=True)
mobile_style_js = Path(__file__).parent.joinpath("mobile_style.js").read_text(encoding="utf-8")


async def get_dynamic_screenshot(dyn: DynamicItem):
    dynid = dyn.extend.dyn_id_str
    if BotConfig.Bilibili.use_browser:
        st = int(time.time())
        app = Ariadne.current()
        browser_context = app.launch_manager.get_interface(PlaywrightContext).context
        for i in range(3):
            page = await browser_context.new_page()
            try:
                page.on("requestfinished", network_request)
                page.on("requestfailed", network_requestfailed)
                if BotConfig.Bilibili.mobile_style:
                    url = f"https://m.bilibili.com/dynamic/{dynid}"
                    await page.set_viewport_size({"width": 400, "height": 780})
                    with contextlib.suppress(TimeoutError):
                        await page.goto(url, wait_until="networkidle", timeout=20000)
                    if "bilibili.com/404" in url:
                        logger.warning(f"[Bilibili推送] {dynid} 动态不存在，正在尝试本地渲染")
                        break
                    await page.add_script_tag(content=mobile_style_js)
                    card = await page.query_selector(".dyn-card")
                    assert card
                    clip = await card.bounding_box()
                    assert clip
                else:
                    url = f"https://t.bilibili.com/{dynid}"
                    await page.set_viewport_size({"width": 2560, "height": 1080})
                    with contextlib.suppress(TimeoutError):
                        await page.goto(url, wait_until="networkidle", timeout=20000)
                    if "bilibili.com/404" in url:
                        logger.warning(f"[Bilibili推送] {dynid} 动态不存在，正在尝试本地渲染")
                        break
                    card = await page.query_selector(".card")
                    assert card
                    clip = await card.bounding_box()
                    assert clip
                    bar = await page.query_selector(".bili-dyn-action__icon")
                    assert bar
                    bar_bound = await bar.bounding_box()
                    assert bar_bound
                    clip["height"] = bar_bound["y"] - clip["y"] - 2
                image = await page.screenshot(
                    clip=clip, full_page=True, type="jpeg", quality=98
                )
                await page.close()
                return image
            except Exception as e:  # noqa
                url = page.url
                if "bilibili.com/404" in url:
                    logger.error(f"[Bilibili推送] {dynid} 动态不存在，正在尝试本地渲染")
                    break
                elif type(e) == AssertionError:
                    logger.exception(f"[BiliBili推送] {dynid} 动态截图失败，正在重试：")
                    await page.screenshot(
                        path=f"{error_path}/{dynid}_{i}_{st}.jpg",
                        full_page=True,
                        type="jpeg",
                        quality=80,
                    )
                else:
                    capture_exception()
                    logger.exception(f"[BiliBili推送] {dynid} 动态截图失败，正在重试：")
                    await page.screenshot(
                        path=f"{error_path}/{dynid}_{i}_{st}.jpg",
                        full_page=True,
                        type="jpeg",
                        quality=80,
                    )
                with contextlib.suppress():
                    await page.close()

    dynamic_rander = Render()
    try:
        return await dynamic_rander.run(dyn)
    except Exception:  # noqa
        capture_exception()
        logger.exception(f"[Bilibili推送] {dynid} 动态本地渲染失败")
        return None


async def network_request(request: Request):
    url = request.url
    method = request.method
    response = await request.response()
    if response:
        status = response.status
        timing = "%.2f" % response.request.timing["responseEnd"]
    else:
        status = "/"
        timing = "/"
    logger.debug(f"[Response] [{method} {status}] {timing}ms <<  {url}")


def network_requestfailed(request: Request):
    url = request.url
    fail = request.failure
    method = request.method
    logger.warning(f"[RequestFailed] [{method} {fail}] << {url}")
