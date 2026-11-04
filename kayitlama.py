
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path
from openpyxl import load_workbook
from copy import copy
from datetime import date, datetime


# SECILEN EXCEL DOSYASINI SAKLAR
def dosya_sec(dosya_yazi, secilen_dosya, temizle_butonu, bos_buton):
    dosya_yolu = filedialog.askopenfilename(
        title="Excel dosyasi sec",
        filetypes=[("Excel Dosyalari", "*.xlsx")]
    )

    if dosya_yolu:
        secilen_dosya["yol"] = dosya_yolu
        dosya_adi = Path(dosya_yolu).name

        dosya_yazi.config(text=f"Secilen dosya: {dosya_adi}")
        temizle_butonu.config(state="normal")
        bos_buton.config(state="normal")


# YINELENEN SATIRLARI TEMIZLER
def yinelenenleri_temizle(secilen_dosya, durum_yazi):
    dosya_yolu = secilen_dosya["yol"]

    if not dosya_yolu:
        return

    try:
        workbook = load_workbook(dosya_yolu)
        sheet = workbook.active

        gorulen_satirlar = set()
        silinecek_satirlar = []

        for satir_no in range(2, sheet.max_row + 1):
            satir_verileri = tuple(
                hucre.value for hucre in sheet[satir_no]
            )

            if all(deger is None for deger in satir_verileri):
                continue

            if satir_verileri in gorulen_satirlar:
                silinecek_satirlar.append(satir_no)
            else:
                gorulen_satirlar.add(satir_verileri)

        kaydetme_yolu = filedialog.asksaveasfilename(
            title="Temizlenmis dosyayi kaydet",
            initialfile=Path(dosya_yolu).stem + "_temizlenmis.xlsx",
            defaultextension=".xlsx",
            filetypes=[("Excel Dosyalari", "*.xlsx")]
        )

        if not kaydetme_yolu:
            workbook.close()
            return

        if Path(kaydetme_yolu).resolve() == Path(dosya_yolu).resolve():
            workbook.close()
            messagebox.showwarning("Uyari", "Orijinal dosyanin uzerine kaydedemezsin.")
            return

        for satir_no in reversed(silinecek_satirlar):
            sheet.delete_rows(satir_no)

        workbook.save(kaydetme_yolu)
        workbook.close()

        durum_yazi.config(
            text=f"{len(silinecek_satirlar)} tekrar temizlendi."
        )

        messagebox.showinfo(
            "Tamamlandi",
            f"{len(silinecek_satirlar)} yinelenen satir temizlendi.\n\n{kaydetme_yolu}"
        )

    except Exception as hata:
        messagebox.showerror("Hata", str(hata))


# BOS HUCReLERI BULUR
def bos_hucreleri_bul(secilen_dosya, durum_yazi):
    dosya_yolu = secilen_dosya["yol"]

    if not dosya_yolu:
        return

    try:
        workbook = load_workbook(dosya_yolu)
        sheet = workbook.active

        bos_hucreler = []

        for satir in sheet.iter_rows():
            for hucre in satir:
                deger = hucre.value

                if deger is None or (
                    isinstance(deger, str) and not deger.strip()
                ):
                    if hucre.row == 1:
                        sutun_bilgisi = "Baslik hucresi"
                    else:
                        baslik = sheet.cell(
                            row=1,
                            column=hucre.column
                        ).value

                        sutun_bilgisi = (
                            f"Sutun: {baslik}"
                            if baslik else "Sutun basligi bos"
                        )

                    bos_hucreler.append(
                        f"{hucre.coordinate} - {sutun_bilgisi}"
                    )

        workbook.close()

        if not bos_hucreler:
            durum_yazi.config(text="Bos hucre bulunamadi.")
            messagebox.showinfo("Sonuc", "Bos hucre bulunamadi.")
            return

        durum_yazi.config(
            text=f"{len(bos_hucreler)} bos hucre bulundu."
        )

        pencere = tk.Toplevel()
        pencere.title("Bos Hucre Raporu")
        pencere.geometry("450x400")

        baslik = tk.Label(
            pencere,
            text=f"Toplam {len(bos_hucreler)} bos hucre bulundu.",
            font=("Arial", 13, "bold")
        )
        baslik.pack(pady=10)

        metin = tk.Text(pencere, width=55, height=20)
        metin.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        kaydirma = tk.Scrollbar(pencere, command=metin.yview)
        kaydirma.pack(side="right", fill="y")

        metin.config(yscrollcommand=kaydirma.set)

        for hucre in bos_hucreler:
            metin.insert("end", hucre + "\n")

        metin.config(state="disabled")

    except Exception as hata:
        messagebox.showerror("Hata", str(hata))


# EXCEL DOSYALARINI BIRLESTIRIR
def excel_dosyalarini_birlestir(durum_yazi):
    dosya_yollari = filedialog.askopenfilenames(
        title="Birlestirilecek Excel dosyalarini sec",
        filetypes=[("Excel Dosyalari", "*.xlsx")]
    )

    if len(dosya_yollari) < 2:
        messagebox.showwarning(
            "Uyari",
            "En az iki Excel dosyasi secmelisin."
        )
        return

    workbooklar = []

    try:
        for yol in dosya_yollari:
            workbooklar.append(load_workbook(yol))

        ilk_sheet = workbooklar[0].active

        ilk_basliklar = tuple(
            hucre.value for hucre in ilk_sheet[1]
        )

        for sira, workbook in enumerate(workbooklar[1:], start=2):
            diger_sheet = workbook.active

            diger_basliklar = tuple(
                hucre.value for hucre in diger_sheet[1]
            )

            if diger_basliklar != ilk_basliklar:
                raise ValueError(
                    f"{sira}. dosyanin sutun basliklari ilk dosyayla ayni degil."
                )

        for workbook in workbooklar[1:]:
            sheet = workbook.active

            for satir in sheet.iter_rows(min_row=2, values_only=True):
                if all(deger is None for deger in satir):
                    continue

                ilk_sheet.append(satir)

        kaydetme_yolu = filedialog.asksaveasfilename(
            title="Birlesmis dosyayi kaydet",
            initialfile="birlesmis_excel.xlsx",
            defaultextension=".xlsx",
            filetypes=[("Excel Dosyalari", "*.xlsx")]
        )

        if not kaydetme_yolu:
            return

        secilen_yollar = {
            str(Path(yol).resolve()) for yol in dosya_yollari
        }

        if str(Path(kaydetme_yolu).resolve()) in secilen_yollar:
            messagebox.showwarning(
                "Uyari",
                "Orijinal dosyalarin uzerine kaydedemezsin."
            )
            return

        workbooklar[0].save(kaydetme_yolu)

        durum_yazi.config(text="Dosyalar basariyla birlestirildi.")

        messagebox.showinfo(
            "Tamamlandi",
            f"{len(dosya_yollari)} Excel dosyasi birlestirildi.\n\n{kaydetme_yolu}"
        )

    except Exception as hata:
        messagebox.showerror("Birlestirme hatasi", str(hata))

    finally:
        for workbook in workbooklar:
            workbook.close()


# EXCEL VERILERINI SIRALAR
def excel_sirala(durum_yazi, root):
    dosya_yolu = filedialog.askopenfilename(
        title="Siralanacak Excel dosyasini sec",
        filetypes=[("Excel Dosyalari", "*.xlsx")]
    )

    if not dosya_yolu:
        return

    workbook = None

    try:
        workbook = load_workbook(dosya_yolu)
        sheet = workbook.active

        if sheet.max_row < 2:
            messagebox.showwarning(
                "Uyari",
                "Siralanacak veri bulunamadi."
            )
            return

        sutun_no = simpledialog.askinteger(
            "Sutun sec",
            f"Siralamak istedigin sutunun numarasini gir.\n"
            f"1 ile {sheet.max_column} arasinda bir sayi yaz.",
            parent=root,
            minvalue=1,
            maxvalue=sheet.max_column
        )

        if sutun_no is None:
            return

        baslik = sheet.cell(row=1, column=sutun_no).value

        artan = messagebox.askyesno(
            "Siralama yonu",
            f"'{baslik}' sutunu artan siralansin mi?\n\n"
            "Evet: A-Z / Kucukten buyuge\n"
            "Hayir: Z-A / Buyukten kucuge"
        )

        satirlar = []

        for satir_no in range(2, sheet.max_row + 1):
            satir_verileri = []

            for hucre in sheet[satir_no]:
                satir_verileri.append({
                    "value": hucre.value,
                    "style": copy(hucre._style),
                    "hyperlink": copy(hucre.hyperlink),
                    "comment": copy(hucre.comment)
                })

            satirlar.append(satir_verileri)

        def siralama_anahtari(satir):
            deger = satir[sutun_no - 1]["value"]

            if isinstance(deger, (datetime, date)):
                return (0, 1, deger)

            if isinstance(deger, (int, float)):
                return (0, 2, deger)

            return (0, 3, str(deger).casefold())

        dolu_satirlar = [
            satir for satir in satirlar
            if satir[sutun_no - 1]["value"] is not None
            and not (
                isinstance(satir[sutun_no - 1]["value"], str)
                and not satir[sutun_no - 1]["value"].strip()
            )
        ]

        bos_satirlar = [
            satir for satir in satirlar
            if satir not in dolu_satirlar
        ]

        dolu_satirlar.sort(
            key=siralama_anahtari,
            reverse=not artan
        )

        siralanmis_satirlar = dolu_satirlar + bos_satirlar

        for satir_no, satir_verileri in enumerate(
            siralanmis_satirlar, start=2
        ):
            for sutun, veri in enumerate(satir_verileri, start=1):
                hucre = sheet.cell(row=satir_no, column=sutun)

                hucre.value = veri["value"]
                hucre._style = copy(veri["style"])
                hucre.hyperlink = copy(veri["hyperlink"])
                hucre.comment = copy(veri["comment"])

        kaydetme_yolu = filedialog.asksaveasfilename(
            title="Siralanmis dosyayi kaydet",
            initialfile=Path(dosya_yolu).stem + "_siralanmis.xlsx",
            defaultextension=".xlsx",
            filetypes=[("Excel Dosyalari", "*.xlsx")]
        )

        if not kaydetme_yolu:
            return

        if Path(kaydetme_yolu).resolve() == Path(dosya_yolu).resolve():
            messagebox.showwarning(
                "Uyari",
                "Orijinal dosyanin uzerine kaydedemezsin."
            )
            return

        workbook.save(kaydetme_yolu)

        durum_yazi.config(text="Excel dosyasi basariyla siralandi.")

        messagebox.showinfo(
            "Tamamlandi",
            f"'{baslik}' sutunu siralandi.\n\n{kaydetme_yolu}"
        )

    except Exception as hata:
        messagebox.showerror("Siralama hatasi", str(hata))

    finally:
        if workbook is not None:
            workbook.close()


# ANA UYGULAMA PENCERESI
def main():
    root = tk.Tk()
    root.title("Excel Asistani")
    root.geometry("520x480")

    secilen_dosya = {"yol": None}

    baslik = tk.Label(
        root,
        text="Excel Asistanı",
        font=("Arial", 20, "bold")
    )
    baslik.pack(pady=20)

    aciklama = tk.Label(
        root,
        text="Excel islemlerinizi kolaylastirin."
    )
    aciklama.pack(pady=5)

    dosya_yazi = tk.Label(
        root,
        text="Henüz dosya seçilmedi."
    )
    dosya_yazi.pack(pady=10)

    temizle_butonu = tk.Button(
        root,
        text="Tekrarları Temizle",
        state="disabled",
        command=lambda: yinelenenleri_temizle(
            secilen_dosya, durum_yazi
        )
    )
    temizle_butonu.pack(pady=8)

    bos_buton = tk.Button(
        root,
        text="Boş Hücreleri Bul",
        state="disabled",
        command=lambda: bos_hucreleri_bul(
            secilen_dosya, durum_yazi
        )
    )
    bos_buton.pack(pady=8)

    sec_butonu = tk.Button(
        root,
        text="Excel Dosyası Seç",
        command=lambda: dosya_sec(
            dosya_yazi,
            secilen_dosya,
            temizle_butonu,
            bos_buton
        )
    )
    sec_butonu.pack(pady=8)

    birlestir_butonu = tk.Button(
        root,
        text="Excel Dosyalarını Birleştir",
        command=lambda: excel_dosyalarini_birlestir(durum_yazi)
    )
    birlestir_butonu.pack(pady=8)

    sirala_butonu = tk.Button(
        root,
        text="Excel Verilerini Sirala",
        command=lambda: excel_sirala(durum_yazi, root)
    )
    sirala_butonu.pack(pady=8)

    durum_yazi = tk.Label(
        root,
        text="Islem bekleniyor."
    )
    durum_yazi.pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
