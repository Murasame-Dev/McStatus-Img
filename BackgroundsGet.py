import httpx
import os

def download_image_with_httpx_auto_redirect(url, save_path):
    """
    使用httpx库自动处理重定向下载图片
    
    Args:
        url (str): 图片URL
        save_path (str): 保存路径
    """
    try:
        # httpx默认也会自动跟随重定向
        with httpx.Client(follow_redirects=True) as client:
            response = client.get(url, timeout=30.0)
        
        # 检查状态码
        if response.status_code == 200:
            # 确保保存目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 写入文件
            with open(save_path, 'wb') as f:
                f.write(response.content)

            Background = response.content

            print(f"图片已成功保存到: {save_path}")
            print(f"最终URL: {response.url}")  # 显示最终重定向后的URL
            return Background
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"下载失败: {e}")
        return False

# 使用示例
if __name__ == "__main__":
    image_url = "https://www.loliapi.com/acg/"
    save_path = "images/downloaded_image.jpg"
    download_image_with_httpx_auto_redirect(image_url, save_path)