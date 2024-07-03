import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()

    def buildGraph(self, compagnie):
        self._aeroporti = DAO.getAeroporti(compagnie)
        self._graph.clear()
        self._graph.add_nodes_from(self._aeroporti)

        for a1 in self._aeroporti:
            for a2 in self._aeroporti:
                if not self._graph.has_edge(a1, a2):
                    peso = DAO.getPeso(a1.ID, a2.ID)
                    if peso>0:
                        self._graph.add_edge(a1, a2, weight=peso)

        print(self._graph)

        return self._aeroporti

    def getConnessi(self, aeroporto):
        result = []
        conn = list(nx.neighbors(self._graph, aeroporto))
        for c in conn:
            result.append((c, self._graph[aeroporto][c]["weight"]))
        result.sort(key=lambda x:x[1], reverse=True)
        return result

    def testConnessione(self, partenza, arrivo):
        path = nx.shortest_path(self._graph, partenza, arrivo)
        if len(path)==0:
            return False
        return True

    def getPath(self, partenza, arrivo, soglia):

        self._bestSol = []
        self._bestScore = 0

        parziale = [partenza]
        for node in nx.neighbors(self._graph, partenza):
            parziale.append(node)
            self._ricorsione(parziale, arrivo, soglia)
            parziale.pop()

        return self._bestScore, self._bestSol


    def _ricorsione(self, parziale, arrivo, soglia):

        if parziale[-1] == arrivo:
            score = self._score(parziale)
            if score > self._bestScore:
                self._bestScore = score
                self._bestSol = parziale[:]
            return

        if len(parziale) == soglia+1:
            return

        for node in nx.neighbors(self._graph, parziale[-1]):
            if node not in parziale:
                parziale.append(node)
                self._ricorsione(parziale, arrivo, soglia)
                parziale.pop()

    def _score(self, list):
        score = 0
        for i in range(len(list) - 1):
            score += self._graph[list[i]][list[i+1]]["weight"]
        return score

