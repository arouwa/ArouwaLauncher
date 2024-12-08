import customtkinter as ctk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import subprocess
import os
import threading
from tkinter import ttk
import time

class MinecraftLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Launcher")
        self.root.geometry("800x500")

        # Karanlık tema için CustomTkinter ayarları
        ctk.set_appearance_mode("dark")  # Dark mode
        ctk.set_default_color_theme("green")  # Yeşil tema

        # Sol panel (News ve Client)
        self.left_frame = ctk.CTkFrame(self.root, width=200, height=500, fg_color="gray")
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # News başlıkları
        self.news_label = ctk.CTkLabel(self.left_frame, text="News", font=("Arial", 18))
        self.news_label.pack(pady=10)

        # Coming Soon büyük yazısı
        self.news_content = ctk.CTkLabel(self.left_frame, text="COMING SOON", font=("Arial", 24, "bold"))
        self.news_content.pack(pady=30)

        # Client başlıkları
        self.client_label = ctk.CTkLabel(self.left_frame, text="Client", font=("Arial", 18))
        self.client_label.pack(pady=20)

        # Sağ panel (Kullanıcı adı ve Sürüm seçimi)
        self.right_frame = ctk.CTkFrame(self.root, width=600, height=500, fg_color="gray")
        self.right_frame.pack(side="right", fill="both", padx=10, pady=10)

        # Kullanıcı adı giriş
        self.username_label = ctk.CTkLabel(self.right_frame, text="Kullanıcı Adı:")
        self.username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.right_frame)
        self.username_entry.pack(pady=5)

        # Sürüm seçimi
        self.version_label = ctk.CTkLabel(self.right_frame, text="Minecraft Sürümü:")
        self.version_label.pack(pady=5)
        self.version_combobox = ctk.CTkComboBox(self.right_frame, values=[
            "1.8.9", "1.9", "1.10", "1.11", "1.12", "1.13", "1.14", "1.15", "1.16",
            "1.17", "1.18", "1.19", "1.20", "1.20.1", "1.20.2", "1.20.3", "1.20.4", "1.20.5", 
            "1.20.6", "1.21", "fabric:1.8.9", "fabric:1.9", "fabric:1.10", "fabric:1.11",
            "fabric:1.12", "fabric:1.13", "fabric:1.14", "fabric:1.15", "fabric:1.16",
            "fabric:1.17", "fabric:1.18", "fabric:1.19", "fabric:1.20", "fabric:1.20.1",
            "fabric:1.20.2", "fabric:1.20.3", "fabric:1.20.4", "fabric:1.20.5", "fabric:1.20.6", 
            "fabric:1.21"
        ])
        self.version_combobox.pack(pady=5)

        # Start butonu sağ alt köşede
        self.start_button = ctk.CTkButton(self.right_frame, text="Start", command=self.start_game, width=150, height=40)
        self.start_button.pack(side="bottom", anchor="se", padx=20, pady=20)

        # Yükleme ekranı
        self.progress = ttk.Progressbar(self.right_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20, padx=10, side="bottom")

        # Mods Panel
        self.mods_panel = ctk.CTkFrame(self.root, width=400, height=150, fg_color="gray")
        self.mods_panel.pack(side="bottom", fill="both", padx=10, pady=10)

        self.mods_label = ctk.CTkLabel(self.mods_panel, text="Mods", font=("Arial", 18))
        self.mods_label.pack(pady=5)

        # "Open Mods Folder" düğmesi
        self.open_mods_button = ctk.CTkButton(self.mods_panel, text="Open Mods Folder", command=self.open_mods_folder)
        self.open_mods_button.pack(pady=10)

        # Modları göstereceğimiz Textbox
        self.mods_textbox = ctk.CTkTextbox(self.mods_panel, height=4, width=50, fg_color="gray")
        self.mods_textbox.pack(pady=10)

        # Modları sürükleyip bırakmak için alan
        self.mods_drop_area = ctk.CTkFrame(self.mods_panel, width=380, height=100, border_width=2, fg_color="gray")
        self.mods_drop_area.pack(pady=10)
        self.mods_drop_area.drop_target_register(DND_FILES)
        self.mods_drop_area.dnd_bind('<<Drop>>', self.on_mod_drop)

        # Uygulama başlatıldığında mevcut modları listele
        self.list_mods()

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

    def on_mod_drop(self, event):
        mod_file = event.data
        mods_folder = self.get_mods_folder()
        if not mods_folder:
            return
        if not os.path.exists(mods_folder):
            os.makedirs(mods_folder)
        dest = os.path.join(mods_folder, os.path.basename(mod_file))
        os.rename(mod_file, dest)
        self.list_mods()

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


# Uygulama başlatma
if __name__ == "__main__":
    try:
        root = TkinterDnD.Tk()
    except NameError:
        from tkinter import Tk
        root = Tk()
    app = MinecraftLauncherApp(root)
    root.mainloop()
