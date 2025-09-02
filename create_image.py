from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from PIL.ImageColor import getrgb
import asyncio

from .motd_formatter import foramt_motd
from .get_background import download_image_with_httpx_auto_redirect

BACKGROUND_URL = "https://www.loliapi.com/acg/"
DEFAULT_ICON = "./minecraft-creeper-face.png"

def create_background(input: bytes, width: int, height: int):
    background = Image.open(BytesIO(input))
    w1, h1, w2, h2 = background.getbbox()
    midw = (w1 + w2) // 2
    midh = (h1 + h2) // 2
    rheight = int(height / width * w2)
    rwidth = w2
    if rheight > h2:
        rwidth = int(width / height * h2)
        rheight = h2
    
    background = background.crop((midw - int(rwidth / 2),
                                  midh - int(rheight / 2),
                                  midw + int(rwidth / 2),
                                  midh + int(rheight / 2)))
    background = background.resize((width, height),
                                   Image.Resampling.LANCZOS)

    blurred_background = background.filter(ImageFilter.GaussianBlur(radius=5))
    
    image = blurred_background
    return image

def draw_text_with_shadow(image: Image.Image,
                          text: str,
                          posx: int,
                          posy: int,
                          font_size: int):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("./MiSans-Bold.ttf", font_size)
    draw.text((posx + 2, posy + 2), text, font=font, fill='black')
    draw.text((posx, posy), text, font=font, fill='white')

def draw_motd_text_with_shadow(image: Image.Image,
                               text: str,
                               posx: int,
                               posy: int,
                               font_size: int):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("./MiSans-Bold.ttf", font_size)
    w1, _, w2, _ = draw.textbbox((0, 0), text.strip(), font=font)
    weight = w2 - w1
    motd_list = foramt_motd(text.strip(), weight)
    for pos, color, text in motd_list:
        w1, _, w2, _ = draw.textbbox((0, 0), text, font=font)
        weight = w2 - w1
        draw.text((posx + pos + 1 - weight, posy + 1), text, font=font, fill='black')
        draw.text((posx + pos - weight, posy), text, font=font, fill=getrgb(color))

def create_image(background: bytes,
                 icon: str | None,
                 text_list: list[str],
                 motd_list: list[str]):
    # 图片尺寸
    width, height = 1200, 400
    if (len(text_list) + len(motd_list)) * 20 + 20 > height:
        height = (len(text_list) + len(motd_list)) * 20 + 20
    else:
        font_size = height // 12
    if font_size * 20 > width - width // 2.5:
        font_size = (width - width // 2.5) // 20
    
    try:
        image = create_background(background, width, height)
    except FileNotFoundError:
        image = Image.new('RGB', (width, height), color='orange')
    
    # 添加半透明蒙版层以增强文字可读性
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 80))  # 半透明黑色蒙版
    image.paste(overlay, (0, 0), overlay)

    if width // 2 > height:
        small_size = int(height * 0.8)
    else:
        small_size = width // 3
    if icon == None:
        small_image = Image.new('RGBA', (small_size, small_size), color='gray')
    else:
        small_image = Image.open(BytesIO(icon)).resize((small_size, small_size),
                                                       Image.Resampling.LANCZOS)

    image.paste(small_image, (30, height // 2 - small_size // 2))

    text_list_size = len(text_list)
    motd_list_size = len(motd_list)
    start_posy = height / 2 - (text_list_size + motd_list_size) / 2 * font_size * 1.2
    for i in range(motd_list_size):
        draw_motd_text_with_shadow(image,
                                   motd_list[i],
                                   width // 2.5,
                                   start_posy + font_size * 1.2 * i,
                                   int(font_size * 0.8))
    for i in range(text_list_size):
        draw_text_with_shadow(image,
                              text_list[i],
                              width // 2.5,
                              start_posy + font_size * 1.2 * (i + motd_list_size),
                              font_size)
    
    return image

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
