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
