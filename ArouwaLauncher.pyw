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
        self.version_combobox = ctk.CTkComboBox(self.right_frame, values=["1.8.9", "1.9", "1.10", "1.11", "1.12", 
                                                                       "1.13", "1.14", "1.15", "1.16", "1.17", 
                                                                       "1.18", "1.19", "1.20", "1.20.1", "1.20.2", 
                                                                       "1.20.3", "1.20.4", "1.20.5", "1.20.6", 
                                                                       "1.21"])
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

        # Modları sürükleyip bırakmak için alan
        self.mods_drop_area = ctk.CTkFrame(self.mods_panel, width=380, height=100, border_width=2, fg_color="gray")
        self.mods_drop_area.pack(pady=10)

        # Mod sürükleyip bırakma alanına etkileşim ekleyelim
        self.mods_drop_area.drop_target_register(DND_FILES)
        self.mods_drop_area.dnd_bind('<<Drop>>', self.on_mod_drop)

        # Modları göstereceğimiz Textbox
        self.mods_textbox = ctk.CTkTextbox(self.mods_panel, height=4, width=50, fg_color="gray")
        self.mods_textbox.pack(pady=10)

    def start_game(self):
        username = self.username_entry.get()
        version = self.version_combobox.get()

        if not username or not version:
            messagebox.showerror("Hata", "Lütfen kullanıcı adı ve sürüm seçin!")
            return

        # Yükleme ekranını göster
        self.progress['value'] = 0
        self.progress.update()

        # Start butonunu devre dışı bırak
        self.start_button.configure(state="disabled")

        # Yeni bir iş parçacığı başlat, Minecraft'ı burada başlatacağız
        threading.Thread(target=self.run_minecraft, args=(username, version)).start()

    def run_minecraft(self, username, version):
        # Minecraft'ı başlatmak için portablemc komutunu subprocess ile çalıştırıyoruz
        try:
            # Minecraft'ı başlatmadan önce biraz bekletelim (progress bar'ı simüle etmek için)
            self.simulate_progress()

            # Minecraft başlatılacak
            command = f"portablemc start {version} --username {username}"
            
            # Minecraft'ı başlatıyoruz ve işlem tamamlanana kadar bekliyoruz
            self.hide_gui()  # Minecraft başlatıldığında GUI'yi gizle

            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

            # Çıktıyı yazdırma (isteğe bağlı)
            print(result.stdout)
            messagebox.showinfo("Başlatma", f"{version} sürümü başarıyla başlatıldı.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Başlatma Hatası", f"Başlatma hatası: {e}")
            print(f"Başlatma hatası: {e}")
        finally:
            # İşlem tamamlandığında Start butonunu tekrar aktif yapalım
            self.start_button.configure(state="normal")
            self.progress['value'] = 0

            self.show_gui()  # Minecraft kapandığında GUI'yi tekrar göster

    def simulate_progress(self):
        """İlerleme çubuğunu simüle etme fonksiyonu (gerçek ilerleme yerine)"""
        for i in range(0, 101, 10):
            self.progress['value'] = i
            self.progress.update()
            time.sleep(1)  # Gerçek zamanlı bekleme

    def hide_gui(self):
        """Minecraft başlatıldığında GUI'yi gizler"""
        self.root.after(100, lambda: self.root.withdraw())  # GUI'yi gizle

    def show_gui(self):
        """Minecraft kapandıktan sonra GUI'yi tekrar gösterir"""
        self.root.after(100, lambda: self.root.deiconify())  # GUI'yi göster

    def on_mod_drop(self, event):
        mod_file = event.data  # Sürüklenen dosyanın yolu
        print(f"Mod Dosyası Yüklendi: {mod_file}")

        # Minecraft mods klasörü konumu (Kullanıcı adı dinamik şekilde alınacak)
        user_profile_path = os.environ.get("USERPROFILE", "")
        if user_profile_path:
            mods_folder = os.path.join(user_profile_path, "AppData", "Roaming", ".minecraft", "mods")
        else:
            messagebox.showerror("Hata", "Kullanıcı profili alınamadı!")
            return

        if not os.path.exists(mods_folder):
            os.makedirs(mods_folder)

        # Modu ilgili klasöre taşıyalım
        try:
            dest = os.path.join(mods_folder, os.path.basename(mod_file))
            os.rename(mod_file, dest)
            print(f"Mod başarıyla {dest} konumuna taşındı.")

            # Modu GUI'de göstermek için Textbox'a ekleyelim
            self.mods_textbox.insert("end", os.path.basename(mod_file) + "\n")
        except Exception as e:
            print(f"Mod taşınırken hata oluştu: {e}")

# Uygulama başlatma
if __name__ == "__main__":
    root = TkinterDnD.Tk()  # TkinterDnD.Tk() kullanıyoruz
    app = MinecraftLauncherApp(root)
    root.mainloop()
