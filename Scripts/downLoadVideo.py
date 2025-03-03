import yt_dlp
import os

# 检查文件是否存在
def file_exists(filepath):
    return os.path.exists(filepath)

# 下载 MP4 格式视频
def downloads(link):
    video_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': '%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',
    }

    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'cookiefile': 'cookies.txt',
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',
    }

    try:
        # 下载视频
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)  # 获取信息但不下载
            video_title = info_dict.get('title', 'Unknown')
            video_file = f"{video_title}.mp4"
            
            # 检查文件是否存在
            if file_exists(video_file):
                choice = input(f"文件 {video_file} 已存在，是否覆盖？(y/n): ").strip().lower()
                if choice != 'y':
                    print("跳过视频下载。")
                else:
                    ydl.download([link])
                    print(f"视频文件已下载: {video_file}")
            else:
                ydl.download([link])
                print(f"视频文件已下载: {video_file}")
        
        # 提取音频
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)  # 获取信息但不下载
            audio_title = info_dict.get('title', 'Unknown')
            audio_file = f"{audio_title}.mp3"
            
            # 检查文件是否存在
            if file_exists(audio_file):
                choice = input(f"文件 {audio_file} 已存在，是否覆盖？(y/n): ").strip().lower()
                if choice != 'y':
                    print("跳过音频提取。")
                else:
                    ydl.download([link])
                    print(f"音频文件已提取: {audio_file}")
            else:
                ydl.download([link])
                print(f"音频文件已提取: {audio_file}")

    except Exception as e:
        print(f"下载出错: {e}")

# 输入视频链接并调用下载函数
url = input("视频链接：")
downloads(url)