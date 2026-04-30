import tkinter as tk
from tkinter import ttk, messagebox


class Arayuz:

    def __init__(self, pencere, uygulama):
        self.pencere = pencere
        self.uygulama = uygulama

        pencere.title("Araç Kiralama Sistemi")
        pencere.geometry("900x500")

        # tablo
        self.tablo = ttk.Treeview(
            pencere,
            columns=("plaka", "marka", "model", "ucret", "durum"),
            show="headings"
        )

        self.tablo.pack(fill="both", expand=True, padx=10, pady=10)

        for sutun in self.tablo["columns"]:
            self.tablo.heading(sutun, text=sutun.upper())
            self.tablo.column(sutun, anchor="center")

        # butonlar
        buton_cercevesi = ttk.Frame(pencere)
        buton_cercevesi.pack(pady=10)

        ttk.Button(buton_cercevesi, text="Araç Ekle", command=self.ekle_formu).grid(row=0, column=0, padx=5)
        ttk.Button(buton_cercevesi, text="Sil", command=self.arac_sil).grid(row=0, column=1, padx=5)
        ttk.Button(buton_cercevesi, text="Kirala", command=self.kirala_formu).grid(row=0, column=2, padx=5)
        ttk.Button(buton_cercevesi, text="İade Et", command=self.arac_iade).grid(row=0, column=3, padx=5)
        ttk.Button(buton_cercevesi, text="Düzenle", command=self.duzenle_formu).grid(row=0, column=4, padx=5)

        self.verileri_goster()

    def verileri_goster(self):

        for oge in self.tablo.get_children():
            self.tablo.delete(oge)

        for arac in self.uygulama.araclar:
            self.tablo.insert("", "end", values=(
                arac["plaka"],
                arac["marka"],
                arac["model"],
                arac["gunluk_ucret"],
                arac["durum"]
            ))

    def secili_plaka(self):
        secili_oge = self.tablo.focus()
        if not secili_oge:
            messagebox.showerror("Hata", "Lütfen bir araç seçin.")
            return None

        return str(self.tablo.item(secili_oge)["values"][0]).strip()

    # arac ekle fonksiyonu
    def ekle_formu(self):
        yeni_pencere = tk.Toplevel(self.pencere)
        yeni_pencere.title("Araç Ekle")

        etiketler = ["Plaka", "Marka", "Model", "Ücret"]
        girisler = {}

        for i, etiket_metni in enumerate(etiketler):
            ttk.Label(yeni_pencere, text=etiket_metni).grid(row=i, column=0, padx=5, pady=5)
            giris = ttk.Entry(yeni_pencere)
            giris.grid(row=i, column=1, padx=5, pady=5)
            girisler[etiket_metni] = giris

        def kaydet():
            try:
                self.uygulama.arac_ekle(
                    girisler["Plaka"].get().strip(),
                    girisler["Marka"].get().strip(),
                    girisler["Model"].get().strip(),
                    girisler["Ücret"].get().strip()
                )

                messagebox.showinfo("Başarılı", "Araç eklendi.")
                yeni_pencere.destroy()
                self.verileri_goster()

            except Exception as e:
                messagebox.showerror("Hata", str(e))

        ttk.Button(yeni_pencere, text="Kaydet", command=kaydet).grid(row=5, columnspan=2)

    #arac sil fonksiyonu
    def arac_sil(self):
        plaka = self.secili_plaka()

        if not plaka:
            return

        if not messagebox.askyesno("Onay", "Bu aracı silmek istiyor musunuz?"):
            return

        try:
            self.uygulama.arac_sil(plaka.strip())
            messagebox.showinfo("Başarılı", "Araç silindi.")
            self.verileri_goster()

        except Exception as e:
            messagebox.showerror("Hata", str(e))

    # arac kirala fonksiyonu
    def kirala_formu(self):
        secili_oge = self.tablo.focus()

        if not secili_oge:
            messagebox.showerror("Hata", "Lütfen araç seçin.")
            return

        degerler = self.tablo.item(secili_oge)["values"]
        plaka = str(degerler[0]).strip()
        durum = str(degerler[4]).strip()

        if durum == "kirada":
            messagebox.showerror("Hata", "Bu araç zaten kirada, kiralanamaz.")
            return

        if durum == "bakımda":
            messagebox.showerror("Hata", "Bu araç bakımda, kiralanamaz.")
            return

        # popup
        yeni_pencere = tk.Toplevel(self.pencere)
        yeni_pencere.title("Araç Kirala")

        ttk.Label(yeni_pencere, text="Müşteri").grid(row=0, column=0)
        musteri = ttk.Entry(yeni_pencere)
        musteri.grid(row=0, column=1)

        ttk.Label(yeni_pencere, text="Başlangıç").grid(row=1, column=0)
        baslangic = ttk.Entry(yeni_pencere)
        baslangic.grid(row=1, column=1)

        ttk.Label(yeni_pencere, text="Bitiş").grid(row=2, column=0)
        bitis = ttk.Entry(yeni_pencere)
        bitis.grid(row=2, column=1)

        def kirala():
            try:
                ucret = self.uygulama.arac_kirala(
                    plaka,
                    musteri.get().strip(),
                    baslangic.get().strip(),
                    bitis.get().strip()
                )

                messagebox.showinfo("Başarılı", f"Toplam ücret: {ucret} TL")
                yeni_pencere.destroy()
                self.verileri_goster()

            except Exception as e:
                messagebox.showerror("Hata", str(e))

        ttk.Button(yeni_pencere, text="Kirala", command=kirala).grid(row=3, columnspan=2)

    # arac iade fonksiyonu
    def arac_iade(self):
        plaka = self.secili_plaka()

        if not plaka:
            return

        if not messagebox.askyesno("Onay", "İade edilsin mi?"):
            return

        try:
            self.uygulama.arac_iade(plaka.strip())
            messagebox.showinfo("Başarılı", "Araç iade edildi.")
            self.verileri_goster()

        except Exception as e:
            messagebox.showerror("Hata", str(e))

    # arac duzenle fonksiyonu
    def duzenle_formu(self):
        plaka = self.secili_plaka()

        if not plaka:
            return

        yeni_pencere = tk.Toplevel(self.pencere)
        yeni_pencere.title("Düzenle")

        ttk.Label(yeni_pencere, text="Yeni Model").grid(row=0, column=0)
        model = ttk.Entry(yeni_pencere)
        model.grid(row=0, column=1)

        ttk.Label(yeni_pencere, text="Yeni Ücret").grid(row=1, column=0)
        ucret = ttk.Entry(yeni_pencere)
        ucret.grid(row=1, column=1)

        ttk.Label(yeni_pencere, text="Durum").grid(row=2, column=0)
        durum_kutusu = ttk.Combobox(yeni_pencere, values=["müsait", "kirada", "bakımda"])
        durum_kutusu.grid(row=2, column=1)

        def kaydet():
            try:
                yeni_model = model.get().strip()
                yeni_ucret = ucret.get().strip()
                yeni_durum = durum_kutusu.get().strip()

                if not yeni_model and not yeni_ucret and not yeni_durum:
                    messagebox.showerror("Hata", "En az bir alan doldurulmalıdır.")
                    return

                self.uygulama.arac_duzenle(
                    plaka.strip(),
                    yeni_model or None,
                    yeni_ucret or None,
                    yeni_durum or None
                )

                messagebox.showinfo("Başarılı", "Güncellendi.")
                yeni_pencere.destroy()
                self.verileri_goster()

            except Exception as e:
                messagebox.showerror("Hata", str(e))

        ttk.Button(yeni_pencere, text="Kaydet", command=kaydet).grid(row=3, columnspan=2)