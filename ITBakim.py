import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from tkcalendar import DateEntry
from datetime import datetime, timedelta 
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from tkinter import Menu, Label, SUNKEN, BOTTOM, X

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=192.168.1.15;"  
    "Database=HTSLIFE_TEST;"  
    "UID=SA;"  
    "PWD=;"
)  
window = ThemedTk(theme="arc")
window.title("Periyodik Bakım Takip Listesi")
window.geometry("1000x600")

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About")

status_bar = tk.Label(window, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)


cursor = conn.cursor()

CATEGORIES = ["Donanım", "Yazılım", "Ağ", "Diğer"]
ISLEM_SECENEKLERI = [
    "Antivirüs kontrolü", "İzinsiz program kontrolü", "Doluluk Kontrolü", "E-mail yedekleme",
    "PC yedekleme", "PC yazılım temizleme", "PC fiziki temizlik veya bakım", "Depolama Çözümleri",
    "Çevre birimleri kontrol ve bakımı", "Yazılım güncellemeleri", "Yeni yazılım eklenmesi",
    "Envanter Kontrolü(IT)", "Server bakımı", "Donanım Güncellemesi", "Ürün Zimmetlenmesi",
    "Windows Güncellemesi", "Lisans Güncellemeleri", "Geri Alma veya Format"
]




logo_path = "C:\\Users\\Muhasebe\\Desktop\\arkaplan seffaf.png"
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((int(logo_image.width / 6), int(logo_image.height / 6)), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(window, image=logo)
logo_label.place(relx=1.0, rely=0.0, anchor='ne')

button_frame = tk.Frame(window)
button_frame.pack(pady=10)


table_frame = tk.Frame(window)
table_frame.pack(fill="both", expand=True)
columns = [
    "id", "Cihaz Adı", "Sicil No", "Kullanıcı Adı", "Sorumlu Kişi", 
    "Açıklama", "Son Bakım Tarihi", "Bir Sonraki Bakım Tarihi", "Kategori", "Yapılan İşlem","Departman"
]
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=35)


for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=120)
table.pack(fill="both", expand=True)

yakin_bakim_title = tk.Label(window, text="Yaklaşan Bakımlar", font=("Helvetica", 18, "bold"))
yakin_bakim_title.pack(pady=10) 

yakin_bakim_frame = tk.Frame(window)
yakin_bakim_frame.pack(fill="both", expand=True, padx_=10, pady=10)

yakin_columns = [
    "id", "Cihaz Adı", "Sicil No", "Kullanıcı Adı", "Sorumlu Kişi", 
    "Açıklama", "Son Bakım Tarihi", "Bir Sonraki Bakım Tarihi", "Kategori", "Yapılan İşlem", "Departman"
]
yakin_table = ttk.Treeview(yakin_bakim_frame, columns=yakin_columns, show="headings", height=25)

kategori_dict = {
    "1": "Ağ",
    "2": "Yazılım",
    "3": "Donanım",
    "4": "Diğer"
}

islem_dict = {
    "1": "Antivirüs kontrolü",
    "2": "İzinsiz program kontrolü",
    "3": "Doluluk Kontrolü",
    "4": "E-mail yedekleme",
    "5": "PC yedekleme",
    "6": "PC yazılım temizleme",
    "7": "PC fiziki temizlik veya bakım",
    "8": "Depolama Çözümleri",
    "9": "Çevre birimleri kontrol ve bakımı",
    "10": "Yazılım güncellemeleri",
    "11": "Yeni yazılım eklenmesi",
    "12": "Envanter Kontrolü(IT)",
    "13": "Server bakımı",
    "14": "Donanım Güncellemesi",
    "15": "Ürün Zimmetlenmesi",
    "16": "Windows Güncellemesi",
    "17": "Lisans Güncellemeleri",
    "18": "Geri Alma veya Format"
}


Kategori_ID = "1" 
Islem_ID = "1"     

Kategori_Adi = kategori_dict.get(Kategori_ID, "Bilinmiyor")
Islem_Adi = islem_dict.get(Islem_ID, "Bilinmiyor")


print(f"Kategori ID: {Kategori_ID}, Kategori Adı: {Kategori_Adi}")

def departmanlari_al():
    try:
        cursor.execute("SELECT DISTINCT Departman FROM ITENVANTER")
        departmanlar = [row[0] for row in cursor.fetchall()]
        return departmanlar
    except Exception as e:
        messagebox.showerror("Hata", f"Departman verileri alınamadı: {e}")
        return []



def generate_sicil_no(department_number):
    current_year = datetime.now().year
    return f"{department_number}-{current_year}"

def kategori_ve_islem_verilerini_al():
    global kategori_dict, islem_dict
    try:
        cursor.execute("""
            SELECT 
                id, 
                CihazAdi, 
                SicilNo, 
                KullaniciAdi, 
                SorumluKisi, 
                Aciklama, 
                SonBakimTarihi, 
                BirSonrakiBakimTarihi, 
                Kategori, 
                YapilanIslem, 
                Departman
            FROM ITBakimListesi
            JOIN Kategoriler ON ITBakimListesi.Kategori = Kategoriler.Kategori_Adi
            JOIN YapilanIslemler ON ITBakimListesi.YapilanIslem = YapilanIslemler.Islem_Adi
        """)
        rows = cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Hata", f"Veritabanı hatası: {e}")


def verileri_listele():
    
    kategori_ve_islem_verilerini_al()


    for row in table.get_children():
        table.delete(row)

    try:
        cursor.execute("SELECT * FROM ITBakimListesi")
        rows = cursor.fetchall()

        for row in rows:
            Kategori_ID = row[8]  
            Islem_ID = row[9]     

            print(f"Kategori ID: {Kategori_ID}, Yapılan İşlem ID: {Islem_ID}")  

            Kategori_Adi = kategori_dict.get(Kategori_ID, "Bilinmiyor")  
            Islem_Adi = islem_dict.get(Islem_ID, "Bilinmiyor")  

             
            updated_row = list(row)
            updated_row[8] = Kategori_Adi    
            updated_row[9] = Islem_Adi  
            table.insert("", "end", values=updated_row)

           

    except Exception as e:
        messagebox.showerror("Hata", f"Veri listeleme hatası: {e}")
yakin_bakim_frame = tk.Frame(window)
yakin_bakim_frame.pack(fill="both", expand=True, pady=10)

yakin_columns = [
    "id", "Cihaz Adı", "Sicil No", "Kullanıcı Adı", "Sorumlu Kişi",
    "Açıklama", "Son Bakım Tarihi", "Bir Sonraki Bakım Tarihi", "Kategori", "Yapılan İşlem", "Departman"
]
yakin_table = ttk.Treeview(yakin_bakim_frame, columns=yakin_columns, show="headings", height=15)

for col in yakin_columns:
    yakin_table.heading(col, text=col)
    yakin_table.column(col, anchor="center", width=120)
yakin_table.pack(fill="both", expand=True)


def yakin_bakimlari_listele():
    print("yakin_bakimlari_listele called")  # Debug print
    # Tablodaki mevcut verileri temizle
    for row in yakin_table.get_children():
        yakin_table.delete(row)
    
    today = datetime.now().date()
    future_date = today + timedelta(days=30)  # Örneğin, 30 gün sonraya kadar olan bakımlar

    try:
        cursor.execute("SELECT * FROM ITBakimListesi WHERE BirSonrakiBakimTarihi BETWEEN ? AND ?", (today, future_date))
        rows = cursor.fetchall()
        print(f"Rows fetched: {rows}")  # Debug print

        for row in rows:
            print(f"Inserting row: {row}")  # Debug print
            yakin_table.insert("", "end", values=row)  # Tabloda her satırı ekle

    except Exception as e:
        messagebox.showerror("Hata", f"Veri listeleme hatası: {e}")

# Call the function on launch


# Add the implementation for filtreleme_ekrani_olustur function
def filtreleme_ekrani_olustur():
    pass

def veri_sil():
    selected_items = table.selection()  # Use the correct table
    print(f"Selected items: {selected_items}")  # Debug print
    if not selected_items:
        messagebox.showwarning("Uyarı", "Lütfen silmek için bir veri seçin!")
        return

    for item in selected_items:
        selected_data = table.item(item, "values")
        print(f"Selected data: {selected_data}")  # Debug print
        sicil_no = selected_data[2]  # Use the correct index for SicilNo

        if not sicil_no:
            messagebox.showwarning("Uyarı", "Seçili verinin Sicil No'su yok, bu veri silinemez!")
            continue

        if messagebox.askyesno("Silme Onayı", f"Seçili veriyi silmek istediğinize emin misiniz? {selected_data}"):
            try:
                cursor.execute("DELETE FROM ITBakimListesi WHERE SicilNo=?", (sicil_no,))
                conn.commit()
                table.delete(item)  # Remove the item from the table view
                messagebox.showinfo("Başarılı", "Veri başarıyla silindi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Veri silme hatası: {e}")


    verileri_listele()  # Refresh the table view




# Define the veri_guncelle function
def veri_guncelle():
    selected_items = table.selection()
    if not selected_items:
        messagebox.showwarning("Uyarı", "Lütfen güncellemek için bir veri seçin!")
        return

    selected_item = selected_items[0]
    selected_data = table.item(selected_item, "values")

    guncelle_pencere = tk.Toplevel(window)
    guncelle_pencere.title("Veri Güncelle")
    guncelle_pencere.geometry("400x500")

    labels = [
        "id", "Cihaz Adı","Sicil No", "Kullanıcı Adı", "Sorumlu Kişi", "Açıklama",
        "Son Bakım Tarihi", "Bir Sonraki Bakım Tarihi", "Kategori", "Yapılan İşlem"
    ]
    
    entries = {}

    for idx, label_text in enumerate(labels):
        label = tk.Label(guncelle_pencere, text=label_text)
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="e")

        if label_text == "Kategori":
            kategori_var = tk.StringVar(value=selected_data[8])
            kategori_menu = ttk.Combobox(guncelle_pencere, textvariable=kategori_var, values=CATEGORIES)
            kategori_menu.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = kategori_var
        elif label_text == "Yapılan İşlem":
            islem_var = tk.StringVar(value=selected_data[9])
            islem_menu = ttk.Combobox(guncelle_pencere, textvariable=islem_var, values=ISLEM_SECENEKLERI)
            islem_menu.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = islem_var
        elif "Tarih" in label_text:
            tarih_var = tk.StringVar(value=selected_data[idx])
            tarih_entry = DateEntry(guncelle_pencere, textvariable=tarih_var, date_pattern='yyyy/mm/dd')
            tarih_entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = tarih_var
        else:
            entry = tk.Entry(guncelle_pencere)
            entry.insert(0, selected_data[idx])
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = entry

    def kaydet():
        updated_data = {
            "Cihaz Adı": entries["Cihaz Adı"].get(),
            "Kullanıcı Adı": entries["Kullanıcı Adı"].get(),
            "Sorumlu Kişi": entries["Sorumlu Kişi"].get(),
            "Açıklama": entries["Açıklama"].get(),
            "Son Bakım Tarihi": entries["Son Bakım Tarihi"].get(),
            "Bir Sonraki Bakım Tarihi": entries["Bir Sonraki Bakım Tarihi"].get(),
            "Kategori": entries["Kategori"].get(),
            "Yapılan İşlem": entries["Yapılan İşlem"].get()
        }
        print("Updated Data:", updated_data)

        try:
            cursor.execute("""
                UPDATE ITBakimListesi
                SET CihazAdi=?, KullaniciAdi=?, SorumluKisi=?, Aciklama=?, SonBakimTarihi=?, BirSonrakiBakimTarihi=?, Kategori=?, YapilanIslem=?
                WHERE id=?
            """, (
                updated_data["Cihaz Adı"], updated_data["Kullanıcı Adı"], updated_data["Sorumlu Kişi"], updated_data["Açıklama"],
                updated_data["Son Bakım Tarihi"], updated_data["Bir Sonraki Bakım Tarihi"], updated_data["Kategori"], updated_data["Yapılan İşlem"],
                selected_data[0]
            ))
            conn.commit()
            messagebox.showinfo("Başarılı", "Veri başarıyla güncellendi!")
            guncelle_pencere.destroy()
            verileri_listele()
        except Exception as e:
            messagebox.showerror("Hata", f"Veri güncelleme hatası: {e}")

    # Add Save and Cancel buttons
    tk.Button(guncelle_pencere, text="Kaydet", command=kaydet).grid(row=len(labels), column=0, pady=10)
    tk.Button(guncelle_pencere, text="İptal", command=guncelle_pencere.destroy).grid(row=len(labels), column=1, pady=10)

# Correct the button definition


def filtreleme_ekrani_olustur():
    filtre_pencere = tk.Toplevel(window)
    filtre_pencere.title("Filtreleme")
    filtre_pencere.geometry("300x200")

    # Kategori Combobox
    tk.Label(filtre_pencere, text="Kategori:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    kategori_var = tk.StringVar()
    kategori_menu = ttk.Combobox(filtre_pencere, textvariable=kategori_var, values=list(kategori_dict.values()))
    kategori_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Yapılan İşlem Combobox
    tk.Label(filtre_pencere, text="Yapılan İşlem:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    islem_var = tk.StringVar()
    islem_menu = ttk.Combobox(filtre_pencere, textvariable=islem_var, values=list(islem_dict.values()))
    islem_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Filtreyi Uygula fonksiyonu
    def filtreyi_uygula():
        secilen_kategori = kategori_var.get()
        secilen_islem = islem_var.get()

        # Tablodaki mevcut verileri temizle
        for row in table.get_children():
            table.delete(row)

        try:
            query = "SELECT * FROM ITBakimListesi WHERE 1=1"
            params = []
            
            if secilen_kategori:
                query += " AND Kategori=?"
                kategori_id = next((key for key, value in kategori_dict.items() if value == secilen_kategori), None)
                params.append(kategori_id)
            
            if secilen_islem:
                query += " AND YapilanIslem=?"
                islem_id = next((key for key, value in islem_dict.items() if value == secilen_islem), None)
                params.append(islem_id)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()

            for row in rows:
                table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Hata", f"Filtreleme hatası: {e}")

    # Filtreyi Uygula ve İptal butonları
    tk.Button(filtre_pencere, text="Filtreyi Uygula", command=filtreyi_uygula).grid(row=2, column=0, columnspan=2, pady=20)
    tk.Button(filtre_pencere, text="İptal", command=filtre_pencere.destroy).grid(row=3, column=0, columnspan=2, pady=10)

# Add the filter button to the main window


    def kaydet():

        guncellenmis_veri = [
            selected_data[0],  # Sıra No
            entries["Cihaz Adı"].get(),
            selected_data[2],  # Sicil No değişmez
            entries["Kullanıcı Adı"].get(),
            entries["Sorumlu Kişi"].get(),
            entries["Açıklama"].get(),
            entries["Son Bakım Tarihi"].get(),
            entries["Bir Sonraki Bakım Tarihi"].get(),
            entries["Kategori"].get(),
            entries["Yapılan İşlem"].get(),
            entries["Departman"].get()
        ]

        cursor.execute("""
            UPDATE ITBakimListesi 
            SET CihazAdi=?, KullaniciAdi=?, SorumluKisi=?, Aciklama=?, SonBakimTarihi=?, 
                BirSonrakiBakimTarihi=?, Kategori=?, YapilanIslem=?, Departman=?
            WHERE SicilNo=?
        """, guncellenmis_veri[1:], guncellenmis_veri[2])
        conn.commit()

        messagebox.showinfo("Başarılı", "Veri başarıyla güncellendi!")
        guncelle_pencere.destroy()
        verileri_listele()

    tk.Button(guncelle_pencere, text="Kaydet", command=kaydet).grid(row=len(labels), column=0, pady=10)
    tk.Button(guncelle_pencere, text="İptal", command=guncelle_pencere.destroy).grid(row=len(labels), column=1, pady=10)

def veri_ekle():
    ekle_pencere = tk.Toplevel(window)
    ekle_pencere.title("Veri Ekle")
    ekle_pencere.geometry("400x500")

    labels = [
        "Cihaz Adı", "Kullanıcı Adı", "Sorumlu Kişi", "Açıklama",
        "Son Bakım Tarihi", "Bir Sonraki Bakım Tarihi", "Departman", "Kategori", "Yapılan İşlem"
    ]
    entries = {}
    departmanlar = departmanlari_al()  

    for idx, label_text in enumerate(labels):
        label = tk.Label(ekle_pencere, text=label_text)
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="e")

        if label_text == "Departman":
            departman_var = tk.StringVar()
            departman_menu = ttk.Combobox(ekle_pencere, textvariable=departman_var, values=departmanlar)
            departman_menu.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = departman_var
        elif label_text == "Kategori":
            kategori_var = tk.StringVar()
            kategori_menu = ttk.Combobox(ekle_pencere, textvariable=kategori_var, values=list(kategori_dict.values()))
            kategori_menu.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = kategori_var
        elif label_text == "Yapılan İşlem":
            islem_var = tk.StringVar()
            islem_menu = ttk.Combobox(ekle_pencere, textvariable=islem_var, values=list(islem_dict.values()))
            islem_menu.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = islem_var
        elif "Tarih" in label_text:
            tarih_var = tk.StringVar()
            tarih_entry = DateEntry(ekle_pencere, textvariable=tarih_var, date_pattern='yyyy/mm/dd')
            tarih_entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = tarih_var
        else:
            entry = tk.Entry(ekle_pencere)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = entry

    def kaydet():
        cihaz_adi = entries["Cihaz Adı"].get()
        kullanici_adi = entries["Kullanıcı Adı"].get()
        sorumlu_kisi = entries["Sorumlu Kişi"].get()
        aciklama = entries["Açıklama"].get()
        son_bakim_tarihi = entries["Son Bakım Tarihi"].get()
        bir_sonraki_bakim_tarihi = entries["Bir Sonraki Bakım Tarihi"].get()
        departman = entries["Departman"].get()
        kategori_adi = entries["Kategori"].get()
        islem_adi = entries["Yapılan İşlem"].get()

        kategori_id = next((key for key, value in kategori_dict.items() if value == kategori_adi), None)
        islem_id = next((key for key, value in islem_dict.items() if value == islem_adi), None)

        # Check if the name matches any existing record
        cursor.execute("SELECT SicilNo FROM ITBakimListesi WHERE KullaniciAdi=?", (kullanici_adi,))
        result = cursor.fetchone()
        if result:
            sicil_no = result[0]
        else:
            sicil_no = generate_sicil_no(departman)

        yeni_veri = [
            "",  
            cihaz_adi,
            sicil_no,
            kullanici_adi,
            sorumlu_kisi,
            aciklama,
            son_bakim_tarihi,
            bir_sonraki_bakim_tarihi,
            kategori_id,  # Kategori ID
            islem_id,  # Yapılan İşlem ID
            departman
        ]

        cursor.execute(""" 
            INSERT INTO ITBakimListesi (CihazAdi, SicilNo, KullaniciAdi, SorumluKisi, Aciklama, 
                SonBakimTarihi, BirSonrakiBakimTarihi, Kategori, YapilanIslem, Departman)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, yeni_veri[1:])
        conn.commit()

        messagebox.showinfo("Başarılı", "Veri başarıyla eklendi!")
        ekle_pencere.destroy()
        verileri_listele()

    tk.Button(ekle_pencere, text="Kaydet", command=kaydet).grid(row=len(labels), column=0, pady=10)
    tk.Button(ekle_pencere, text="İptal", command=ekle_pencere.destroy).grid(row=len(labels), column=1, pady=10)
# Create a context menu
context_menu = Menu(window, tearoff=0)
context_menu.add_command(label="Refresh", command=verileri_listele)

# Function to show the context menu
def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

# Bind the right-click event to the table to show the context menu
table.bind("<Button-3>", show_context_menu)
yakin_table.bind("<Button-3>", show_context_menu)

verileri_listele_button = tk.Button(button_frame, text="Veri Listele", command=verileri_listele)
verileri_listele_button.grid(row=0, column=0, padx=10, pady=5)


filtre_button = tk.Button(button_frame, text="Filtrele", command=filtreleme_ekrani_olustur)
filtre_button.grid(row=0, column=6, padx=10, pady=5) 




veri_sil_button = tk.Button(button_frame, text="Veri Sil", command=veri_sil)
veri_sil_button.grid(row=0, column=2, padx=10, pady=5)

veriyi_guncelle_button = tk.Button(button_frame, text="Veri Güncelle", command=veri_guncelle)
veriyi_guncelle_button.grid(row=0, column=3, padx=10, pady=5)

veri_ekle_button = tk.Button(button_frame, text="Veri Ekle", command=veri_ekle)
veri_ekle_button.grid(row=0, column=4, padx=10, pady=5)



verileri_listele()
yakin_bakimlari_listele()


window.mainloop()

print(f"Kategori ID: {Kategori_ID}, Kategori Adı: {Kategori_Adi}")
print(f"Islem ID: {Islem_ID}, Islem Adı: {Islem_Adi}")
