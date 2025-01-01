
import os
import qrcode
import cv2
import pandas as pd
import numpy as np

ERROR_CORRECTION_LEVELS = {
    "L": qrcode.ERROR_CORRECT_L,
    "M": qrcode.ERROR_CORRECT_M,
    "Q": qrcode.ERROR_CORRECT_Q,
    "H": qrcode.ERROR_CORRECT_H,
}

# make QRCode Image
def make_qrcode(text, version=10, error_correction_level_key="L", box_size=10, border=8):
    error_correction_level = ERROR_CORRECTION_LEVELS.get(error_correction_level_key, qrcode.ERROR_CORRECT_L)
    qr = qrcode.QRCode(version=version, error_correction=error_correction_level, box_size=box_size, border=border)
    qr.add_data(text)
    qr.make()
    img = qr.make_image(fillcolor="black")
    return img.get_image()

# apply
def row_to_QRimg(row, output_dir):
    img = make_qrcode(row["text"])
    img.save(f'{output_dir}{row["filename"]}.jpg')

# make QRCode Image from csv
def make_qrcode_csv(csv_dir, output_dir):
    # Check paths exist
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
            row_to_QRimg(qrlist.iloc[i], output_dir=output_dir)
        except Exception as e:
            return f"Failed to create QR code for row {i}. Please check the data in the CSV file."

    return "QR code creation completed successfully."

def decode_qrcode(input_image):
    open_cv_image = np.array(input_image) 
    img = open_cv_image[:, :, ::-1].copy() 

    detector = cv2.QRCodeDetectorAruco()

    data, _, _ = detector.detectAndDecode(img)

    if data:
        return data
    else:
        return "QR Code not detected"
