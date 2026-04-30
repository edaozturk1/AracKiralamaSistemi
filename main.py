import tkinter as tk

from backend.islemler import (
    arac_ekle,
    arac_sil,
    arac_kirala,
    arac_iade_et,
    arac_duzenle
)

from backend.dosya import verileri_yukle, verileri_kaydet, tarih_donustur_yukle
from gui import Arayuz


class Uygulama:
    def __init__(self):
        self.araclar = verileri_yukle()

        for arac in self.araclar:
            arac["baslangic_tarihi"] = tarih_donustur_yukle(arac.get("baslangic_tarihi"))
            arac["bitis_tarihi"] = tarih_donustur_yukle(arac.get("bitis_tarihi"))

    def arac_ekle(self, plaka, marka, model, ucret):
        arac_ekle(self.araclar, plaka, marka, model, ucret)
        verileri_kaydet(self.araclar)

    def arac_sil(self, plaka):
        arac_sil(self.araclar, plaka)
        verileri_kaydet(self.araclar)

    def arac_kirala(self, plaka, musteri, baslangic, bitis):
        ucret = arac_kirala(self.araclar, plaka, musteri, baslangic, bitis)
        verileri_kaydet(self.araclar)
        return ucret

    def arac_iade(self, plaka):
        arac_iade_et(self.araclar, plaka)
        verileri_kaydet(self.araclar)

    def arac_duzenle(self, plaka, model, ucret, durum):
        arac_duzenle(self.araclar, plaka, model, ucret, durum)
        verileri_kaydet(self.araclar)


if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = Uygulama()
    arayuz = Arayuz(pencere, uygulama)
    pencere.mainloop()