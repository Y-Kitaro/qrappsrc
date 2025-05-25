import webview
import os
from qrcode_utils import Qrcode_utils

# Reactアプリのパス
frontend_dir = os.path.join(os.path.dirname(__file__), 'webui', 'dist')
index_html = os.path.join(frontend_dir, 'index.html')

if __name__ == '__main__':
    qrcode_api = Qrcode_utils()

    # ウィンドウを作成
    window = webview.create_window(
        'QRコードツール',
        url=index_html,  # Reactのパスを指定
        js_api=qrcode_api,  # JavaScriptから呼び出せるPythonAPIを登録
        width=800,
        height=600
    )

    qrcode_api.set_window(window)
    # アプリケーションを開始
    webview.start()