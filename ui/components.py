import os
import shutil
import stat
import subprocess
import threading
import time
import psutil
import winshell

import tkinter as tk

from utils.helpers import notify_user
from config.decryptor_k import decrypt_data
from config.settings import *


def find_and_restart_process(process_name, app_instance):
    process_path = None
    process_found = False
    retries = 5

    while retries > 0:
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            if proc.info['name'] == process_name:
                process_found = True
                try:
                    print(f"Завершение процесса {proc.info['name']} с PID {proc.info['pid']} ...")
                    proc.kill()
                    process_path = proc.info['exe']
                except psutil.NoSuchProcess:
                    print(f"Процесс {proc.info['name']} с PID {proc.info['pid']} уже не существует.")
                    continue  # Skip to the next process
        time.sleep(2)

        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                print(f"Процесс {process_name} все еще работает. Повторная попытка завершения...")
                retries -= 1
                continue

        if process_path is not None:
            print(f"Запуск процесса {process_name} снова ...")
            try:
                # Attempt to start the process multiple times
                start_retries = 10
                while start_retries > 0:
                    try:
                        subprocess.Popen(process_path)
                        break  # If the process started successfully, break the loop
                    except Exception as e:
                        print(
                            f"Не удалось запустить процесс {process_name}. Ошибка: {str(e)}. Повторная попытка через 1 секунду...")
                        time.sleep(1)  # Wait for 1 second before retrying
                        start_retries -= 1

                # After the process is restarted, update the UI elements
                app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Done!")
                app_instance.progress_var.set(100)  # Fill the progress bar
                app_instance.restart_btn.config(state='normal',
                                                text=RESTART_BTN_TEXT)  # Enable the button and change its text back

                app_instance.unblock_buttons()

                # Проверка, запущен ли процесс
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] == process_name:
                        app_instance.log_area.insert(tk.END, "\n\nБитрикс, успешно запущен!\n", "center_tag")
                        app_instance.log_area.tag_configure("center_tag", foreground="green", justify='center',
                                                            font=("Helvetica", 12, "bold"))
                        return  # Exit the function if the process was successfully started
                print(f"Процесс {process_name} не был запущен.")
            except Exception as e:
                print(f"Не удалось запустить процесс {process_name}. Ошибка: {str(e)}")

        retries -= 1  # Decrement the retry counter

    if not process_found:
        app_instance.log_area.insert(tk.END, "\n\nБитрикс24 не запущен!\n", "red_tag")
        app_instance.log_area.tag_configure("red_tag", foreground="red", justify='center',
                                            font=("Helvetica", 12, "bold"))
        app_instance.log_area.insert(tk.END, "(запустите в ручную Битрикс24)\n", "black_tag")
        app_instance.log_area.tag_configure("black_tag", foreground="black", justify='center')

    # After the process is restarted, update the UI elements
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Done!")
    app_instance.progress_var.set(100)  # Fill the progress bar
    app_instance.restart_btn.config(state='normal',
                                    text=RESTART_BTN_TEXT)  # Enable the button and change its text back
    app_instance.unblock_buttons()


def restart_bitrix(app_instance):
    app_instance.block_buttons()
    app_instance.restart_btn.config(state='disabled', text="Перезапускаю....")
    app_instance.log_area.delete('1.0', tk.END)  # Clear the output before each run
    app_instance.restart_btn.config(state='disabled', text="Перезапуск...")  # Disable the button and change its text
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + f"{RESTART_BTN_TEXT}...")
    app_instance.progress_var.set(0)  # Reset the progress bar
    threading.Thread(target=find_and_restart_process,
                     args=(BITRIX_PROCESS_NAME, app_instance)).start()  # Start the process in a separate thread


def clear_directory(directory):
    def on_error(func, path, exc_info):
        """
        Error handler for `shutil.rmtree`.

        If the error is due to an access error (read only file)
        it attempts to add write permission and then retries.

        If the error is for another reason it re-raises the error.
        """
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

    if os.path.exists(directory):
        for i in range(3):  # try 3 times
            try:
                shutil.rmtree(directory, onerror=on_error)
                os.makedirs(directory)
                return True
            except PermissionError:
                time.sleep(2)  # wait for 2 seconds before trying again
    else:
        return False


def clear_cache(app_instance):
    cache_dir = os.path.expanduser("~\\AppData\\Local\\Temp")
    if clear_directory(cache_dir):
        app_instance.log_area.insert(tk.END, f'Cleared: {cache_dir}\n')


def clear_downloads(app_instance):
    downloads_dir = os.path.join(os.path.expanduser("~"), 'Downloads')
    if clear_directory(downloads_dir):
        app_instance.log_area.insert(tk.END, f'Cleared: {downloads_dir}\n')


def clear_recycle_bin(app_instance):
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        app_instance.log_area.insert(tk.END, 'Recycle Bin cleared!\n')
    except Exception as e:
        app_instance.log_area.insert(tk.END, f'Failed to clear Recycle Bin: {str(e)}\n')


def clear_office_temps(app_instance):
    excel_temp_dir = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Office\\UnsavedFiles")
    word_temp_dir = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Word")
    if clear_directory(excel_temp_dir):
        app_instance.log_area.insert(tk.END, f'Cleared: {excel_temp_dir}\n')
    if clear_directory(word_temp_dir):
        app_instance.log_area.insert(tk.END, f'Cleared: {word_temp_dir}\n')


def clear_1C_folders(app_instance):
    roaming_1C_dir = os.path.expanduser("~\\AppData\\Roaming\\1C\\1cv8")
    local_1C_dir = os.path.expanduser("~\\AppData\\Local\\1C\\1cv8")
    if clear_directory(roaming_1C_dir):
        app_instance.log_area.insert(tk.END, f'Cleared: {roaming_1C_dir}\n')
    if clear_directory(local_1C_dir):
        app_instance.log_area.insert(tk.END, f'Cleared: {local_1C_dir}\n')


def clear_all(app_instance):
    app_instance.block_buttons()
    app_instance.clear_btn.config(state='disabled', text="Идет чистка....")  # Disable the button and change its text
    app_instance.log_area.delete('1.0', tk.END)  # Clear text immediately
    app_instance.progress_var.set(0)  # Reset the progress bar
    threading.Thread(target=do_clear_all, args=(app_instance,)).start()  # Start long operations in a separate thread


def do_clear_all(app_instance):
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Clearing cache...")
    clear_cache(app_instance)
    app_instance.window.after(100, app_instance.progress_var.set, 20)  # Increment the progress bar
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Clearing downloads...")
    clear_downloads(app_instance)
    app_instance.window.after(100, app_instance.progress_var.set, 40)  # Increment the progress bar
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Clearing recycle bin...")
    clear_recycle_bin(app_instance)
    app_instance.window.after(100, app_instance.progress_var.set, 60)  # Increment the progress bar
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Clearing office temps...")
    clear_office_temps(app_instance)
    app_instance.window.after(100, app_instance.progress_var.set, 80)  # Increment the progress bar
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Clearing 1C folders...")
    clear_1C_folders(app_instance)
    app_instance.window.after(100, app_instance.progress_var.set, 100)  # Increment the progress bar
    num_chars = app_instance.log_area.winfo_width() // 8  # Adjust for character width
    app_instance.log_area.insert(tk.END, "=" * (num_chars - 1) + "\n")  # Add separator
    # Notify the user when the cleaning process is finished
    # notify_user(APP_NAME, "Чистка завершена успешно!")
    app_instance.log_area.insert(tk.END, "\n\nЧистка завершена успешно!\n", "center_tag")
    app_instance.log_area.tag_configure("center_tag", foreground="green", justify='center',
                                        font=("Helvetica", 12, "bold"))
    app_instance.log_area.insert(tk.END, "(Теперь можно закрыть приложение)\n", "black_tag")
    app_instance.log_area.tag_configure("black_tag", foreground="black", justify='center')
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Done!")
    app_instance.clear_btn.config(state='normal',
                                  text=CLEAR_BTN_TEXT)  # Enable the button and change its text back
    app_instance.unblock_buttons()


def restart_printer(app_instance):
    app_instance.block_buttons()
    app_instance.printer_btn.config(state='disabled', text="Настраиваю....")  # Disable the button and change its text
    app_instance.log_area.delete('1.0', tk.END)  # Clear text immediately
    app_instance.progress_var.set(0)  # Reset the progress bar
    threading.Thread(target=printer_repair, args=(app_instance,)).start()  # Start long operations in a separate thread


def printer_repair(app_instance):
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Closing the task manager...")
    taskmgr_restart(app_instance)
    app_instance.window.after(100, app_instance.progress_var.set, 45)  # Increment the progress bar
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Restarting spooler...")
    spooler_restart(app_instance)


def taskmgr_restart(app_instance):
    os.system(f"echo {decrypt_data(PWD, KEY)} | runas /user:{decrypt_data(USER, KEY)} /savecred \"taskkill /F /IM taskmgr.exe\"")
    os.system(f"echo {decrypt_data(PWD, KEY)} | runas /user:{decrypt_data(USER, KEY)} /savecred \"start taskmgr\"")
    app_instance.log_area.insert(tk.END, 'Task manager restarted\n')


def spooler_restart(app_instance):
    os.system(f"echo {decrypt_data(PWD, KEY)} | runas /user:{decrypt_data(USER, KEY)} /savecred \"net stop spooler\"")
    os.system(f"echo {decrypt_data(PWD, KEY)} | runas /user:{decrypt_data(USER, KEY)} /savecred \"del /Q C:\\Windows\\System32\\spool\\PRINTERS\\*\"")
    os.system(f"echo {decrypt_data(PWD, KEY)} | runas /user:{decrypt_data(USER, KEY)} /savecred \"net start spooler\"")
    app_instance.log_area.insert(tk.END, 'Spooler restarted\n')
    app_instance.window.after(100, app_instance.progress_var.set, 100)  # Increment the progress bar
    num_chars = app_instance.log_area.winfo_width() // 8  # Adjust for character width
    app_instance.log_area.insert(tk.END, "=" * (num_chars - 1) + "\n")  # Add separator
    # Notify the user when the cleaning process is finished
    # notify_user(APP_NAME, "Службы принтера перезапущенны успешно!")
    app_instance.log_area.insert(tk.END, "\n\nСлужбы принтера перезапущенны успешно!\n", "center_tag")
    app_instance.log_area.tag_configure("center_tag", foreground="green", justify='center',
                                        font=("Helvetica", 12, "bold"))
    app_instance.log_area.insert(tk.END, "(Теперь можно закрыть приложение)\n", "black_tag")
    app_instance.log_area.tag_configure("black_tag", foreground="black", justify='center')
    app_instance.status_var.set("Version: " + APP_VERSION + " | Status:" + "Done!")
    app_instance.printer_btn.config(state='normal',
                                  text=PRINTER_BTN_TEXT)  # Enable the button and change its text back
    app_instance.unblock_buttons()
