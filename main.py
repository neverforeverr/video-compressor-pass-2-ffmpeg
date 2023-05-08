import os
import shlex
import subprocess
import tkinter as tk
from tkinter import filedialog as fd, ttk, Label, Button, scrolledtext
import threading


source = "/home/virgiawan/Video/"
hasil = "/home/virgiawan/Videos/TUMBAL\ PROYEK/"


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Video Compressor")
        self.geometry('365x350')
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

        self.textbox = scrolledtext.ScrolledText(self, bg='black', fg='green', width=48, height=8)

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
        pass1 = f"ffmpeg -y -i {video} -c:v libx264 -b:v 8k -c:a aac -b:a 8k -refs 5 -t 10 -pass 1 -f null /dev/null"

        thread1 = threading.Thread(target=self.tmp_proc, args=(pass1,))
        thread1.start()

    def tmp_proc(self, command):
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            line = process.stdout.readline().decode()
            if not line:
                break

            # Update the textbox in the main thread
            self.textbox.after(0, self.textbox.insert, tk.END, line)
            self.textbox.after(0, self.textbox.see, tk.END)

        process.wait()

        # Update the progress bar
        # self.progress_bar.after(0, self.progress_bar.step, 50)

        pass2 = f"ffmpeg -y -i {video} -c:v libx264 -b:v 8k -c:a aac -b:a 8k -refs 5 -pass 2 {merger}"
        thread2 = threading.Thread(target=self.tmp_proc, args=(pass2,))
        thread2.start()


if __name__ == "__main__":
    root = App()
    root.resizable(True, True)
    root.mainloop()
