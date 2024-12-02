
import gradio as gr
from qrcode_utils import make_qrcode, decode_qrcode, make_qrcode_csv, ERROR_CORRECTION_LEVELS

def main():
    with gr.Blocks() as page:
        with gr.Tab("Make QRCode Image"):
            version = gr.Slider(10, minimum=1, maximum=40, step=1)
            error_correction_level_key = gr.Dropdown(list(ERROR_CORRECTION_LEVELS.keys()), label="Error Correction Level")
            error_correction_level_key.value = "L"
            input_text = gr.Textbox("input_Text")
            output_image = gr.Image(show_label=False, width="50%")
            gr.Interface(fn=make_qrcode, inputs=[input_text, version, error_correction_level_key], outputs=output_image)
        with gr.Tab("Decode QRCode Image"):
            input_image = gr.Image()
            output_text = gr.TextArea(label="decoded text")
            gr.Interface(fn=decode_qrcode, inputs=input_image, outputs=output_text)
        with gr.Tab("Make QRCode Image from CSV"):
            csv_dir = gr.Textbox(label="csv_dir", value="qr.csv")
            output_dir = gr.Textbox(label="output_dir", value="qrimg/")
            gr.Interface(fn=make_qrcode_csv, inputs=[csv_dir, output_dir], outputs="text")
    page.launch(inbrowser=True)

if __name__ == "__main__":
    main()
