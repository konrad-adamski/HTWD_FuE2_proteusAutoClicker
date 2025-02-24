import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from AutoClicker import AutoClicker
from utils import file_count
import os

this_background_color = '#478a84'


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.clicker_thread = None
        self.title("DSC AutoClicker")
        self.minsize(720, 200)

        self.configure(background=this_background_color)

        self.directory_path = tk.StringVar(self)
        self.is_demo = tk.BooleanVar(self)  # Boolean variable for the checkbox
        self.factor = tk.DoubleVar(self)  # Double variable for the factor input

        select_button = tk.Button(self, text="Quellverzeichnis wählen", command=self.select_directory)
        select_button.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky="ew")
        select_button.config(width=20)

        self.path_entry = tk.Entry(self, textvariable=self.directory_path, state="readonly")
        self.path_entry.grid(row=0, column=1, columnspan=2, padx=(5, 10), pady=(10, 0), sticky="ew")
        self.path_entry.config(width=50)

        # Checkbox for is_demo
        demo_checkbox = tk.Checkbutton(self, text="is Demo", variable=self.is_demo)
        demo_checkbox.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='w')

        # Frame for Factor widgets
        factor_frame = tk.Frame(self, background=this_background_color)
        factor_frame.grid(row=1, column=1, columnspan=2, padx=(10, 10), pady=(5, 10), sticky='w')

        # Label and Entry for factor
        factor_label = tk.Label(factor_frame, text="Delay factor:", background=this_background_color)
        factor_label.pack(side=tk.LEFT, padx=(0, 10))
        factor_entry = tk.Spinbox(factor_frame, from_=1, to=5, increment=0.1, textvariable=self.factor, width=4)
        factor_entry.pack(side=tk.LEFT)

        self.start_button = tk.Button(self, text="Start", command=self.open_directory, state="disabled")
        self.start_button.grid(row=2, column=0, columnspan=3, padx=10, pady=(10, 10), sticky='w')
        self.start_button.config(width=20)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def open_directory(self):
        if self.directory_path.get():
            os.startfile(self.directory_path.get())

            # Dateianzahl im Verzeichnis ermitteln
            files_numb = file_count(self.directory_path.get())

            clicker = AutoClicker(files_numb, self.factor.get(), self.is_demo.get())
            self.start_button.config(state="disabled")

            # Start the AutoClicker in a separate thread
            self.clicker_thread = threading.Thread(target=clicker.start)
            self.clicker_thread.start()

            # Monitor the AutoClicker thread to end the program when the AutoClicker is finished
            self.after(100, self.check_clicker_thread)
        else:
            messagebox.showinfo("Information", "Bitte beide Verzeichnisse auswählen!")

    def check_clicker_thread(self):
        if not self.clicker_thread.is_alive():
            self.destroy()
        else:
            self.after(100, self.check_clicker_thread)

    def select_directory(self):
        dirname = filedialog.askdirectory(parent=self)
        if dirname:
            self.directory_path.set(dirname)
            self.check_paths()

    def check_paths(self):
        if self.directory_path.get():
            self.start_button.config(state="normal")
        else:
            self.start_button.config(state="disabled")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
