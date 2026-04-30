import json
from datetime import datetime


def tarih_donustur_yukle(tarih_str): #gösterirken DD/MM/YYYY
    if tarih_str:
        return datetime.strptime(tarih_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    return None


def tarih_donustur_kaydet(tarih_str): #kaydederken YYYY-MM-DD
    if tarih_str:
        return datetime.strptime(tarih_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    return None


def verileri_yukle(dosya_adi="araclar.json"):
    try:
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)
            return veri if isinstance(veri, list) else []

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:  # JSON dosyası bozulma hatası
        print("Veri dosyası bozuk, yeni bir liste oluşturuluyor.")
        return []


def verileri_kaydet(araclar, dosya_adi="araclar.json"):
    araclar_kopya = []

    for arac in araclar:
        arac_kopya = arac.copy()
        arac_kopya['baslangic_tarihi'] = tarih_donustur_kaydet(arac.get('baslangic_tarihi'))
        arac_kopya['bitis_tarihi'] = tarih_donustur_kaydet(arac.get('bitis_tarihi'))
        araclar_kopya.append(arac_kopya)

    with open(dosya_adi, "w", encoding="utf-8") as dosya:
        json.dump(araclar_kopya, dosya, ensure_ascii=False, indent=4)


