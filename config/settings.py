"""
项目配置文件
"""
import os

# OpenAI API密钥（必需）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-api-key")

# 直播间URL（运行时可输入）
LIVE_ROOM_URL = ""

# Whisper模型路径
WHISPER_MODEL = "large-v3"

# 音频配置
AUDIO_CHUNK_DURATION = 60  # 60秒切片
AUDIO_FORMAT = "mp3"

# 抓取间隔
DANMU_INTERVAL = 5  # 弹幕5秒
SALES_INTERVAL = 30  # 销量30秒
PRODUCT_INTERVAL = 30  # 商品30秒

# 数据库配置
DB_PATH = "data/live_analysis.db"

# 报告输出
REPORT_DIR = "reports"
