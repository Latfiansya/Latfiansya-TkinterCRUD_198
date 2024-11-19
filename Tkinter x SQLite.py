import sqlite3  # Modul untuk database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Import Tkinter untuk GUI

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database SQLite
    cursor = conn.cursor()  # Membuat cursor untuk eksekusi SQL
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            nama_siswa TEXT,  
            biologi INTEGER,  
            fisika INTEGER, 
            inggris INTEGER,  
            prediksi_fakultas TEXT  
        ) 
    ''')  # Membuat tabel yang berisikan atribut-atribut : nama_siswa, biologi, fisika, inggris, dan prediksi fakultas
    # Tipe data dalam tabel juga di set pada code diatas
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()   # Menutup koneksi

# Fungsi untuk mengambil semua data dari tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Query untuk mengambil semua data
    rows = cursor.fetchall()  # Menyimpan hasil query
    conn.close()  # Menutup koneksi
    return rows   # Mengembalikan data

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    cursor.execute('''  
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi)) # Query untuk memasukkan/menyimpan data
    # VALUES (?) menandakan nilai/isian akan di input oleh user
    conn.commit()  # Menyimpan perubahan
    conn.close()   # Menutup koneksi

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    cursor.execute('''  
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ? 
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) # Query untuk memperbarui data berdasarkan ID
    # SET ... = ? menandakan nilai/isian akan di input oleh user
    conn.commit()  # Menyimpan perubahan
    conn.close()   # Menutup koneksi

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Query untuk menghapus data berdasarkan ID
    conn.commit()  # Menyimpan perubahan
    conn.close()   # Menutup koneksi

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:    # Biologi tertinggi
        return "Kedokteran"                       # Hasil prediksinya
    elif fisika > biologi and fisika > inggris:   # Fisika tertinggi
        return "Teknik"                           # Hasil prediksinya
    elif inggris > biologi and inggris > fisika:  # Inggris tertinggi
        return "Bahasa"                           # Hasil prediksinya
    else:                                         # Jika nilainya sama
        return "Tidak Diketahui"                  # Hasil prediksinya

# Fungsi untuk menambahkan data baru
def submit():
    try:
        nama = nama_var.get()  # Mengambil nama dari input pengguna
        biologi = int(biologi_var.get())  # Mengambil nilai Biologi
        fisika = int(fisika_var.get())    # Mengambil nilai Fisika
        inggris = int(inggris_var.get())  # Mengambil nilai Inggris

        if not nama:  # Validasi, nama tidak boleh kosong
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)   # Hitung prediksi
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  # Tampilkan notifikasi
        clear_inputs()    # Reset input
        populate_table()  # Refresh tabel
    except ValueError as e:  # Tangani kesalahan input
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data
def update():
    try:
        if not selected_record_id.get():  # Validasi, ID harus dipilih terlebih dahulu
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mengambil ID dari data terpilih
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:  # Validasi nama
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Perbarui database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Tampilkan notifikasi
        clear_inputs()    # Reset input
        populate_table()  # Refresh tabel
    except ValueError as e: 
        messagebox.showerror("Error", f"Kesalahan: {e}") # Pesan apabila terdapat kesalahan

# Fungsi untuk menghapus data
def delete():
    try:
        if not selected_record_id.get():  # Validasi, ID harus dipilih terlebih dahulu
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Ambil ID data
        delete_database(record_id)  # Hapus dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Memunculkan notifikasi
        clear_inputs()    # Reset input
        populate_table()  # Refresh tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}") # Pesan apabila terdapat kesalahan

# Fungsi untuk mengosongkan entry (sebelum dan setelah input nilai)
def clear_inputs():
    nama_var.set("")     # Reset nama
    biologi_var.set("")  # Reset Biologi
    fisika_var.set("")   # Reset Fisika
    inggris_var.set("")  # Reset Inggris
    selected_record_id.set("")  # Reset ID terpilih

# Fungsi untuk menampilkan data di tabel
def populate_table():
    for row in tree.get_children():  # Menghapus data lama dari tabel
        tree.delete(row)
    for row in fetch_data():  # Menambahkan data baru dari database
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi input dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]     # Ambil data yang dipilih di tabel
        selected_row = tree.item(selected_item)['values']  # Ambil nilai-nilainya

        selected_record_id.set(selected_row[0])  # Set ID (yang dipilih)
        nama_var.set(selected_row[1])            # Isi nama
        biologi_var.set(selected_row[2])         # Isi Biologi
        fisika_var.set(selected_row[3])          # Isi Fisika
        inggris_var.set(selected_row[4])         # Isi Inggris
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")  # Pesan apabila terdapat kesalahan

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk() # Fungsi untuk menampilkan jendela tkinter
root.title("Prediksi Fakultas Siswa")  # Judul jendela/aplikasi

# Membuat variabel tkinter untuk input data
nama_var = StringVar()            # Untuk menyimpan nama
biologi_var = StringVar()         # Untuk menyimpan nilai biologi
fisika_var = StringVar()          # Untuk menyimpan nilai fisika
inggris_var = StringVar()         # Untuk menyimpan nilai inggris
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Membuat komponen GUI
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5) # Membuat label nama siswa dan mengatur posisinya
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5) # Membuat entry untuk nama siswa dan mengatur posisinya

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5) # Membuat label nilai biologi dan mengatur posisinya
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5) # Membuat entry untuk nilai biologi dan mengatur posisinya

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5) # Membuat label nilai fisika dan mengatur posisinya
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5) # Membuat entry untuk fisika dan mengatur posisinya

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5) # Membuat label nilai inggris dan mengatur posisinya
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5) # Membuat entry untuk nilai inggris dan mengatur posisinya

Button(root, text="Add", command=submit).grid(row=4, column=0,pady=10) # Membuat button untuk submit tabel baru
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10) # Membuat button untuk update tabel
Button(root, text=" Delete ", command=delete).grid(row=4, column=2, pady=10) # Membuat button untuk delete tabel

# Membuat tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')  # Membuat tabel untuk menampilkan data menggunakan Treeview

# Mengatur posisi isi tabel agar di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())  # Mengatur judul kolom
    tree.column(col, anchor='center')  # Agar isi tabel rata tengah

tree.grid(row=7, column=0, columnspan=3, padx=10, pady=10)  # Posisi tabel di GUI

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Event klik tabel untuk isi input

populate_table()  # Mengisi tabel saat pertama kali aplikasi dijalankan

root.mainloop()  # Fungsi untuk menjalankan aplikasi