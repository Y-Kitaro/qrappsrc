import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode_utils
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

# 定数定義
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400
IMAGE_SCALE_FACTOR = 0.7
DEFAULT_CSV_PATH = "./qrcode_template.csv"
DEFAULT_OUTPUT_DIR = "./qrimg/"
SUPPORTED_IMAGE_TYPES = [("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
SUPPORTED_CSV_TYPES = [("CSV files", "*.csv")]

class QRCodeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QRコード作成アプリ")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.create_tabs()

    def create_tabs(self):
        self.create_qrcode_tab()
        self.create_decode_qr_tab()
        self.create_csv_qr_tab()

    def create_qrcode_tab(self):
        make_qr_frame = ttk.Frame(self.notebook)
        self.notebook.add(make_qr_frame, text="QRコード作成")

        version_label = ttk.Label(make_qr_frame, text="バージョン")
        version_label.grid(row=0, column=0, pady=5)
        self.version_var = tk.IntVar(value=10)
        version_entry = ttk.Entry(make_qr_frame, textvariable=self.version_var, width=5)
        version_entry.grid(row=0, column=1, padx=5, pady=5)

        ecl_label = ttk.Label(make_qr_frame, text="誤り訂正レベル")
        ecl_label.grid(row=0, column=2, pady=5)
        self.ecl_var = tk.StringVar(value="L")
        ecl_dropdown = ttk.Combobox(make_qr_frame, textvariable=self.ecl_var, state="readonly", values=list(qrcode_utils.ERROR_CORRECTION_LEVELS.keys()))
        ecl_dropdown.grid(row=0, column=3, columnspan=2, pady=5)

        input_text_label = ttk.Label(make_qr_frame, text="入力テキスト")
        input_text_label.grid(row=1, column=0, pady=5)
        self.input_text = tk.Text(make_qr_frame, height=5)
        self.input_text.grid(row=1, column=1, columnspan=4, pady=5)

        self.output_image = ttk.Label(make_qr_frame)
        self.output_image.grid(row=2, column=0, columnspan=5, pady=5)

        make_qr_button = ttk.Button(make_qr_frame, text="QRコード生成", command=self.make_qr_code)
        make_qr_button.grid(row=3, column=0, columnspan=5, pady=10)

    def make_qr_code(self):
        text = self.input_text.get("1.0", tk.END).strip()
        version = int(self.version_var.get())
        ecl = self.ecl_var.get()
        try:
            qr_image = qrcode_utils.make_qrcode(text, version, qrcode_utils.ERROR_CORRECTION_LEVELS[ecl])
            qr_image = self.resize_qr_image(qr_image)
            self.display_qr_image(qr_image)
        except Exception as e:
            messagebox.showerror("エラー", f"QRコード生成エラー: {e}")

    def create_decode_qr_tab(self):
        decode_qr_frame = ttk.Frame(self.notebook)
        self.notebook.add(decode_qr_frame, text="QRコード読み取り")

        input_image_label = ttk.Label(decode_qr_frame, text="画像ファイルパス")
        input_image_label.grid(row=0, column=0, pady=5)
        self.input_image_entry = ttk.Entry(decode_qr_frame, width=40)
        self.input_image_entry.grid(row=0, column=1, pady=5)

        select_image_button = ttk.Button(decode_qr_frame, text="画像選択", command=lambda: self.select_file(self.input_image_entry, SUPPORTED_IMAGE_TYPES))
        select_image_button.grid(row=0, column=2, pady=5)

        self.output_text = tk.Text(decode_qr_frame, height=5)
        self.output_text.grid(row=1, column=0, columnspan=3, pady=5)

        decode_button = ttk.Button(decode_qr_frame, text="QRコード読み取り", command=self.decode_qr)
        decode_button.grid(row=2, column=0, columnspan=3, pady=10)

    def decode_qr(self):
        filepath = self.input_image_entry.get()
        try:
            img = Image.open(filepath).convert("RGB")
            open_cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            decoded_data = qrcode_utils.decode_qrcode(open_cv_image)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, decoded_data)
        except FileNotFoundError:
            messagebox.showerror("エラー", "ファイルが見つかりません")
        except Exception as e:
            messagebox.showerror("エラー", f"QRコード読み取りエラー: {e}")

    def create_csv_qr_tab(self):
        csv_qr_frame = ttk.Frame(self.notebook)
        self.notebook.add(csv_qr_frame, text="CSVからQRコード作成")

        csv_dir_label = ttk.Label(csv_qr_frame, text="CSVファイルパス")
        csv_dir_label.grid(row=0, column=0, pady=5)
        self.csv_dir_entry = ttk.Entry(csv_qr_frame, width=40)
        self.csv_dir_entry.insert(0, DEFAULT_CSV_PATH)
        self.csv_dir_entry.grid(row=0, column=1, pady=5)

        select_csv_dir_button = ttk.Button(csv_qr_frame, text="csv選択", command=lambda: self.select_file(self.csv_dir_entry, SUPPORTED_CSV_TYPES))
        select_csv_dir_button.grid(row=0, column=2, pady=5)

        output_dir_label = ttk.Label(csv_qr_frame, text="出力ディレクトリ")
        output_dir_label.grid(row=1, column=0, pady=5)
        self.output_dir_entry = ttk.Entry(csv_qr_frame, width=40)
        self.output_dir_entry.insert(0, DEFAULT_OUTPUT_DIR)
        self.output_dir_entry.grid(row=1, column=1, pady=5)

        select_imgdir_button = ttk.Button(csv_qr_frame, text="出力ディレクトリ選択", command=lambda: self.select_directory(self.output_dir_entry))
        select_imgdir_button.grid(row=1, column=2, pady=5)

        make_qr_csv_button = ttk.Button(csv_qr_frame, text="CSVからQRコード生成", command=self.make_qr_from_csv)
        make_qr_csv_button.grid(row=2, column=0, columnspan=3, pady=10)

    def make_qr_from_csv(self):
        csv_dir = self.csv_dir_entry.get()
        output_dir = self.output_dir_entry.get()
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            result = qrcode_utils.make_qrcode_csv(csv_dir, output_dir)
            messagebox.showinfo("完了", result)
        except FileNotFoundError:
            messagebox.showerror("エラー", "CSVファイルが見つかりません")
        except Exception as e:
            messagebox.showerror("エラー", f"CSVからのQRコード生成エラー: {e}")

    def resize_qr_image(self, qr_image):
        """QRコード画像をウィンドウサイズに合わせてリサイズする"""
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        max_image_size = min(window_width * IMAGE_SCALE_FACTOR, window_height * IMAGE_SCALE_FACTOR)
        return qr_image.resize((int(max_image_size), int(max_image_size)), Image.LANCZOS)

    def display_qr_image(self, qr_image):
        """QRコード画像をTkinterのラベルに表示する"""
        photo = ImageTk.PhotoImage(qr_image)
        self.output_image.config(image=photo)
        self.output_image.image = photo  # 参照を保持

    def select_file(self, entry, filetypes):
        """ファイル選択ダイアログを開き、選択されたファイルのパスをエントリーに設定する"""
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            entry.delete(0, tk.END)
            entry.insert(0, filepath)

    def select_directory(self, entry):
        """ディレクトリ選択ダイアログを開き、選択されたディレクトリのパスをエントリーに設定する"""
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

def main():
    app = QRCodeApp()
    app.mainloop()

if __name__ == "__main__":
    main()