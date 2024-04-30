import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        mese = self._view.dd_mese.value
        umidita_genova = self._model.get_umidita_media(mese,"Genova")
        umidita_torino = self._model.get_umidita_media(mese, "Torino")
        umidita_milano = self._model.get_umidita_media(mese, "Milano")
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media nel mese selezionato:\n"
                                                      f"{umidita_genova}\n"
                                                      f"{umidita_milano}\n"
                                                      f"{umidita_torino}"))
        self._view.update_page()



    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()
        mese = self._view.dd_mese.value
        analisi = self._model.calcola_percorsi(mese)

        self._view.lst_result.controls.append(ft.Text(f" Il costo della soluzione ottimale è: {analisi[1]}\n"))
        for element in analisi[0]:
            self._view.lst_result.controls.append(ft.Text(f"{element.__str__()}"))
        self._view.update_page()


    def read_mese(self, e):
        self._mese = int(e.control.value)

