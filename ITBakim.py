import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from tkcalendar import DateEntry
from datetime import datetime, timedelta 


conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=192.168.1.15;"  
    "Database=HTSLIFE_TEST;"  
    "UID=SA;"  
    "PWD=;",  



)

cursor = conn.cursor()

CATEGORIES = ["Donanım", "Yazılım", "Ağ", "Diğer"]
ISLEM_SECENEKLERI = [
    "Antivirüs kontrolü", "İzinsiz program kontrolü", "Doluluk Kontrolü", "E-mail yedekleme",
    "PC yedekleme", "PC yazılım temizleme", "PC fiziki temizlik veya bakım", "Depolama Çözümleri",
    "Çevre birimleri kontrol ve bakımı", "Yazılım güncellemeleri", "Yeni yazılım eklenmesi",
    "Envanter Kontrolü(IT)", "Server bakımı", "Donanım Güncellemesi", "Ürün Zimmetlenmesi",
    "Windows Güncellemesi", "Lisans Güncellemeleri", "Geri Alma veya Format"
]


window = tk.Tk()
window.title("Periyodik Bakım Takip Listesi")
window.geometry("1000x600")

logo_path = "C:\\Users\\Muhasebe\\Desktop\\arkaplan seffaf.png"
logo = tk.PhotoImage(file=logo_path)
logo_label = tk.Label(window, image=logo)
logo_label.pack()


button_frame = tk.Frame(window)
button_frame.pack(pady=10)


table_frame = tk.Frame(window)
table_frame.pack(fill="both", expand=True)
columns = [
    "Sıra No", "Cihaz Adı", "Sicil No", "Kullanıcı Adı", "Sorumlu Kişi", 
    "Açıklama", "Son Bakım Tarihi", "Bir Sonraki Bakım Tarihi", "Kategori", "Yapılan İşlem","Departman"
]
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)


for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=120)
table.pack(fill="both", expand=True)


yakin_bakim_frame = tk.Frame(window)
yakin_bakim_frame.pack(fill="both", expand=True, pady=10)

yakin_columns = [
    "Sıra No", "Cihaz Adı", "Sicil No", "Kullanıcı Adı", "Sorumlu Kişi", 
    "Açıklama", "Son Bakım Tarihi", "Bir Sonraki Bakım Tarihi", "Kategori", "Yapılan İşlem", "Departman"
]
yakin_table = ttk.Treeview(yakin_bakim_frame, columns=yakin_columns, show="headings", height=15)

kategori_dict = {
    "1": "Ağ",
    "2": "Yazılım",
    "3": "Donanım"
}

islem_dict = {
    "1": "E-mail yedekleme",
    "2": "Doluluk Kontrolü",
    "3": "PC fiziki temizlik veya bakım"
}


Kategori_ID = "1" 
Islem_ID = "1"     

Kategori_Adi = kategori_dict.get(Kategori_ID, "Bilinmiyor")
Islem_Adi = islem_dict.get(Islem_ID, "Bilinmiyor")


print(f"Kategori ID: {Kategori_ID}, Kategori Adı: {Kategori_Adi}")

def departmanlari_al():
    try:
        cursor.execute("SELECT Departman_Adi FROM Departmanlar")
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
        
        cursor.execute("SELECT Kategori_ID, Kategori_Adi FROM Kategoriler")
        kategori_dict = {row[0]: row[1] for row in cursor.fetchall()}
        print("Kategori Dict:", kategori_dict)  

  
        cursor.execute("SELECT Islem_ID, Islem_Adi FROM YapilanIslemler")
        rows = cursor.fetchall()
        islem_dict = {row[0]: row[1] for row in rows}
        print("Islem Dict:", islem_dict)  

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
    "Sıra No", "Cihaz Adı", "Sicil No", "Kullanıcı Adı", "Sorumlu Kişi",
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




def veriyi_guncelle():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Uyarı", "Lütfen güncellemek için bir veri seçin!")
        return

    selected_data = table.item(selected_item, "values")

    guncelle_pencere = tk.Toplevel(window)
    guncelle_pencere.title("Veri Güncelle")
    guncelle_pencere.geometry("400x500")

    labels = [
        "Cihaz Adı", "Kullanıcı Adı", "Sorumlu Kişi", "Açıklama",
        "Son Bakım Tarihi", "Bir Sonraki Bakım Tarihi", "Kategori", "Yapılan İşlem"
    ]
    entries = {}
    departmanlar = departmanlari_al() 

    for idx, label_text in enumerate(labels):
        label = tk.Label(guncelle_pencere, text=label_text)
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="e")

        if label_text == "Departman":
            departman_var = tk.StringVar()
            departman_menu = ttk.Combobox(ekle_pencere, textvariable=departman_var, values=departmanlar)
            departman_menu.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = departman_var
        elif label_text == "Kategori":
            kategori_var = tk.StringVar()
            kategori_menu = ttk.Combobox(ekle_pencere, textvariable=kategori_var, values=list(kategori_dict.values()))
            kategori_menu.grid(row=idx, column=1, padx=10, pady=5, sticky=  "w")
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
    
        kategori_adi = entries["Kategori"].get()
        islem_adi = entries["Yapılan İşlem"].get()
        
        Kategori_ID = next((key for key, value in kategori_dict.items() if value == kategori_adi), None)
        Islem_ID = next((key for key, value in islem_dict.items() if value == islem_adi), None)

        guncellenmis_veri = [
            selected_data[0],  # Sıra No
            entries["Cihaz Adı"].get(),
            selected_data[2],  # Sicil No değişmez
            entries["Kullanıcı Adı"].get(),
            entries["Sorumlu Kişi"].get(),
            entries["Açıklama"].get(),
            entries["Son Bakım Tarihi"].get(),
            entries["Bir Sonraki Bakım Tarihi"].get(),
            Kategori_ID,  # Kategori ID
            Islem_ID,  # Yapılan İşlem ID
            entries["Departman"].get()
        ]

        cursor.execute(""" 
            UPDATE ITBakimListesi 
            SET CihazAdi=?, KullaniciAdi=?, SorumluKisi=?, Aciklama=?, SonBakimTarihi=?, 
                BirSonrakiBakimTarihi=?, Kategori=?, YapilanIslem=?, Departman=? 
            WHERE SicilNo=?
        """, guncellenmis_veri[1:], selected_data[2])
        conn.commit()

        messagebox.showinfo("Başarılı", "Veri başarıyla güncellendi!")
        guncelle_pencere.destroy()
        verileri_listele()

        for idx, label_text in enumerate(labels):
         label = tk.Label(guncelle_pencere, text=label_text)
         label.grid(row=idx, column=0, padx=10, pady=5, sticky="e")

        if label_text == "Kategori":
            kategori_var = tk.StringVar(value=selected_data[columns.index("Kategori")])
            kategori_menu = ttk.Combobox(guncelle_pencere, textvariable=kategori_var, values=CATEGORIES)
            kategori_menu.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = kategori_var
        elif label_text == "Yapılan İşlem":
            islem_var = tk.StringVar(value=selected_data[columns.index("Yapılan İşlem")])
            islem_menu = ttk.Combobox(guncelle_pencere, textvariable=islem_var, values=ISLEM_SECENEKLERI)
            islem_menu.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = islem_var
        elif "Tarih" in label_text:
            tarih_var = tk.StringVar(value=selected_data[columns.index(label_text)])
            tarih_entry = DateEntry(guncelle_pencere, textvariable=tarih_var, date_pattern='yyyy/mm/dd')
            tarih_entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = tarih_var
        else:
            entry = tk.Entry(guncelle_pencere)
            entry.insert(0, selected_data[columns.index(label_text)])
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="w")
            entries[label_text] = entry
          
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
       
        kategori_adi = entries["Kategori"].get()
        islem_adi = entries["Yapılan İşlem"].get()

        kategori_id = next((key for key, value in kategori_dict.items() if value == kategori_adi), None)
        Islem_ID = next((key for key, value in islem_dict.items() if value == islem_adi), None)

        yeni_veri = [
            "",  
            entries["Cihaz Adı"].get(),
            generate_sicil_no(entries["Departman"].get()),
            entries["Kullanıcı Adı"].get(),
            entries["Sorumlu Kişi"].get(),
            entries["Açıklama"].get(),
            entries["Son Bakım Tarihi"].get(),
            entries["Bir Sonraki Bakım Tarihi"].get(),
            kategori_id,  # Kategori ID
            Islem_ID,  # Yapılan İşlem ID
            entries["Departman"].get()
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


verileri_listele_button = tk.Button(button_frame, text="Veri Listele", command=verileri_listele)
verileri_listele_button.grid(row=0, column=0, padx=10, pady=5)


filtre_button = tk.Button(button_frame, text="Filtrele", command=filtreleme_ekrani_olustur)
filtre_button.grid(row=0, column=6, padx=10, pady=5) 




veri_sil_button = tk.Button(button_frame, text="Veri Sil", command=veri_sil)
veri_sil_button.grid(row=0, column=2, padx=10, pady=5)

veriyi_guncelle_button = tk.Button(button_frame, text="Veri Güncelle", command=veriyi_guncelle)
veriyi_guncelle_button.grid(row=0, column=3, padx=10, pady=5)

veri_ekle_button = tk.Button(button_frame, text="Veri Ekle", command=veri_ekle)
veri_ekle_button.grid(row=0, column=4, padx=10, pady=5)



verileri_listele()
yakin_bakimlari_listele()


window.mainloop()

print(f"Kategori ID: {Kategori_ID}, Kategori Adı: {Kategori_Adi}")
print(f"Islem ID: {Islem_ID}, Islem Adı: {Islem_Adi}")
