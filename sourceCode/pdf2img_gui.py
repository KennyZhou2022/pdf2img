import os
import sys
import threading
from tkinter import Tk, Label, Button, filedialog, StringVar, Entry, messagebox
from tkinter.ttk import Progressbar, Combobox

from pdf2image import convert_from_path
from PIL import Image


def get_poppler_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'poppler', 'bin')
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'poppler', 'bin'))


class PDF2ImageApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF 转图片工具")
        master.geometry("600x250")  # 设置窗口初始大小
        self.pdf_path = StringVar()
        self.output_folder = StringVar()
        self.dpi = StringVar(value="500")
        self.img_format = StringVar(value="jpeg")
        self.row_pad = 3
        root.columnconfigure(1, weight=1)
        master.columnconfigure(1, weight=1)

        # PDF 文件选择
        Label(master, text="选择 PDF 文件:").grid(row=0, column=0, padx=(10, 5), sticky="e", pady=self.row_pad)
        Entry(master, textvariable=self.pdf_path, width=40).grid(row=0, column=1, padx=5, sticky="ew", pady=self.row_pad)
        Button(master, text="浏览", command=self.browse_pdf).grid(row=0, column=2, padx=(5, 10), pady=self.row_pad)

        # 输出路径
        Label(master, text="输出文件夹:").grid(row=1, column=0, padx=(10, 5), sticky="e", pady=self.row_pad)
        Entry(master, textvariable=self.output_folder, width=40).grid(row=1, column=1, padx=5, sticky="ew", pady=self.row_pad)
        Button(master, text="更改", command=self.browse_output_folder).grid(row=1, column=2, padx=(5, 10), pady=self.row_pad)

        # DPI 输入
        Label(master, text="DPI:").grid(row=2, column=0,  padx=(10, 5), sticky="e", pady=self.row_pad)
        Entry(master, textvariable=self.dpi).grid(row=2, column=1, padx=(5, 10), sticky="w", pady=self.row_pad)

        # 图像格式选择
        Label(master, text="图片格式:").grid(row=3, column=0,  padx=(10, 5), sticky="e", pady=self.row_pad)
        self.format_box = Combobox(master, textvariable=self.img_format, values=["png", "jpeg", "bmp", "tiff"], state="readonly")
        self.format_box.grid(row=3, column=1, sticky="w", padx=5, pady=self.row_pad)

        # 进度条 + 状态
        self.progress = Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10, padx=80)

        self.status_label = Label(master, text="")
        self.status_label.grid(row=5, column=0, columnspan=3)

        self.convert_botton = Button(master, text="开始转换", command=self.start_conversion)
        self.convert_botton.grid(row=6, column=0, columnspan=3, pady=10)

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF 文件", "*.pdf")])
        if file_path:
            self.pdf_path.set(file_path)

            # 自动生成输出文件夹
            pdf_name = os.path.splitext(os.path.basename(file_path))[0]
            output_dir = os.path.join(os.path.dirname(file_path), f"{pdf_name}_imgs")
            self.output_folder.set(output_dir)

            # 清空进度和状态
            self.progress["value"] = 0
            self.status_label.config(text="")

    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)

    def start_conversion(self):
        thread = threading.Thread(target=self.convert_pdf_to_images)
        thread.start()

    def convert_pdf_to_images(self):
        pdf_path = self.pdf_path.get()
        dpi = int(self.dpi.get())
        fmt = self.img_format.get().lower()
        output_folder = self.output_folder.get()

        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showerror("错误", "请选择有效的 PDF 文件。")
            return

        try:
            os.makedirs(output_folder, exist_ok=True)

            self.status_label.config(text="正在读取 PDF 页数...")
            self.progress["value"] = 0
            self.master.update()

            poppler_path = get_poppler_path()

            images = convert_from_path(pdf_path, dpi=dpi, fmt=fmt, poppler_path=poppler_path)

            total = len(images)
            self.progress["maximum"] = total

            pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

            for i, page in enumerate(images):
                self.status_label.config(text=f"正在转换第 {i+1}/{total} 页...")
                self.master.update()

                filename = os.path.join(output_folder, f"{pdf_name}_page_{i+1}.{fmt}")
                page.save(filename, fmt.upper())

                self.progress["value"] = i + 1
                self.master.update()

            self.status_label.config(text=f"完成！生成 {total} 张图片。")
            messagebox.showinfo("完成", f"转换完成，图片保存在：\n{output_folder}")
        except Exception as e:
            self.status_label.config(text="转换失败。")
            messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    root = Tk()
    app = PDF2ImageApp(root)
    root.mainloop()
