from .Tipo import Tipos


class Simbolo(object):
    def __init__(self, valor, tipo: Tipos, id, linea, columna):
        self.tipo = tipo
        self.id = id
        self.linea = linea
        self.columna = columna
        self.valor = valor

    def getID(self):
        return self.id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo: Tipos):
        self.tipo = tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor