from get_background import download_image_with_httpx_auto_redirect
from create_image import create_image

# Java版查询模块
from mc_status_api.JavaServerStatus import java_status
# 基岩版查询模块
from mc_status_api.BedrockServerStatus import bedrock_status
# 此API优先解析 srv 记录
from mc_status_api.dnslookup import dns_lookup
# 格式化文本
from mc_status_api.FormatData import format_java_data, format_bedrock_data, format_index, format_java_index, format_bedrock_index

import base64

BACKGROUND_URL = "https://www.loliapi.com/acg/"

def generate_java_status_image(addr: str):
    try:
        ip, type = dns_lookup(addr)
        status = java_status(ip)
        data = format_java_data(ip, type, status)
    except Exception as e:
        print(f"查询服务器时出错: {e}")
        return
    
    background_data = download_image_with_httpx_auto_redirect(BACKGROUND_URL)
    if not background_data:
        background_data = None
    
    motd_list = data['motd'].split("\n")
    text_list = [
        f"ip: {data['ip']}",
        f"type: {data['type']}",
        f"version: {data['version']}",
        f"latency: {round(data['latency'], 2)} ms",
        f"players: {data['players']['online']}/{data['players']['max']}",
    ]

    if status.icon:
        image = create_image(background_data, base64.b64decode(status.icon.split(",")[1]), text_list, motd_list)
    else:
        image = create_image(background_data, None, text_list, motd_list)
    return image

if __name__ == "__main__":
    image = generate_java_status_image("mc.hypixel.net")
    if image:
        image.save("output_image.png")
