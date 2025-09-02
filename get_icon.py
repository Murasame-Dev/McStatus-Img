from .get_background import download_image_with_httpx_auto_redirect
import asyncio

async def get_icon_image(url: str):
    if url.startswith("http"):
        icon_data = await download_image_with_httpx_auto_redirect(url)
        if icon_data:
            return icon_data
        else:
            return None
    else:
        def read_file(path):
            with open(path, "rb") as f:
                return f.read()
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, read_file, url)
