import os
import subprocess
import sys

import requests
from tkinter import ttk, messagebox, scrolledtext
from config.settings import *


def update_app(latest_version):
    real_path = os.path.dirname(sys.executable)
    update_script_path = os.path.join(real_path, "update.exe")

    if os.path.exists(update_script_path):
        print(f"File {update_script_path} exists!")
    else:
        print(f"File {update_script_path} does not exist!")

    update_url = '{}/fop-v{}.exe'.format(SERVER_URL, latest_version)
    subprocess.Popen([update_script_path, latest_version, update_url, real_path])


def check_for_update(app_instance):
    try:
        response = requests.get(f'{SERVER_URL}/update_manifest.json')
        response.raise_for_status()
        manifest = response.json()
        latest_version = manifest['version']

        # app_instance.current_version = '1.0.1'

        if latest_version > APP_VERSION:
            result = messagebox.askquestion("Обновление доступно",
                                            f"Найдена новая версия: {latest_version}. Хотите обновить ваше приложение?",
                                            icon='warning')
            if result == 'yes':
                update_app(latest_version)
            else:
                pass
        else:
            messagebox.showinfo("Версия актуальна", "У вас установлена последняя версия приложения.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при проверке обновлений: {str(e)}")
