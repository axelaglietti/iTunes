import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAlbum = None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        try:
            totDint = int(self._view._txtInDurata.value)
        except ValueError:
            warnings.warn_explicit(message="Non è un intero", category=Warning, filename="controller.py", lineno=16)
            return
        self._model.buildGraph(totDint)
        nodes = self._model._graph.nodes
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente."))
        nodi, archi = self._model.getGraphSize()
        self._view.txt_result.controls.append(ft.Text(f"Nodi: {nodi}, Archi: {archi}"))
        """for n in nodes:
            self._view._ddAlbum.options.append(ft.dropdown.Option(data=n, text=n.Title, on_click=self.getSelectedAlbum()))"""
        listDD = map(lambda x: ft.dropdown.Option(data=x, text=x.Title), nodes)
        self._view._ddAlbum.options = listDD
        self._view.update_page()

    def handleAnalisi(self, e):
        self._view.txt_result.controls.clear()
        if self._choiceAlbum is None:
            warnings.warn(f"Album field not selected")
        else:
            sizeC, totDurata = self._model.getConnessaDetails(self._choiceAlbum)
            self._view.txt_result.controls.append(ft.Text(f"La componente connessa che include {self._choiceAlbum} ha dimensione {sizeC} e durata totale {totDurata}"))
        self._view.update_page()


    def handleGetSetAlbum(self, e):
        pass


    def getSelectedAlbum(self, e):
        if e.control.data is None:
            self._choiceAlbum = None
        else:
            self._choiceAlbum = e.control.data