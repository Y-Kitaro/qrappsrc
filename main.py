import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode_utils  # qrcode_utils.pyファイルが同じディレクトリにあると仮定
from PIL import Image, ImageTk
import cv2
import numpy as np

def create_qrcode_window():
    root = tk.Tk()
    root.title("QRコード作成アプリ")
    root.minsize(600, 400)   # 最小ウィンドウサイズ

    # タブ (Notebook) を作成
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # --- Make QR Code タブ ---
    make_qr_frame = ttk.Frame(notebook)
    notebook.add(make_qr_frame, text="QRコード作成")

    # バージョン入力
    version_label = ttk.Label(make_qr_frame, text="バージョン")
    version_label.grid(row=0, column=0, pady=5)
    version_var = tk.IntVar(value=10)  # Use IntVar to store version
    version_entry = ttk.Entry(make_qr_frame, textvariable=version_var, width=5)  # Entry for number input
    version_entry.grid(row=0, column=1, padx=5, pady=5)

    # 誤り訂正レベルドロップダウン
    ecl_label = ttk.Label(make_qr_frame, text="誤り訂正レベル")
    ecl_label.grid(row=0, column=2, pady=5)
    ecl_var = tk.StringVar()
    ecl_dropdown = ttk.Combobox(make_qr_frame, textvariable=ecl_var, state="readonly")
    ecl_dropdown["values"] = list(qrcode_utils.ERROR_CORRECTION_LEVELS.keys())
    ecl_var.set("L")  # デフォルト値設定
    ecl_dropdown.grid(row=0, column=3, columnspan=2, pady=5)

    # 入力テキスト入力欄
    input_text_label = ttk.Label(make_qr_frame, text="入力テキスト")
    input_text_label.grid(row=2, column=0, pady=5)
    input_text = tk.Text(make_qr_frame, height=5) # 複数行入力対応
    input_text.grid(row=2, column=1, columnspan=2, pady=5)

    # QRコード出力ラベル (Image レベルでの出力を Tkinter にはネイティブで持たないのでラベルとして表示)
    output_image = ttk.Label(make_qr_frame)
    output_image.grid(row=3, column=0, columnspan=3, pady=5)

    def make_qr_code():
        text = input_text.get("1.0", tk.END).strip() # 複数行テキスト取得の修正
        version = int(version_var.get())
        ecl = ecl_var.get()
        try:
            qr_image = qrcode_utils.make_qrcode(text, version, qrcode_utils.ERROR_CORRECTION_LEVELS[ecl])
            # Tkinterで表示するためにPhotoImageに変換
            # QRコードをリサイズする処理
            window_width = root.winfo_width()
            window_height = root.winfo_height()
            max_image_size = min(window_width * 0.7, window_height * 0.7)  # ウィンドウ幅の70%または高さの70%の小さい方
            qr_image = qr_image.resize((int(max_image_size), int(max_image_size)), Image.LANCZOS) # LANCZOSで高品質リサイズ
            photo = ImageTk.PhotoImage(qr_image)
            output_image.config(image=photo)
            output_image.image = photo # 参照を保持
        except Exception as e:
            messagebox.showerror("エラー", f"QRコード生成エラー: {e}")

    make_qr_button = ttk.Button(make_qr_frame, text="QRコード生成", command=make_qr_code)
    make_qr_button.grid(row=2, column=3, columnspan=3, pady=10)

    # --- Decode QR Code タブ ---
    decode_qr_frame = ttk.Frame(notebook)
    notebook.add(decode_qr_frame, text="QRコード読み取り")

    # 画像選択ボタンと入力欄
    input_image_label = ttk.Label(decode_qr_frame, text="画像ファイルパス")
    input_image_label.grid(row=0, column=0, pady=5)
    input_image_entry = ttk.Entry(decode_qr_frame, width=40)
    input_image_entry.grid(row=0, column=1, pady=5)

    def select_image():
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if filepath:
            input_image_entry.delete(0, tk.END)
            input_image_entry.insert(0, filepath)

    select_image_button = ttk.Button(decode_qr_frame, text="画像選択", command=select_image)
    select_image_button.grid(row=0, column=2, pady=5)


    # 出力テキストエリア
    output_text = tk.Text(decode_qr_frame, height=5)
    output_text.grid(row=1, column=1, columnspan=3, pady=5)

    def decode_qr():
        filepath = input_image_entry.get()
        try:
            img = Image.open(filepath).convert("RGB") # RGBに変換
            open_cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            decoded_data = qrcode_utils.decode_qrcode(open_cv_image)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, decoded_data)
        except FileNotFoundError:
            messagebox.showerror("エラー", "ファイルが見つかりません")
        except Exception as e:
            messagebox.showerror("エラー", f"QRコード読み取りエラー: {e}")

    decode_button = ttk.Button(decode_qr_frame, text="QRコード読み取り", command=decode_qr)
    decode_button.grid(row=2, column=0, columnspan=3, pady=10)

    # --- Make QR Code from CSV タブ ---
    csv_qr_frame = ttk.Frame(notebook)
    notebook.add(csv_qr_frame, text="CSVからQRコード作成")

    csv_dir_label = ttk.Label(csv_qr_frame, text="CSVファイルパス")
    csv_dir_label.grid(row=0, column=0, pady=5)
    csv_dir_entry_var = tk.StringVar(value="./qrcode/")
    csv_dir_entry = ttk.Entry(csv_qr_frame, textvariable=csv_dir_entry_var, width=40)
    csv_dir_entry.grid(row=0, column=1, pady=5)
    def select_csv():
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            csv_dir_entry.delete(0, tk.END)
            csv_dir_entry.insert(0, filepath)

    select_csv_dir_button = ttk.Button(csv_qr_frame, text="csv選択", command=select_csv)
    select_csv_dir_button.grid(row=0, column=2, pady=5)

    output_dir_label = ttk.Label(csv_qr_frame, text="出力ディレクトリ")
    output_dir_label.grid(row=1, column=0, pady=5)
    output_dir_var = tk.StringVar(value="./qrimg/")  # Use a StringVar
    output_dir_entry = ttk.Entry(csv_qr_frame, textvariable=output_dir_var, width=40)
    output_dir_entry.grid(row=1, column=1, pady=5)

    def select_path():
        directory = filedialog.askdirectory()  # Use askdirectory()
        if directory:
            output_dir_var.set(directory)  # Update the StringVar

    select_imgdir_button = ttk.Button(csv_qr_frame, text="出力ディレクトリ選択", command=select_path)  # Button in the correct frame
    select_imgdir_button.grid(row=1, column=2, pady=5)

    def make_qr_from_csv():
        csv_dir = csv_dir_entry.get()
        output_dir = output_dir_entry.get()
        try:
            result = qrcode_utils.make_qrcode_csv(csv_dir, output_dir)
            messagebox.showinfo("完了", result) # 結果をメッセージボックスで表示
        except FileNotFoundError:
            messagebox.showerror("エラー", "CSVファイルが見つかりません")
        except Exception as e:
            messagebox.showerror("エラー", f"CSVからのQRコード生成エラー: {e}")

    make_qr_csv_button = ttk.Button(csv_qr_frame, text="CSVからQRコード生成", command=make_qr_from_csv)
    make_qr_csv_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_qrcode_window()
