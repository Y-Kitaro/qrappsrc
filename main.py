import os

import qrcode
import cv2
import gradio as gr
import pandas as pd
import numpy as np

# make QRCode Image
def make_qrcode(text, version=10, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=8):
    qr = qrcode.QRCode(version=version, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(text)
    qr.make()
    img = qr.make_image(fillcolor="black")
    return img.get_image()

# apply
def row_to_QRimg(row, output_dir):
    img = make_qrcode(row["text"])
    img.save(f'{output_dir}{row["filename"]}.jpg')

# make QRCode Image from csv
def make_qrcode_csv(csv_dir, output_dir, progress=gr.Progress()):
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

    
    for i in progress.tqdm(range(len(qrlist))):
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

def main():
    with gr.Blocks() as page:
        with gr.Tab("Make QRCode Image"):
            version = gr.Slider(10, minimum=1, maximum=40, step=1)
            input_text = gr.Textbox("input_Text")
            output_image = gr.Image(show_label=False, width="50%")
            gr.Interface(fn=make_qrcode, inputs=[input_text, version] , outputs=output_image)
        with gr.Tab("Decode QRCode Image"):
            input_image = gr.Image()
            output_text = gr.TextArea(label="decoded text")
            gr.Interface(fn=decode_qrcode, inputs=input_image, outputs=output_text)
        with gr.Tab("Make QRCode Image from CSV"):
            csv_dir = gr.Textbox(label="csv_dir", value="qr.csv")
            output_dir = gr.Textbox(label="output_dir", value="qrimg/")
            gr.Interface(fn=make_qrcode_csv, inputs=[csv_dir, output_dir], outputs="text")
    page.launch(inbrowser=True)

if __name__=="__main__":
    main()