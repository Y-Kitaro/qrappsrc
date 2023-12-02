import qrcode
import gradio as gr
import pandas as pd

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
def make_qrcode_csv(csv_dir, output_dir):
    qrlist = pd.read_csv(csv_dir, encoding="utf-8")
    qrlist.apply(row_to_QRimg, axis=1, output_dir=output_dir)
    return "Making QRCode completed."

def main():
    with gr.Blocks() as page:
        with gr.Tab("Make QRCode Image"):
            input_text = gr.Textbox()
            output_image = gr.Image(show_label=False, width="50%")
            gr.Interface(fn=make_qrcode, inputs=input_text, outputs=output_image)
        with gr.Tab("Make QRCode Image from CSV"):
            csv_dir = gr.Textbox(label="csv_dir", value="qr.csv")
            output_dir = gr.Textbox(label="output_dir", value="qrimg/")
            result_area = gr.TextArea()
            make_qecode_button = gr.Button("Make QRCode")

        make_qecode_button.click(fn=make_qrcode_csv, inputs=[csv_dir, output_dir], outputs=result_area)
    page.launch(inbrowser=True)

if __name__=="__main__":
    main()