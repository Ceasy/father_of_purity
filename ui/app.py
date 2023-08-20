import os
import sys

from tkinter import ttk, messagebox, scrolledtext
from ui.components import *
from updater import update
from config.settings import *


def open_license_file():
    if getattr(sys, 'frozen', False):
        # Если программа "заморожена" (скомпилирована)
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(base_path, "LICENSE.txt")
    os.system(f'start "" "{file_path}"')


class App:
    def __init__(self, root):
        self.window = root
        self.window_x = 0
        self.window_y = 0
        self.log_area = scrolledtext.ScrolledText(self.window)

        self.restart_btn = ttk.Button(self.window, text=RESTART_BTN_TEXT, command=lambda: restart_bitrix(self),
                                      style=BTN_STYLE)
        self.clear_btn = ttk.Button(self.window, text=CLEAR_BTN_TEXT, command=lambda: clear_all(self), style=BTN_STYLE)
        self.printer_btn = ttk.Button(self.window, text=PRINTER_BTN_TEXT, command=lambda: restart_printer(self),
                                      style=BTN_STYLE)

        self.status_var = tk.StringVar()
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self.window, orient=PROGRESS_BAR_ORIENTATION, length=PROGRESS_BAR_LENGTH,
                                            mode=PROGRESS_BAR_MODE,
                                            variable=self.progress_var)
        self.status_bar = tk.Label(self.window, text="Version: " + APP_VERSION + "",
                                   textvariable=self.status_var, bd=1,
                                   relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')

        self.initialize_ui()
        update.check_for_update(self)

    def initialize_ui(self):
        self.window.title(APP_NAME)
        self.window.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ico", "32px.ico"))
        self.window.geometry(APP_WINDOW_SIZE)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window_x = int((screen_width / 2) - (500 / 2))
        self.window_y = int((screen_height / 2) - (400 / 2))
        self.window.geometry(f"{APP_WINDOW_SIZE}+{self.window_x}+{self.window_y}")
        self.window.resizable(False, False)

        main_menu = tk.Menu(self.window)
        self.window.config(menu=main_menu)

        about_menu = tk.Menu(main_menu, tearoff=0)
        about_menu.add_command(label="О программе", command=lambda: messagebox.showinfo("О программе",
                                                                                        "Программа:" + APP_NAME + "\n"
                                                                                                                  "Версия: " + APP_VERSION + "\n"
                                                                                                                                             "Автор:" + APP_AUTOR + "\n"
                                                                                                                                                                    "Лицензия: смотрите файл LICENSE.txt\n"
                                                                                                                                                                    "Описание:" + APP_DESCRIPTION))
        about_menu.add_command(label="Лицензия", command=open_license_file)
        main_menu.add_cascade(label="О программе", menu=about_menu)

        self.status_var.set(
            "Version: " + APP_VERSION + " | Status: " + "Version: " + APP_VERSION + "")  # Setting the default status bar text to the version

        self.progress_bar.pack(side='bottom')

        style = ttk.Style()
        style.configure(BTN_STYLE, font=BTN_FONT, background='dark blue', foreground='black')

        self.clear_btn.pack(fill="x", padx=150, pady=10)
        self.restart_btn.pack(fill="x", padx=150, pady=10)
        self.printer_btn.pack(fill="x", padx=150, pady=10)

        self.log_area.pack(fill="both", expand=True)

    def block_buttons(self):
        self.restart_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')
        self.printer_btn.config(state='disabled')
        self.window.update()

    def unblock_buttons(self):
        self.restart_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        self.printer_btn.config(state='normal')
        self.window.update()
