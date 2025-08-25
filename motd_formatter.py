def format_color(color_code: str) -> str:
    """
    将Minecraft颜色代码转换为对应的颜色名称
    
    Args:
        color_code (str): Minecraft颜色代码（单个字符）
    
    Returns:
        str: 对应的颜色名称
    """
    color_map = {
        '0': '#000000',
        '1': '#0000AA',
        '2': '#00AA00',
        '3': '#00AAAA',
        '4': '#AA0000',
        '5': '#AA00AA',
        '6': '#FFAA00',
        '7': '#AAAAAA',
        '8': '#555555',
        '9': '#5555FF',
        'a': '#55FF55',
        'b': '#55FFFF',
        'c': '#FF5555',
        'd': '#FF55FF',
        'e': '#FFFF55',
        'f': '#FFFFFF',
        'g': '#DDD605',
        'r': '#FFFFFF'
    }
    return color_map.get(color_code.lower(), 'white')

def foramt_motd(data: str, weight: int) -> list[tuple[int, str, str]]:
    """
    格式化 MOTD 文本，去除多余的空格和换行符
    
    Args:
        data (str): 原始 MOTD 文本
    
    Returns:
        list: 格式化后的 MOTD 文本
    """
    iter = 0
    character_count = 0
    motd_list = []
    color_state = "#FFFFFF"
    data_size = len(data)
    while iter < data_size:
        if data[iter] == "§":
            if iter + 1 < data_size:
                color = data[iter + 1]
                text = ""
                iter += 2
                character_count += 1
                while iter < data_size and data[iter] != "§" and data[iter] != "\n":
                    text += data[iter]
                    iter += 1
                if color != "l":
                    color_state = format_color(color)
                motd_list.append(((iter - character_count * 2) / data_size * weight, color_state, text))
            else:
                iter += 1
        else:
            text = ""
            while iter < data_size and data[iter] != "§" and data[iter] != "\n":
                text += data[iter]
                iter += 1
            motd_list.append((len(text), "white", text))
    return motd_list
