"""
销量抓取模块
每30秒抓取商品卡片"已售"数量，计算销量增量
"""
import time
from playwright.sync_api import sync_playwright
from utils.time_utils import get_current_timestamp
from modules.data_storage import DataStorage


class SalesCrawler:
    def __init__(self, live_url):
        self.live_url = live_url
        self.storage = DataStorage()
        self.browser = None
        self.page = None
        self.is_running = False
        self.last_sales_data = {}  # 上次抓取的销量数据
    
    def start(self):
        """启动销量抓取"""
        print("[销量] 开始抓取...")
        self.is_running = True
        
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True)
            self.page = self.browser.new_page()
            self.page.goto(self.live_url)
            self.page.wait_for_load_state("networkidle")
            
            try:
                while self.is_running:
                    self._capture_sales()
                    time.sleep(30)  # 30秒抓取一次
            except Exception as e:
                print(f"[销量] 抓取异常: {e}")
            finally:
                self.stop()
    
    def _capture_sales(self):
        """抓取当前销量数据"""
        try:
            # 注意：不同平台DOM结构不同，需根据实际调整选择器
            product_elements = self.page.query_selector_all(".product-item")
            
            ts = get_current_timestamp()
            current_sales = {}
            
            for element in product_elements:
                try:
                    name = element.query_selector(".product-name").inner_text().strip()
                    sales_text = element.query_selector(".sales-count").inner_text().strip()
                    
                    # 提取数字（如"已售1234" → 1234）
                    import re
                    sales_num = int(re.search(r'\d+', sales_text).group()) if sales_text else 0
                    
                    current_sales[name] = sales_num
                    
                    # 计算销量增量
                    if name in self.last_sales_data:
                        delta = sales_num - self.last_sales_data[name]
                        if delta > 0:
                            sales_event = {
                                "type": "sales",
                                "ts": ts,
                                "content": f"{name}|{delta}",
                                "tag": str(delta)
                            }
                            self.storage.save_event(sales_event)
                            print(f"[销量] {name} +{delta}单")
                
                except Exception as e:
                    continue
            
            # 更新上次数据
            self.last_sales_data = current_sales
        
        except Exception as e:
            print(f"[销量] 解析失败: {e}")
    
    def stop(self):
        """停止抓取"""
        self.is_running = False
        if self.browser:
            self.browser.close()
        print("[销量] 已停止")
