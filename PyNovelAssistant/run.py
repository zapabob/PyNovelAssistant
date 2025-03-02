#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyNovelAssistant 実行スクリプト
小説作成支援アプリケーションを起動します
"""

import os
import sys
import traceback
from pathlib import Path

def setup_environment():
    """環境設定を行います"""
    # スクリプトのディレクトリを取得
    script_dir = Path(__file__).resolve().parent
    
    # srcディレクトリをPYTHONPATHに追加
    src_dir = script_dir / "src"
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))
        print(f"✓ ソースディレクトリをPYTHONPATHに追加しました: {src_dir}")
    else:
        print(f"✗ ソースディレクトリが見つかりません: {src_dir}")
        return False
    
    return True

def find_sample_files():
    """サンプルファイルを検索します"""
    script_dir = Path(__file__).resolve().parent
    
    # サンプルディレクトリの検索
    sample_dir = script_dir / "sample"
    
    if not sample_dir.exists():
        return None, []
        
    # テキストファイルを検索
    sample_files = list(sample_dir.glob("*.txt"))
    
    return sample_dir, sample_files

def run_application():
    """アプリケーションを実行します"""
    try:
        from core.py_novel_assistant import PyNovelAssistant
        print("アプリケーションを起動しています...")
        app = PyNovelAssistant()
        app.run()
        return True
    except ImportError as e:
        print(f"✗ アプリケーションの起動に失敗しました: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"✗ エラーが発生しました: {e}")
        traceback.print_exc()
        return False

def main():
    """メイン関数"""
    print("=" * 60)
    print("PyNovelAssistant 実行スクリプト")
    print("=" * 60)
    
    # 環境設定
    if not setup_environment():
        print("環境設定に失敗しました。")
        input("何かキーを押して終了...")
        return 1
    
    # サンプルファイルの検索
    sample_dir, sample_files = find_sample_files()
    
    if sample_files:
        print(f"サンプルディレクトリ: {sample_dir}")
        print(f"サンプルファイル ({len(sample_files)}件):")
        for file in sample_files:
            print(f"  - {file.name}")
    else:
        print("サンプルファイルは見つかりませんでした。")
    
    print("-" * 60)
    print("PyNovelAssistant を起動します。")
    
    # アプリケーションの実行
    success = run_application()
    
    if not success:
        print("アプリケーションの実行に失敗しました。")
        input("何かキーを押して終了...")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 