import copy
from math import inf
import threading
from database import meteo_dao


class Model:
    meteo = meteo_dao.MeteoDao()

    def __init__(self):
        self.situazioni = []
        self.costo_migliore = float(inf)

    def get_umidita_media(self, mese, localita):
        situa = self.meteo.get_situa_mese(mese, localita)
        um_totale = 0
        for situazione in situa:
            um_totale += situazione.umidita
        return f"{localita}: {round(float(um_totale / len(situa)), 4)}"

    def get_15_gg(self, mese, localita):
        return self.meteo.get_situa_15_gg(mese, localita)

    def calcola_percorsi(self, mese):

        gg_milano = self.get_15_gg(mese, "Milano")
        gg_torino = self.get_15_gg(mese, "Torino")
        gg_genova = self.get_15_gg(mese, "Genova")

        # combo = self.ricorsione([],gg_milano,gg_torino,gg_genova )
        thread = threading.Thread(target=self.ricorsione_1, args=([], gg_milano, gg_torino, gg_genova, 0))
        thread.start()
        # Attendere il completamento del thread prima di continuare
        thread.join()
        situe = []
        for num in range(len(self.situazioni)):
            if self.situazioni[num] == 0:
                situe.append(gg_milano[num])
            elif self.situazioni[num] == 1:
                situe.append(gg_torino[num])
            elif self.situazioni[num] == 2:
                situe.append(gg_genova[num])

        return situe, self.costo_migliore

    def conta_citta(self, lista_parziale, nome_citta):
        citta = 0
        for element in lista_parziale:
            if element.localita == nome_citta:
                citta += 1
        return citta

    def num_citta_accettabili(self, lista):
        mil = 0
        to = 0
        ge = 0
        for elemento in lista:
            if elemento.localita == "Milano":
                mil += 1
            if elemento.localita == "Torino":
                to += 1
            if elemento.localita == "Genova":
                ge += 1
        if mil <= 6 and to <= 6 and ge <= 6:
            return True
        return False

    def ultima_localita(self, lista_parziale, nome_citta):
        if lista_parziale[-1].localita == nome_citta:
            return True
        return False

    def sol_max_6_occorrenze(self, lista_parziale, numero):
        if lista_parziale.count(numero) <= 6:
            return True
        return False

    def sol_accettabile(self, lista_parziale):
        """ ritorna vero se ogni numero nella lista compare almeno 3 volte di seguito"""

        flag = True
        consecutive_count = 1  # Contatore per tenere traccia delle occorrenze consecutive dell'elemento corrente

        for i in range(len(lista_parziale) - 4):
            if lista_parziale[i] == lista_parziale[i + 1]:
                consecutive_count += 1

            else:
                if consecutive_count < 3:
                    flag = False
                consecutive_count = 1

        return flag

    def ricorsione_1(self, parziale, umidita_milano, umidita_torino, umidita_genova, costo):

        if len(parziale) == 15:  # caso base: tutti i giorni sono stati visitati

            if costo < self.costo_migliore and self.sol_accettabile(parziale):
                self.situazioni = copy.deepcopy(parziale)
                self.costo_migliore = costo
                print(f"{parziale} costo : {self.costo_migliore}")

            # esplora tutte le possibili scelte per il giorno successivo
        for citta in range(3):
            # 0: Milano, 1: Torino, 2: Genova
            if citta == 0:
                if len(umidita_milano) > len(parziale):
                    nuovo_costo = costo + umidita_milano[len(parziale)].umidita + (
                        0 if (len(parziale) == 0 or parziale[-1] == 0) else 100)
                    nuovo_parziale = parziale + [0]

                    if self.sol_max_6_occorrenze(nuovo_parziale, 0):
                        self.ricorsione_1(nuovo_parziale, umidita_milano,
                                          umidita_torino,
                                          umidita_genova, nuovo_costo)

            if citta == 1:
                if len(umidita_torino) > len(parziale):
                    nuovo_costo = costo + umidita_torino[len(parziale)].umidita + (
                        0 if (len(parziale) == 0 or parziale[-1] == 1) else 100)
                    nuovo_parziale = parziale + [1]

                    if self.sol_max_6_occorrenze(nuovo_parziale, 1):
                        self.ricorsione_1(nuovo_parziale, umidita_milano,
                                          umidita_torino,
                                          umidita_genova, nuovo_costo)

            if citta == 2:
                if len(umidita_genova) > len(parziale):
                    nuovo_costo = costo + umidita_genova[len(parziale)].umidita + (
                        0 if (len(parziale) == 0 or parziale[-1] == 2) else 100)
                    nuovo_parziale = parziale + [2]

                    if self.sol_max_6_occorrenze(nuovo_parziale, 2):
                        self.ricorsione_1(nuovo_parziale, umidita_milano,
                                          umidita_torino,
                                          umidita_genova, nuovo_costo)

        if len(parziale) > 0:
            parziale.pop()
