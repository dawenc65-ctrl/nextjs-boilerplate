#!/usr/bin/env python3
"""
AI交易机器人主程序
文件名: main.py
功能: 协调各个模块，实现自动化交易
"""

import time
import json
import logging
from data_fetcher import DataFetcher
from ai_predictor import AIPredictor
from trade_executor import TradeExecutor
from risk_manager import RiskManager
from logger import setup_logging

class TradingBot:
    def __init__(self):
        self.setup_components()
        self.position = None
        self.balance = 0
        
    def setup_components(self):
        """初始化各个组件"""
        # 加载配置
        with open('config/keys.json', 'r') as f:
            self.api_config = json.load(f)
        with open('config/trading_config.json', 'r') as f:
            self.trading_config = json.load(f)
            
        # 初始化模块
        self.data_fetcher = DataFetcher(self.api_config)
        self.ai_predictor = AIPredictor()
        self.trade_executor = TradeExecutor(self.api_config)
        self.risk_manager = RiskManager(self.trading_config)
        
        logging.info("AI交易机器人初始化完成")
    
    def run(self):
        """主运行循环"""
        logging.info("开始运行AI交易机器人")
        
        while True:
            try:
                self.trading_cycle()
                time.sleep(self.trading_config['check_interval'])
                
            except KeyboardInterrupt:
                logging.info("用户中断程序")
                break
            except Exception as e:
                logging.error(f"运行错误: {e}")
                time.sleep(10)
    
    def trading_cycle(self):
        """单个交易周期"""
        # 获取数据 → AI分析 → 风险管理 → 执行交易
        data = self.data_fetcher.get_realtime_data()
        signal, confidence = self.ai_predictor.analyze(data)
        
        if self.risk_manager.approve_trade(signal, confidence, self.position):
            self.execute_trade(signal, confidence)

if __name__ == "__main__":
    setup_logging()
    bot = TradingBot()
    bot.run()
