# pdf2img_gui.py

import os
from tkinter import Tk, filedialog, messagebox, Label, Entry, Button, StringVar, IntVar, OptionMenu
from pdf2image import convert_from_path

# 指定 poppler 路径
import sys

if hasattr(sys, '_MEIPASS'):
    POPLER_BIN_PATH = os.path.join(sys._MEIPASS, 'poppler', 'bin')
else:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    POPLER_BIN_PATH = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'poppler', 'bin'))


def convert_pdf(pdf_path, output_folder, dpi, img_format):
    try:
        os.makedirs(output_folder, exist_ok=True)
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            poppler_path=POPLER_BIN_PATH  # 手动指定路径
        )
        for i, img in enumerate(images):
            output_path = os.path.join(output_folder, f'page_{i+1}.{img_format}')
            img.save(output_path, img_format.upper())
    except Exception as e:
        messagebox.showerror("错误", f"转换失败: {e}")


def start_conversion():
    pdf_path = pdf_path_var.get()
    output_folder = output_folder_var.get()
    dpi = dpi_var.get()
    img_format = img_format_var.get()

    if not pdf_path or not output_folder:
        messagebox.showwarning("缺失输入", "请选择 PDF 文件和输出目录")
        return

    convert_pdf(pdf_path, output_folder, dpi, img_format)


def choose_pdf():
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if path:
        pdf_path_var.set(path)


def choose_folder():
    path = filedialog.askdirectory()
    if path:
        output_folder_var.set(path)


# GUI 初始化
root = Tk()
root.title("PDF 转图片")

pdf_path_var = StringVar()
output_folder_var = StringVar()
dpi_var = IntVar(value=500)
img_format_var = StringVar(value='jpeg')

Label(root, text="PDF 文件:").grid(row=0, column=0, sticky='e')
Entry(root, textvariable=pdf_path_var, width=40).grid(row=0, column=1)
Button(root, text="选择", command=choose_pdf).grid(row=0, column=2)

Label(root, text="输出文件夹:").grid(row=1, column=0, sticky='e')
Entry(root, textvariable=output_folder_var, width=40).grid(row=1, column=1)
Button(root, text="选择", command=choose_folder).grid(row=1, column=2)

Label(root, text="DPI:").grid(row=2, column=0, sticky='e')
Entry(root, textvariable=dpi_var).grid(row=2, column=1, sticky='w')

Label(root, text="图片格式:").grid(row=3, column=0, sticky='e')
OptionMenu(root, img_format_var, 'png', 'jpeg').grid(row=3, column=1, sticky='w')

Button(root, text="开始转换", command=start_conversion).grid(row=4, column=1, pady=10)

root.mainloop()
