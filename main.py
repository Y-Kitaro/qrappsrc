import webview
import os
import sys
from qrcode_utils import Qrcode_utils

def get_index_html_path():
    """
    実行ファイルからのindex.htmlの相対パス
    """
    if getattr(sys, 'frozen', False):
        # sys.executable はEXE自身のパスを指す
        index_html_path = os.path.join(os.path.dirname(sys.executable), os.path.join('webui', 'index.html'))
    else:
        # __file__ は現在のスクリプトのパス
        frontend_dir = os.path.join(os.path.dirname(__file__), 'webui', 'dist')
        index_html_path = os.path.join(frontend_dir, 'index.html')
    
    return index_html_path

# Reactアプリのパス
index_html = get_index_html_path()

class Api:
    def __init__(self):
        self.qrcode_utils = None
        
    def open_file(self, file_types=(), allow_multiple=False):
        result = _window.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=file_types,
            allow_multiple=allow_multiple
        )
        # pywebviewはタプルで返すため、扱いやすいように整形する
        if not result:
            return None
        return list(result) if allow_multiple else result[0]

    def select_folder(self):
        result = _window.create_file_dialog(
            webview.FOLDER_DIALOG,
        )
        # フォルダ選択は常に単一のパス（のタプル）が返る
        return result[0] if result else None

if __name__ == '__main__':
    api = Api()
    api.qrcode_utils = Qrcode_utils(api)

    # ウィンドウを作成
    _window = webview.create_window(
        'QRコードツール',
        url=index_html,  # Reactのパスを指定
        js_api=api,  # JavaScriptから呼び出せるPythonAPIを登録
        width=800,
        height=600
    )
    # アプリケーションを開始
    webview.start()