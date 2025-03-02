#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
テキスト生成クラス
AIモデルを使用したテキスト生成を管理します
"""

import threading
import time
import traceback

from utils.job_queue import JobQueue


class Generator:
    """テキスト生成クラス"""
    
    def __init__(self, ctx):
        """初期化"""
        self.ctx = ctx
        self.enabled = False
        self.generating = False
        self.job_queue = JobQueue()
        self.last_update_time = time.time()
    
    def update(self):
        """定期更新処理"""
        if not self.enabled or self.generating:
            return
        
        # 指定された時間間隔でテキスト生成を実行
        current_time = time.time()
        if (current_time - self.last_update_time) >= 0.1:  # 100ms
            self.last_update_time = current_time
            self.generate()
    
    def generate(self):
        """テキスト生成を実行"""
        if self.generating:
            return
        
        # 生成中フラグを設定
        self.generating = True
        
        # 別スレッドで生成処理を実行
        threading.Thread(target=self._generate_thread, daemon=True).start()
    
    def _generate_thread(self):
        """生成スレッド処理"""
        try:
            # 入力テキストの取得
            input_text = self.ctx.main_window.input_area.get_text()
            if not input_text:
                self.generating = False
                return
            
            # テキスト生成パラメータの設定
            params = {
                "prompt": input_text,
                "max_new_tokens": self.ctx["gen_max_tokens"],
                "temperature": self.ctx["gen_temperature"],
                "top_p": self.ctx["gen_top_p"],
                "top_k": self.ctx["gen_top_k"],
                "repetition_penalty": self.ctx["gen_repetition_penalty"],
                "stop": self.ctx["gen_stop_strings"],
            }
            
            # KoboldCPPモデルを使用してテキスト生成
            result = self.ctx.kobold_cpp.generate(params)
            
            if result and "text" in result:
                generated_text = result["text"]
                
                # 出力エリアに表示
                self.ctx.main_window.output_area.add_text(generated_text)
                
                # 自動継続の場合、入力エリアに追加
                if self.ctx.get("gen_auto_continue", False):
                    new_text = input_text + generated_text
                    self.ctx.main_window.input_area.set_text(new_text)
            
            # ウィンドウタイトルの更新
            self.ctx.main_window.update_title()
            
        except Exception as e:
            print(f"生成エラー: {e}")
            traceback.print_exc()
        
        finally:
            # 生成中フラグをクリア
            self.generating = False
    
    def start(self):
        """生成を開始"""
        self.enabled = True
        self.ctx.main_window.update_title()
        print("テキスト生成を開始しました")
    
    def stop(self):
        """生成を停止"""
        self.enabled = False
        self.ctx.main_window.update_title()
        print("テキスト生成を停止しました")
    
    def toggle(self):
        """生成の開始/停止を切り替え"""
        if self.enabled:
            self.stop()
        else:
            self.start() 