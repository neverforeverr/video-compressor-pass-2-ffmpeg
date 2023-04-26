import sys
import os
import shlex
import subprocess
import tkinter as tk
from time import sleep
from tkinter import filedialog as fd, ttk, Label, Button, scrolledtext


source = "/home/virgiawan/Video/"
hasil = "/home/virgiawan/Videos/TUMBAL\ PROYEK/"


class Redirect(object):
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, message):
        self.textbox.insert(tk.END, message)
        self.textbox.see(tk.END)

    def flush(self):
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Video Compressor")
        self.minsize(width=365, height=350)
        self.maxsize(width=365, height=350)
        self.config(background="white")

        # button_explore
        self.explore_button = Button(
            self,
            text="Cari File",
            borderwidth=1,
            command=self.exploreFile,
            relief="solid",
        )

        self.compress_button = Button(
            self,
            text="Kompress",
            command=self.kompresFile,
            borderwidth=1,
            relief="solid",
        )

        self.progress_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            mode="determinate",
            length=350,
        )

        self.textbox = scrolledtext.ScrolledText(self, width=48, height=8, border=1)

        self.file_label = Label(
            self,
            text="File dipilih:",
            width=50,
            height=5,
            borderwidth=1,
            relief="solid",
        )

        self.compress_button.place(x=275, y=100)
        self.explore_button.place(x=5, y=100)
        self.progress_bar.place(x=5, y=300)
        self.file_label.place(x=5, y=5)
        self.textbox.place(x=5, y=150)

    def exploreFile(self):
        global merger, video

        video = fd.askopenfilename(
            initialdir=source,
            initialfile="",
            title="Cari file",
            filetypes=[("Mp4 file", ".mp4")],
        )

        basename = os.path.basename(video)
        splitbase = os.path.splitext(basename)[0]
        merger = f"{hasil}{splitbase}__awkoawkoawko.mp4"

        self.file_label.configure(text="File Dipilih: \n " + basename)

    def kompresFile(self):
        pass1 = f"ffmpeg -y -i {video} -c:v libx264 -b:v 8k -c:a aac -b:a 8k -refs 5 -pass 1 -f null /dev/null"
        subprocess.run(shlex.split(pass1), stdout=sub.stdout, stderr=sys.stderr)

        sleep(3)

        pass2 = f"ffmpeg -y -i {video} -c:v libx264 -b:v 8k -c:a aac -b:a 8k -refs 5 -pass 2 {merger}"
        subprocess.run(shlex.split(pass2), stdout=sys.stdout, stderr=sys.stderr)


if __name__ == "__main__":
    root = App()

    # Mengganti sys.stdout dan sys.stderr dengan StdoutRedirector
    sys.stdout = Redirect(root.textbox)
    sys.stderr = Redirect(root.textbox)

    root.mainloop()
