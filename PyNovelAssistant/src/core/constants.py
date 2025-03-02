#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
定数モジュール
アプリケーション全体で使用する定数を定義します
"""

class Constants:
    """定数クラス"""
    
    # アプリケーション情報
    APP_NAME = "PyNovelAssistant"
    APP_VERSION = "0.1.0"
    
    # ファイル関連
    DEFAULT_EXT = ".txt"
    RECENT_FILES_MAX = 10
    
    # UI関連
    AREA_MIN_SIZE = 200
    INPUT_FONT_SIZE = 12
    OUTPUT_FONT_SIZE = 12
    
    # リポジトリURL
    REPO_URL = "https://github.com/yourusername/PyNovelAssistant"
    
    # モデル関連
    DEFAULT_CONTEXT_SIZE = 4096
    DEFAULT_GPU_LAYERS = 33
    
    # 生成関連
    MIN_TEMPERATURE = 0.1  # 最小温度
    MAX_TEMPERATURE = 2.0  # 最大温度
    MIN_TOP_P = 0.0  # 最小top_p
    MAX_TOP_P = 1.0  # 最大top_p
    MIN_TOP_K = 1  # 最小top_k
    MAX_TOP_K = 100  # 最大top_k
    MIN_REP_PENALTY = 1.0  # 最小繰り返しペナルティ
    MAX_REP_PENALTY = 2.0  # 最大繰り返しペナルティ
    
    @classmethod
    def init(cls, ctx):
        """コンテキストを使用して初期化"""
        # ここでコンテキストから読み込んだ設定に基づいて定数を更新できます
        pass 