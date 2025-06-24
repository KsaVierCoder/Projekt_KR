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
