import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._compagnie = None
        self._aeroportoP = None
        self._aeroportoA = None

    def handleAnalizza(self, e):
        self._view._txt_result.controls.clear()

        try:
            self._compagnie = int(self._view._txtInNumC.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserisci un avlore numerico!"))
            self._view.update_page()
            return

        aeroporti = self._model.buildGraph(self._compagnie)
        self._view._ddAeroportoP.disabled = False
        self._view._ddAeroportoA.disabled = False
        self._view._btnConnessi.disabled = False
        self._view._btnPercorso.disabled = False

        for a in aeroporti:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=a, text=a.AIRPORT, on_click=self.readDDP))
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(data=a, text=a.AIRPORT, on_click=self.readDDA))


        self._view.update_page()

    def readDDP(self, e):
        self._aeroportoP = e.control.data

    def readDDA(self, e):
        self._aeroportoA = e.control.data

    def handleConnessi(self, e):
        self._view._txt_result.controls.clear()

        if self._aeroportoP is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare l'aeroporto!"))
            self._view.update_page()
            return

        conn = self._model.getConnessi(self._aeroportoP)
        for c in conn:
            self._view._txt_result.controls.append(ft.Text(f"{c[0]} --> numero voli = {c[1]}"))

        self._view.update_page()

    def handleTestConnessione(self, e):
        self._view._txt_result.controls.clear()

        if self._aeroportoP is None or self._aeroportoA is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare gli aeroporti!"))
            self._view.update_page()
            return

        test = self._model.testConnessione(self._aeroportoP, self._aeroportoA)
        if test==True:
            self._view._txt_result.controls.append(ft.Text("Aeroporti connessi"))
            self._view._txtInNumTratte.disabled = False
            self._view._btnCercaItinerario.disabled = False
        else:
            self._view._txt_result.controls.append(ft.Text("Aeroporti non connessi, selezionarne altri"))

        self._view.update_page()


    def handleCercaItinerario(self, e):
        self._view._txt_result.controls.clear()

        if self._aeroportoP is None or self._aeroportoA is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare gli aeroporti!"))
            self._view.update_page()
            return

        try:
            self._soglia = int(self._view._txtInNumTratte.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("Inserire una soglia!"))
            self._view.update_page()
            return

        score, path = self._model.getPath(self._aeroportoP, self._aeroportoA, self._soglia)

        self._view._txt_result.controls.append(ft.Text(f"Trovato percorso di peso: {score}"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(f"{p.AIRPORT}"))

        self._view.update_page()

