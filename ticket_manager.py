import pyodbc

try:
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=192.168.1.15;"
        "Database=HTSLIFE_TEST;"
        "UID=SA;"
        "PWD="  # Ensure the correct password is provided
    )
    cursor = conn.cursor()
    print("Database connection established.")
except Exception as e:
    print(f"Error connecting to the database: {e}")

def get_sicil_no(kullanici_adi):
    try:
        cursor.execute("SELECT SicilNo FROM ITBakimListesi WHERE KullaniciAdi = ?", kullanici_adi)
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
    except Exception as e:
        print(f"Error fetching Sicil No: {e}")
        return None

def get_tickets():
    try:
        cursor.execute("SELECT * FROM ITBakimListesi")
        rows = cursor.fetchall()
        tickets = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
        return tickets
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return {"error": str(e)}

def create_ticket(data):
    try:
        sicil_no = get_sicil_no(data["KullaniciAdi"])
        if not sicil_no:
            return {"error": "Sicil No not found for the given Kullanici Adi"}
        
        cursor.execute("""
            INSERT INTO ITBakimListesi (CihazAdi, SicilNo, KullaniciAdi, SorumluKisi, Aciklama, 
                SonBakimTarihi, BirSonrakiBakimTarihi, Kategori, YapilanIslem, Departman)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["CihazAdi"], sicil_no, data["KullaniciAdi"], data.get("SorumluKisi", ""), data["Aciklama"],
            data["SonBakimTarihi"], data["BirSonrakiBakimTarihi"], data.get("Kategori", ""), data.get("YapilanIslem", ""), data.get("Departman", "")
        ))
        conn.commit()
        return {"message": "Ticket created successfully"}
    except Exception as e:
        print(f"Error creating ticket: {e}")
        return {"error": str(e)}