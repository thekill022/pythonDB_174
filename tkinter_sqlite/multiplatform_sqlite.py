# menyertakan package terkait untuk kebutuhan tampilan dan database
import tkinter as tk
from tkinter import *
from customtkinter import *
import tkinter.messagebox as msg
import sqlite3 as sql

# inisialisasi tkinter
app = Tk()

# mengatur warna background, ukuran jendela, judul jendela, dan mendisabled zoom jendela
app.configure(bg="white")
app.geometry('400x300') 
app.resizable(False,False)
app.title("Prediksi Hasil")

# membuat pembungkus utama yaitu window untuk semua element dan membuat window menjadi scrollabe dengan package customtkinter
Window = CTkScrollableFrame(master=app, orientation='vertical', width=400, height=300, fg_color='#ffffff')
Window.pack(expand=True)

# membuat label judul dan layout lainya yaitu label untuk entry dan entry serta membuat variabel untuk menangkap nilai entry
judul = tk.Label(Window, text='Prediksi Kelulusan Fakultas', bg='white')
judul.pack(padx=5, pady=0, fill='x', side='top')

first_frame = tk.Frame(Window, bg='white', height=400)
first_frame.pack(padx=0, pady=5,fill='x', side='top')

nama_siswa = tk.StringVar()
matematika = tk.DoubleVar()
geografi = tk.DoubleVar()
inggris = tk.DoubleVar()
prediksi_fakultas = tk.StringVar()

frames = []
entry = []
for i in range(1,5,1) :
        if i == 1 :
            x = tk.Label(first_frame, text=f'Nama Siswa \t:', bg='white')
            y = tk.Entry(first_frame, width=40, textvariable=nama_siswa)
        elif i == 2 :
            x = tk.Label(first_frame, text=f'Matematika \t:', bg='white')
            y = tk.Entry(first_frame, width=40, textvariable=matematika)
        elif i == 3 :
            x = tk.Label(first_frame, text=f'Geografi \t:', bg='white')
            y = tk.Entry(first_frame, width=40, textvariable=geografi)
        else :
            x = tk.Label(first_frame, text=f'Inggris \t\t:', bg='white')
            y = tk.Entry(first_frame, width=40, textvariable=inggris)
        
        frames.append(x)
        entry.append(y)
        
a = 0
for i in frames :
        i.grid(padx=5, pady=5, row=a, column=0, sticky='W')
        entry[a].grid(padx=5,pady=5,row=a, column=1, sticky='W')
        a += 1


result_label = tk.Label(first_frame, text='Hasil Prediksi \t: ', bg='white')
result_label.grid(padx=5, row=4, column=0, sticky='W')

result_prodi = tk.Label(first_frame, text='', bg='white')
result_prodi.grid(padx=5, row=4, column=1, sticky='W')

btn_frame = tk.Frame(first_frame, bg='white', width=300)
btn_frame.grid(row=5, column=0, columnspan=2)

# membuat function click yang akan berfungsi sebagai trigger pengiriman data ke database ketika tombol di klik
def click() :

    # menambahkan try dan except untuk error handling apabila terjadi error saat function dijalankan
    try :
        # membuat function prediksi untuk prediksi prodi
        def prediksi() :
            # membuat error handling berupa kondisi apabila nilai yang di input lebih dari 100 maka akan keluar dari function dan terbaca error
            if matematika.get() > 100 or geografi.get() > 100 or inggris.get() > 100 :
                exit()
            
            # membuat kondisi jika terdapat nilai dibawah KKM
            if matematika.get() < 75 or geografi.get() < 75 or inggris.get() < 75 :
                return 'Tidak Lulus Seleksi'
            # membuat kondisi jika matematika adalah nilai tertinggi
            elif matematika.get() > geografi.get() and matematika.get() > inggris.get() :
                return 'MIPA'
            # membuat kondisi jika geografi adalah nilai tertinggi
            elif geografi.get() > matematika.get() and geografi.get() > inggris.get() :
                return 'Ilmu Sosial'
            # membuat kondisi jika inggris adalah nilai tertinggi
            elif inggris.get() > geografi.get() and inggris.get() > matematika.get() :
                return 'Bahasa'
            # membuat kondisi selain kondisi yang telah dibuat sebelumnya
            else :
                # membuat kondisi jika nilai matematika = geografi tapi lebih besar dari nilai inggris
                if matematika.get() == geografi.get() and matematika.get() > inggris.get():
                    return 'MIPA atau Ilmu Sosial'
                # membuat kondisi jika nilai matematika = matematika tapi lebih besar dari nilai geografi
                elif matematika.get() == inggris.get() and matematika.get() > geografi.get() :
                    return 'MIPA atau Bahasa'
                # membuat kondisi jika nilai geografi = inggris tapi lebih besar dari nilai matematika
                elif geografi.get() == inggris.get() and geografi.get() > matematika.get() :
                    return 'Ilmu Sosial atau Bahasa'
                # membuat kondisi jika semua bernilai sama
                elif matematika.get() == geografi.get() == inggris.get() :
                    return 'Memenuhi Semua Fakultas'
                
        # membuat variabel untuk menampung nilai return dari function prediksi
        prediksi_diterima = prediksi()

        # membuat kondisi jika nama siswa terisi maka store data baru akan dijalankan
        if nama_siswa.get().strip() != '' :
            # menghubungkan ke database 
            db_con = sql.connect('YOUR DATABASE PATH')
            # mengexecute perintah query untuk membuat tabel prodi jika tabel prodi belum ada didalam database
            db_con.execute('''CREATE TABLE IF NOT EXISTS prodi(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama_siswa TEXT NOT NULL,
                        matematika REAL NOT NULL,
                        geografi REAL NOT NULL,
                        inggris REAL NOT NULL,
                        prediksi_fakutas TEXT NOT NULL)''')
            # mengexecute perintah query untuk store data ke dalam database prodi
            db_con.execute(f"INSERT INTO prodi(nama_siswa, matematika, geografi, inggris, prediksi_fakutas) VALUES ('{nama_siswa.get().upper().strip()}',{matematika.get()},{geografi.get()},{inggris.get()}, '{prediksi_diterima}')")
            # mengirim perintah kedatabase untuk menjalankan execute query yang telah didefinisikan sebelumnya
            db_con.commit()
            # menampilkan messagebox jika data berhasil dikirimkan
            msg.showinfo(title='Info', message=f"Data Berhasil Dikirim")
            # membuat cursor agar bisa fetch/memanggil data didalam database untuk ditampilkan
            c = db_con.cursor()
            # mengexecute perintah query untuk menselect data prediksi_fakultas yang cocok dengan nama siswa
            c.execute(f"SELECT prediksi_fakutas FROM prodi WHERE nama_siswa = '{nama_siswa.get().upper().strip()}'")
            # mengatur ulang atribut text pada label result_prodi dengan data yang difecth pada index ke -1 agar 
            # data terakhir yang distore yang akan dibaca lalu akses index ke 0 agar nilai yang dikembalikan hanya string
            result_prodi.config(text=c.fetchall()[-1][0])
            # karena semua proses ke database sudah selesai, maka diclose
            db_con.close()

            # mereset semua nilai entry ke semua
            nama_siswa.set('')
            matematika.set('0.0')
            geografi.set('0.0')
            inggris.set('0.0')

    # kondisi yang terjadi jika try menangkap error
    except :
        # menampilkan messagebox error
        msg.showerror(title='error', message='Terjadi Error saat pengiriman data')

# membuat button dengan trigger function click sebagai trigger untuk mengirimkan data ke database
button = tk.Button(btn_frame, text='Lihat Hasil', command=click)
button.grid(padx=20,pady=5, row=0, column=0)

# membuat mainloop agar window tidak autoclose saat dijalankan
app.mainloop()