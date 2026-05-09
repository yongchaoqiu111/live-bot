"""
主流程控制 - 四维成交线索闭环
话术+弹幕+商品+销量
"""
import sys
import os
import time
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import LIVE_ROOM_URL
from modules.danmu_crawler import DanmuCrawler
from modules.audio_recorder import AudioRecorder
from modules.speech_to_text import SpeechToText
from modules.cart_crawler import CartCrawler
from modules.sales_crawler import SalesCrawler  # 新增销量抓取
from modules.ai_analyzer import AIAnalyzer
from modules.report_generator import ReportGenerator
from modules.data_storage import DataStorage


def main():
    """主流程"""
    print("=" * 60)
    print("直播竞品复刻实战系统")
    print("四维闭环：话术+弹幕+商品+销量")
    print("=" * 60)
    
    live_url = LIVE_ROOM_URL
    if not live_url:
        live_url = input("请输入直播间URL: ")
    
    print(f"\n目标直播间: {live_url}\n")
    
    # 初始化模块
    danmu_crawler = DanmuCrawler(live_url)
    audio_recorder = AudioRecorder()
    cart_crawler = CartCrawler(live_url)
    sales_crawler = SalesCrawler(live_url)  # 新增
    speech_to_text = SpeechToText()
    ai_analyzer = AIAnalyzer()
    report_generator = ReportGenerator()
    storage = DataStorage()
    
    try:
        # 第1步：清空旧数据
        print("[步骤1] 清空历史数据...")
        storage.clear_all()
        
        # 第2步：启动四维数据采集
        print("\n[步骤2] 启动四维数据采集...")
        
        record_start_ts = audio_recorder.start_recording()
        print(f"录音起始时间戳: {record_start_ts}")
        
        # 后台线程
        threads = []
        
        danmu_thread = threading.Thread(target=danmu_crawler.start)
        danmu_thread.daemon = True
        danmu_thread.start()
        threads.append(danmu_thread)
        
        cart_thread = threading.Thread(target=cart_crawler.start)
        cart_thread.daemon = True
        cart_thread.start()
        threads.append(cart_thread)
        
        sales_thread = threading.Thread(target=sales_crawler.start)  # 新增
        sales_thread.daemon = True
        sales_thread.start()
        threads.append(sales_thread)
        
        print("四维数据采集已启动...\n")
        print("按 Ctrl+C 停止采集并开始分析\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[提示] 用户停止采集")
        
        # 第3步：停止采集
        print("\n[步骤3] 停止数据采集...")
        danmu_crawler.stop()
        cart_crawler.stop()
        sales_crawler.stop()  # 新增
        audio_recorder.stop_recording()
        time.sleep(2)
        
        # 第4步：音频转文字
        print("\n[步骤4] 开始音频转文字...")
        speech_to_text.batch_transcribe(record_start_ts)
        
        # 第5步：LLM三层分析
        print("\n[步骤5] LLM分析（清洗→归因→策略）...")
        analysis_data = ai_analyzer.generate_full_analysis()
        
        # 第6步：生成报告
        print("\n[步骤6] 生成15-20页专业报告...")
        md_report = report_generator.generate_markdown_report(analysis_data)
        excel_report = report_generator.generate_excel_report(analysis_data)
        
        print("\n" + "=" * 60)
        print("✅ 分析完成！")
        print("=" * 60)
        print(f"Markdown报告: {md_report}")
        if excel_report:
            print(f"Excel报告: {excel_report}")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n[错误] 系统异常: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        storage.close()
        print("\n系统已退出")


if __name__ == "__main__":
    main()
