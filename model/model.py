import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestSet = None
        self._bestScore = None

    def getSetAlbum(self, a1, dTot):
        self._bestSet = None
        self._bestScore = None
        connessa = nx.node_connected_component(self._graph, a1)
        parziale = set(a1)
        connessa.remove(a1)
        self.ricorsione(parziale, connessa, dTot)
        return self._bestSet

    def ricorsione(self, parziale, connessa, dTot):
        # verificare se parziale è una sol ammissibile
        if self.durataTot(parziale) > dTot:
            return
        # verificare se parziale è migliore di best
        if len(parziale) > self._bestScore:
            self._bestScore = len(parziale)
            self._bestSet = copy.deepcopy(parziale)
            # non devo fare la return perchéà non ha senso uscire, posso ancora raggiungere nodi
        # ciclo su nodi raggiungibili -- ricorsione
        for c in connessa:
            if c not in parziale:
                parziale.add(c)
                rimanenti = copy.deepcopy(connessa) # per velocizzare la ricorsione
                rimanenti.remove(c)
                self.ricorsione(parziale, rimanenti, dTot)
                parziale.remove(c)

    def durataTot(self, listOfNodes):
        scoreTot = 0
        for n in listOfNodes:
            scoreTot += n.totD
        return scoreTot

    def buildGraph(self, d):
        self._graph.clear()
        self._idMap = {}
        self._graph.add_nodes_from(DAO.getAlbums(toMillisec(d)))
        self._idMap = {a.AlbumId: a for a in list(self._graph.nodes)}
        edges = DAO.getEdges(self._idMap)
        self._graph.add_edges_from(edges)

    def getConnessaDetails(self, v0):
        conn = nx.node_connected_component(self._graph, v0)
        durataTOT = 0
        for album in conn:
            durataTOT += toMinutes(album.totD)

        return len(conn), durataTOT

    def getGraphSize(self):
        return len(self._graph.nodes), len(self._graph.edges)


# FUORI DALLA CLASSE PERCHE' NON E' UNA FUNZIONE DEL MODELLO
def toMillisec(d):
    return d*60*1000

def toMinutes(d):
    return d/60/1000
