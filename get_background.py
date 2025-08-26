import httpx

async def download_image_with_httpx_auto_redirect(url:str):
    """
    使用httpx库自动处理重定向下载图片
    
    Args:
        url (str): 图片URL
        save_path (str): 保存路径
    """
    try:
        # httpx默认也会自动跟随重定向
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, timeout=30.0)

        # 检查状态码
        if response.status_code == 200:
            Background = response.content
            return Background
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"下载失败: {e}")
        return False
