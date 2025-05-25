
import os
import io
import base64
import qrcode
import cv2
import pandas as pd
import numpy as np
import webview
from PIL import Image

ERROR_CORRECTION_LEVELS = {
        "L": qrcode.ERROR_CORRECT_L,
        "M": qrcode.ERROR_CORRECT_M,
        "Q": qrcode.ERROR_CORRECT_Q,
        "H": qrcode.ERROR_CORRECT_H,
    }

class Qrcode_utils:

    def set_window(self, window):
        self.window = window

    def open_file(self, file_types=(), allow_multiple=False):
        result = self.window.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=file_types,
            allow_multiple=allow_multiple
        )
        # pywebviewはタプルで返すため、扱いやすいように整形する
        if not result:
            return None
        return list(result) if allow_multiple else result[0]

    def select_folder(self):
        result = self.window.create_file_dialog(
            webview.FOLDER_DIALOG,
        )
        # フォルダ選択は常に単一のパス（のタプル）が返る
        return result[0] if result else None

    # make QRCode Image
    def make_qrcode(self, text, version=10, error_correction_level_key="L", box_size=10, border=8):
        error_correction_level = ERROR_CORRECTION_LEVELS.get(error_correction_level_key, qrcode.ERROR_CORRECT_L)
        qr = qrcode.QRCode(version=version, error_correction=error_correction_level, box_size=box_size, border=border)
        qr.add_data(text)
        qr.make()
        img = qr.make_image(fillcolor="black")
        return img.get_image()
    
    def make_qrcode_base64(self, text, version=10, error_correction_level_key="L", box_size=10, border=8):
        qr_img = self.make_qrcode(text, version, error_correction_level_key, box_size, border)

        buffered = io.BytesIO()
        qr_img.save(buffered, format="PNG")
        # Base64文字列にエンコード
        qr_img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{qr_img_str}"

    # apply
    def row_to_QRimg(self, row, output_dir):
        img = self.make_qrcode(row["text"])
        print(os.path.join(output_dir, f'{row["filename"]}.jpg'))
        img.save(os.path.join(output_dir, f'{row["filename"]}.jpg'))

    # make QRCode Image from csv
    def make_qrcode_csv(self, csv_dir, output_dir):
        # Check paths exist
        print(csv_dir)
        print(output_dir)
        if not os.path.exists(csv_dir):
            return "CSV file not found. Please check the path to the CSV file."
        
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        except Exception as e:
            return "Failed to create output directory. Please check the permissions and path to the output directory."
        
        try:
            qrlist = pd.read_csv(csv_dir, encoding="utf-8")
        except Exception as e:
            return "Error in reading the CSV file. Please ensure the CSV file is in the correct format."
        
        for i in range(len(qrlist)):
            try:
                self.row_to_QRimg(qrlist.iloc[i], output_dir=output_dir)
            except Exception as e:
                return f"Failed to create QR code for row {i}. Please check the data in the CSV file."

        return "QR code creation completed successfully."

    def decode_qrcode(self):
        qrcode_path = self.open_file()
        try:
            img = Image.open(qrcode_path).convert("RGB")
            open_cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(e)
            pass
        open_cv_image = np.array(open_cv_image) 
        img = open_cv_image[:, :, ::-1].copy() 

        detector = cv2.QRCodeDetectorAruco()

        decoded_text, _, _ = detector.detectAndDecode(img)

        if decoded_text:
            return decoded_text
        else:
            return "QR Code not detected"
