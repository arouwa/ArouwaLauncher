import customtkinter as ctk
from tkinter import messagebox, Tk
import subprocess
import os
import threading
from tkinter import ttk
import time
import requests

class MinecraftLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AROUWA LAUNCHER")
        self.root.geometry("1000x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Yan panel (News)
        self.left_frame = ctk.CTkFrame(self.root, width=250, height=600, fg_color="#1c1c1c")
        self.left_frame.pack(side="left", fill="y")

        self.news_label = ctk.CTkLabel(self.left_frame, text="News", font=("Arial", 18, "bold"), text_color="#5dade2")
        self.news_label.pack(pady=20)

        self.news_content = ctk.CTkTextbox(self.left_frame, height=20, width=200, fg_color="#1c1c1c", text_color="white")
        self.news_content.pack(pady=10, padx=10)
        self.fetch_news()

        # Sağ panel (Menü)
        self.right_frame = ctk.CTkFrame(self.root, fg_color="#1c1c1c")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.username_label = ctk.CTkLabel(self.right_frame, text="Kullanıcı Adı / Username:", text_color="white")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.right_frame)
        self.username_entry.pack(pady=5)

        self.version_label = ctk.CTkLabel(self.right_frame, text="Minecraft Sürümü / Version:", text_color="white")
        self.version_label.pack(pady=5)
        self.version_combobox = ctk.CTkComboBox(self.right_frame, values=[
            "release", "fabric:release", "1.8.9", "1.9", "1.10", "1.11", "1.12", "1.13", "1.14", "1.15", "1.16",
            "1.17", "1.18", "1.19", "1.20", "1.20.1", "1.20.2", "1.20.3", "1.20.4", "1.20.5", 
            "1.20.6", "1.21", "fabric:1.8.9", "fabric:1.9", "fabric:1.10", "fabric:1.11",
            "fabric:1.12", "fabric:1.13", "fabric:1.14", "fabric:1.15", "fabric:1.16",
            "fabric:1.17", "fabric:1.18", "fabric:1.19", "fabric:1.20", "fabric:1.20.1",
            "fabric:1.20.2", "fabric:1.20.3", "fabric:1.20.4", "fabric:1.20.5", "fabric:1.20.6", 
            "fabric:1.21"
        ])
        self.version_combobox.pack(pady=5)

        self.start_button = ctk.CTkButton(self.right_frame, text="Start", command=self.start_game, width=150, height=40)
        self.start_button.pack(pady=20)

        self.progress = ttk.Progressbar(self.right_frame, orient="horizontal", length=250, mode="determinate")
        self.progress.pack(pady=10)

        # Mods panel
        self.mods_panel = ctk.CTkFrame(self.right_frame, fg_color="#1c1c1c")
        self.mods_panel.pack(fill="both", padx=10, pady=10)

        self.mods_label = ctk.CTkLabel(self.mods_panel, text="Mods", font=("Arial", 18, "bold"), text_color="#5dade2")
        self.mods_label.pack(pady=5)

        self.open_mods_button = ctk.CTkButton(self.mods_panel, text="Open Mods Folder", command=self.open_mods_folder)
        self.open_mods_button.pack(pady=10)

        self.mods_textbox = ctk.CTkTextbox(self.mods_panel, height=8, fg_color="#1c1c1c", text_color="white")
        self.mods_textbox.pack(pady=10)

        self.list_mods()

    def fetch_news(self):
        url = "https://github.com/arouwa/ArouwaLauncher/releases"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                news = response.text
                self.news_content.insert("1.0", news)
            else:
                self.news_content.insert("1.0", "Failed to fetch news.")
        except Exception as e:
            self.news_content.insert("1.0", f"Error: {e}")

    def open_mods_folder(self):
        mods_folder = self.get_mods_folder()
        if mods_folder:
            os.startfile(mods_folder)

    def list_mods(self):
        mods_folder = self.get_mods_folder()
        if not mods_folder:
            return
        self.mods_textbox.delete("1.0", "end")
        if os.path.exists(mods_folder):
            mod_files = os.listdir(mods_folder)
            for mod_file in mod_files:
                self.mods_textbox.insert("end", mod_file + "\n")

    def get_mods_folder(self):
        user_profile_path = os.environ.get("USERPROFILE", "")
        if user_profile_path:
            return os.path.join(user_profile_path, "AppData", "Roaming", ".minecraft", "mods")
        else:
            messagebox.showerror("Hata", "Kullanıcı profili alınamadı!")
            return None

    def start_game(self):
        username = self.username_entry.get()
        version = self.version_combobox.get()
        if not username or not version:
            messagebox.showerror("Hata", "Lütfen kullanıcı adı ve sürüm seçin!")
            return
        self.progress['value'] = 0
        self.start_button.configure(state="disabled")
        threading.Thread(target=self.run_minecraft, args=(username, version)).start()

    def run_minecraft(self, username, version):
        try:
            self.simulate_progress()
            command = f"portablemc start {version} --username {username}"
            self.hide_gui()
            subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Başlatma Hatası", f"Başlatma hatası: {e}")
        finally:
            self.start_button.configure(state="normal")
            self.progress['value'] = 0
            self.show_gui()

    def simulate_progress(self):
        for i in range(0, 101, 10):
            self.progress['value'] = i
            self.progress.update()
            time.sleep(0.5)

    def hide_gui(self):
        self.root.withdraw()

    def show_gui(self):
        self.root.deiconify()

if __name__ == "__main__":
    root = Tk()
    app = MinecraftLauncherApp(root)
    root.mainloop()
