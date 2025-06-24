# === IMPORTY ===
from tkinter import *
from tkinter import ttk
import tkintermapview
import requests
from bs4 import BeautifulSoup

# === LISTY ===
sieci_dronow = []
operatorzy = []
klienci = []

# === KLASY ===
class SiecDronow:
    def __init__(self, nazwa, lokalizacja):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.wspolrzedne = self.pobierz_wspolrzedne()
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Sieć: {self.nazwa}")

    def pobierz_wspolrzedne(self):
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        latitude = float(soup.select(".latitude")[1].text.replace(",", "."))
        longitude = float(soup.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]

class OperatorDrona:
    def __init__(self, imie, nazwisko, siec):
        self.imie = imie
        self.nazwisko = nazwisko
        self.siec = siec
        self.wspolrzedne = siec.wspolrzedne
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Operator: {self.imie} {self.nazwisko}")

class Klient:
    def __init__(self, imie, siec):
        self.imie = imie
        self.siec = siec
        self.wspolrzedne = siec.wspolrzedne
        self.marker = map_widget.set_marker(self.wspolrzedne[0], self.wspolrzedne[1], text=f"Klient: {self.imie}")

# === FUNKCJE MAPY ===
def pokaz_wszystkie_sieci():
    map_widget.set_position(52.23, 21.0)
    map_widget.set_zoom(6)
    for o in operatorzy: o.marker.delete()
    for k in klienci: k.marker.delete()
    for s in sieci_dronow:
        s.marker = map_widget.set_marker(s.wspolrzedne[0], s.wspolrzedne[1], text=f"Sieć: {s.nazwa}")

def pokaz_wszystkich_operatorow():
    for s in sieci_dronow: s.marker.delete()
    for k in klienci: k.marker.delete()
    for o in operatorzy:
        o.marker = map_widget.set_marker(o.wspolrzedne[0], o.wspolrzedne[1], text=f"Operator: {o.imie} {o.nazwisko}")

def pokaz_klientow_sieci():
    for s in sieci_dronow: s.marker.delete()
    for o in operatorzy: o.marker.delete()
    for k in klienci: k.marker.delete()
    idx = combobox_siec_na_mapie.current()
    if idx >= 0:
        siec = sieci_dronow[idx]
        for k in klienci:
            if k.siec == siec:
                k.marker = map_widget.set_marker(k.wspolrzedne[0], k.wspolrzedne[1], text=f"Klient: {k.imie}")

def pokaz_operatorow_sieci():
    for s in sieci_dronow: s.marker.delete()
    for o in operatorzy: o.marker.delete()
    for k in klienci: k.marker.delete()
    idx = combobox_siec_na_mapie.current()
    if idx >= 0:
        siec = sieci_dronow[idx]
        for o in operatorzy:
            if o.siec == siec:
                o.marker = map_widget.set_marker(o.wspolrzedne[0], o.wspolrzedne[1], text=f"Operator: {o.imie} {o.nazwisko}")

# === FUNKCJE LIST ===
def dodaj_siec_z_odswiezeniem():
    dodaj_siec()
    odswiez_siec_dla_operatora()
    odswiez_siec_dla_klienta()
    odswiez_siec_na_mapie()

def dodaj_siec():
    nazwa = entry_nazwa_sieci.get()
    lokalizacja = entry_lokalizacja_sieci.get()
    siec = SiecDronow(nazwa, lokalizacja)
    sieci_dronow.append(siec)
    listbox_sieci.insert(END, f"{siec.nazwa} ({siec.lokalizacja})")
    entry_nazwa_sieci.delete(0, END)
    entry_lokalizacja_sieci.delete(0, END)

def usun_siec():
    idx = listbox_sieci.curselection()
    if idx:
        index = idx[0]
        sieci_dronow[index].marker.delete()
        sieci_dronow.pop(index)
        listbox_sieci.delete(index)

def dodaj_operatora():
    imie = entry_imie_operatora.get()
    nazwisko = entry_nazwisko_operatora.get()
    idx = combobox_siec_dla_operatora.current()
    if idx >= 0:
        siec = sieci_dronow[idx]
        operator = OperatorDrona(imie, nazwisko, siec)
        operatorzy.append(operator)
        listbox_operatorzy.insert(END, f"{operator.imie} {operator.nazwisko}")
        entry_imie_operatora.delete(0, END)
        entry_nazwisko_operatora.delete(0, END)

def usun_operatora():
    idx = listbox_operatorzy.curselection()
    if idx:
        index = idx[0]
        operatorzy[index].marker.delete()
        operatorzy.pop(index)
        listbox_operatorzy.delete(index)

def dodaj_klienta():
    imie = entry_imie_klienta.get()
    idx = combobox_siec_dla_klienta.current()
    if idx >= 0:
        siec = sieci_dronow[idx]
        klient = Klient(imie, siec)
        klienci.append(klient)
        listbox_klienci.insert(END, imie)
        entry_imie_klienta.delete(0, END)

def usun_klienta():
    idx = listbox_klienci.curselection()
    if idx:
        index = idx[0]
        klienci[index].marker.delete()
        klienci.pop(index)
        listbox_klienci.delete(index)

# === COMBOBOXY ODSWIEZANIE ===
def odswiez_siec_dla_operatora():
    combobox_siec_dla_operatora['values'] = [s.nazwa for s in sieci_dronow]

def odswiez_siec_dla_klienta():
    combobox_siec_dla_klienta['values'] = [s.nazwa for s in sieci_dronow]

def odswiez_siec_na_mapie():
    combobox_siec_na_mapie['values'] = [s.nazwa for s in sieci_dronow]

# === GUI ===
root = Tk()
root.geometry("1200x800")
root.title("System zarządzania siecią lotów dronów")

frame_siec = Frame(root)
frame_siec.grid(row=0, column=0, padx=10, pady=10, sticky=N)

frame_operator = Frame(root)
frame_operator.grid(row=0, column=1, padx=10, pady=10, sticky=N)

frame_klient = Frame(root)
frame_klient.grid(row=0, column=2, padx=10, pady=10, sticky=N)

frame_kontrola_mapy = Frame(root)
frame_kontrola_mapy.grid(row=1, column=0, columnspan=3, pady=10)

frame_mapa = Frame(root)
frame_mapa.grid(row=2, column=0, columnspan=3)

# === SIEĆ ===
Label(frame_siec, text="Dodaj sieć dronów").pack()
Label(frame_siec, text="Nazwa:").pack()
entry_nazwa_sieci = Entry(frame_siec)
entry_nazwa_sieci.pack()
Label(frame_siec, text="Lokalizacja (Wikipedia):").pack()
entry_lokalizacja_sieci = Entry(frame_siec)
entry_lokalizacja_sieci.pack()
Button(frame_siec, text="Dodaj sieć", command=dodaj_siec_z_odswiezeniem).pack()
Button(frame_siec, text="Usuń sieć", command=usun_siec).pack()
listbox_sieci = Listbox(frame_siec, width=30)
listbox_sieci.pack()

# === OPERATORZY ===
Label(frame_operator, text="Dodaj operatora").pack()
Label(frame_operator, text="Imię:").pack()
entry_imie_operatora = Entry(frame_operator)
entry_imie_operatora.pack()
Label(frame_operator, text="Nazwisko:").pack()
entry_nazwisko_operatora = Entry(frame_operator)
entry_nazwisko_operatora.pack()
Label(frame_operator, text="Sieć:").pack()
combobox_siec_dla_operatora = ttk.Combobox(frame_operator)
combobox_siec_dla_operatora.pack()
Button(frame_operator, text="Dodaj operatora", command=dodaj_operatora).pack()
Button(frame_operator, text="Usuń operatora", command=usun_operatora).pack()
listbox_operatorzy = Listbox(frame_operator, width=30)
listbox_operatorzy.pack()

# === KLIENCI ===
Label(frame_klient, text="Dodaj klienta").pack()
Label(frame_klient, text="Imię:").pack()
entry_imie_klienta = Entry(frame_klient)
entry_imie_klienta.pack()
Label(frame_klient, text="Sieć:").pack()
combobox_siec_dla_klienta = ttk.Combobox(frame_klient)
combobox_siec_dla_klienta.pack()
Button(frame_klient, text="Dodaj klienta", command=dodaj_klienta).pack()
Button(frame_klient, text="Usuń klienta", command=usun_klienta).pack()
listbox_klienci = Listbox(frame_klient, width=30)
listbox_klienci.pack()

# === MAPA KONTROLA ===
Label(frame_kontrola_mapy, text="Wybierz sieć:").grid(row=0, column=0, padx=5)
combobox_siec_na_mapie = ttk.Combobox(frame_kontrola_mapy, width=25)
combobox_siec_na_mapie.grid(row=0, column=1)

Button(frame_kontrola_mapy, text="Mapa wszystkich sieci", command=pokaz_wszystkie_sieci).grid(row=1, column=0, padx=5, pady=5)
Button(frame_kontrola_mapy, text="Mapa operatorów", command=pokaz_wszystkich_operatorow).grid(row=1, column=1, padx=5, pady=5)
Button(frame_kontrola_mapy, text="Klienci wybranej sieci", command=pokaz_klientow_sieci).grid(row=1, column=2, padx=5, pady=5)
Button(frame_kontrola_mapy, text="Operatorzy wybranej sieci", command=pokaz_operatorow_sieci).grid(row=1, column=3, padx=5, pady=5)

# === MAPA ===
map_widget = tkintermapview.TkinterMapView(frame_mapa, width=1150, height=500, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.pack()

root.mainloop()