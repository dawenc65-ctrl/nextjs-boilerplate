"""
数据获取模块
文件名: data_fetcher.py
功能: 从Binance获取实时市场数据
"""

import ccxt
import pandas as pd
import time
import logging

class DataFetcher:
    def __init__(self, config):
        self.setup_exchange(config)
        self.symbol = config['trading']['symbol']
        self.timeframe = config['trading']['timeframe']
    
    def setup_exchange(self, config):
        """设置交易所连接"""
        self.exchange = ccxt.binance({
            'apiKey': config['binance']['api_key'],
            'secret': config['binance']['api_secret'],
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}  # 如果是合约交易
        })
