#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
コンテキストモジュール
アプリケーション全体で共有されるデータと機能を提供します
"""

import os
import json
import logging
import sys
from PyQt6.QtCore import QSettings

from core.models.kobold_cpp import KoboldCpp
from core.models.style_bert_vits2 import StyleBertVits2
from core.models.model_manager import ModelManager
from core.generator import Generator
from utils.path_manager import PathManager

logger = logging.getLogger(__name__)

class Context:
    """
    アプリケーションコンテキストクラス
    
    アプリケーション全体で共有されるデータとオブジェクトを管理します。
    コンポーネント間の依存関係を解決し、状態を共有するために使用されます。
    """
    
    def __init__(self):
        """初期化メソッド"""
        self.logger = logging.getLogger("PyNovelAssistant.Context")
        self.logger.info("コンテキストを初期化しています...")
        
        # 設定の読み込み
        self.settings = QSettings("PyNovelAssistant", "App")
        
        # ディレクトリパスの設定
        self.current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.resources_dir = os.path.join(self.current_dir, "resources")
        self.models_dir = os.path.join(self.resources_dir, "models")
        self.data_dir = os.path.join(self.current_dir, "data")
        
        # パス管理クラスの参照 (インスタンス化せずにクラス自体を参照)
        self.path_manager = PathManager
        
        # ディレクトリの作成
        self._ensure_directories_exist()
        
        # コンポーネントへの参照
        self.main_window = None
        self.input_area = None
        self.output_area = None
        self.gen_area = None
        
        # モデル管理クラスの初期化
        self.model_manager = ModelManager(self)
        self.kobold_cpp = KoboldCpp(self)
        self.style_bert_vits2 = StyleBertVits2(self)
        self.generator = Generator(self)
        
        # 設定データ
        self.config = self._load_config()
        
        # 現在の状態
        self.current_file = None
        self.is_modified = False
        self.is_generating = False
        
        # 生成モデル設定
        self.model_config = {
            "model_type": "default",
            "model_path": "",
            "api_key": "",
            "api_url": "",
            "system_prompt": "あなたは優れた小説の執筆を手伝うAIアシスタントです。"
        }
        
        self.logger.info("コンテキストの初期化が完了しました")
    
    def _ensure_directories_exist(self):
        """必要なディレクトリが存在することを確認"""
        directories = [
            self.resources_dir,
            self.models_dir,
            self.data_dir,
            os.path.join(self.resources_dir, "icons"),
            os.path.join(self.resources_dir, "translations"),
            os.path.join(self.data_dir, "projects"),
            os.path.join(self.data_dir, "backups"),
            os.path.join(self.models_dir, "llm"),
            os.path.join(self.models_dir, "koboldcpp"),
            os.path.join(self.models_dir, "style_bert_vits2")
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                self.logger.info(f"ディレクトリを作成しました: {directory}")
    
    def _load_config(self):
        """構成ファイルの読み込み"""
        config_path = os.path.join(self.data_dir, "config.json")
        default_config = {
            "window": {
                "width": 1200,
                "height": 800,
                "maximized": False
            },
            "editor": {
                "font_family": "Meiryo",
                "font_size": 12,
                "theme": "light",
                "auto_save": True,
                "auto_save_interval": 5  # 分単位
            },
            "generation": {
                "model_type": "local",  # local, api
                "model_name": "default",
                "max_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "repetition_penalty": 1.1
            },
            "recent_files": []
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # デフォルト設定で不足している項目を補完
                    self._merge_configs(config, default_config)
                    self.logger.info("構成ファイルを読み込みました")
                    return config
            except Exception as e:
                self.logger.error(f"構成ファイルの読み込み中にエラーが発生しました: {e}")
        
        self.logger.info("デフォルト構成を使用します")
        return default_config
    
    def _merge_configs(self, config, default_config):
        """設定の辞書をマージする"""
        for key, value in default_config.items():
            if key not in config:
                config[key] = value
            elif isinstance(value, dict) and isinstance(config[key], dict):
                self._merge_configs(config[key], value)
    
    def save_config(self):
        """構成ファイルの保存"""
        config_path = os.path.join(self.data_dir, "config.json")
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            self.logger.info("構成ファイルを保存しました")
            return True
        except Exception as e:
            self.logger.error(f"構成ファイルの保存中にエラーが発生しました: {e}")
            return False
    
    def register_component(self, name, component):
        """コンポーネントの登録"""
        if name in ["main_window", "input_area", "output_area", "gen_area"]:
            setattr(self, name, component)
            self.logger.debug(f"コンポーネントを登録しました: {name}")
        else:
            self.logger.warning(f"不明なコンポーネント名です: {name}")
    
    def update_window_title(self):
        """ウィンドウタイトルの更新"""
        if self.main_window:
            file_name = "無題"
            if self.current_file:
                file_name = os.path.basename(self.current_file)
            
            modified_indicator = "*" if self.is_modified else ""
            title = f"{file_name}{modified_indicator} - PyNovelAssistant"
            self.main_window.setWindowTitle(title)
    
    def set_current_file(self, file_path):
        """現在のファイルを設定"""
        self.current_file = file_path
        if file_path and os.path.exists(file_path):
            # 最近使用したファイルリストを更新
            recent_files = self.config.get("recent_files", [])
            if file_path in recent_files:
                recent_files.remove(file_path)
            recent_files.insert(0, file_path)
            # 最大10個の最近使用したファイルを保持
            self.config["recent_files"] = recent_files[:10]
            self.save_config()
        
        self.update_window_title()
    
    def set_modified(self, modified):
        """変更状態を設定"""
        if self.is_modified != modified:
            self.is_modified = modified
            self.update_window_title()
    
    def get_setting(self, key, default=None):
        """設定値を取得"""
        value = self.settings.value(key, default)
        return value
    
    def set_setting(self, key, value):
        """設定値を設定"""
        self.settings.setValue(key, value)
        self.settings.sync()
    
    def finalize(self):
        """終了処理"""
        self.logger.info("アプリケーションを終了しています...")
        
        # モデルの停止
        if self.kobold_cpp and self.kobold_cpp.is_running():
            self.kobold_cpp.stop()
        
        if self.style_bert_vits2 and self.style_bert_vits2.is_running():
            self.style_bert_vits2.stop()
        
        # 設定の保存
        self.save_config()
        
        self.logger.info("終了処理が完了しました")
    
    def __getitem__(self, key):
        """項目へのアクセス (dict風のインターフェース)"""
        if hasattr(self, key):
            return getattr(self, key)
        return None
    
    def get(self, key, default=None):
        """辞書のようにキーに対する値を取得（存在しない場合はデフォルト値を返す）"""
        value = self.__getitem__(key)
        return value if value is not None else default
    
    def __setitem__(self, key, value):
        """項目の設定 (dict風のインターフェース)"""
        # configに対する操作の場合
        if key.startswith("gen_"):
            # 生成関連の設定はconfigに保存
            if "generation" not in self.config:
                self.config["generation"] = {}
            self.config["generation"][key] = value
        else:
            # 通常の属性として設定
            setattr(self, key, value) 