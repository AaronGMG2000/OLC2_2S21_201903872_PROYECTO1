from .Tipo import Tipos


class Simbolo(object):
    def __init__(self, valor, tipo: Tipos, id, fila, columna, rango=None):
        self.tipo = tipo
        self.id = id
        self.fila = fila
        self.columna = columna
        self.valor = valor
        self.tipado_rango = rango
        
    def getID(self):
        return self.id

    def getTipo(self):
        return self.tipo

    def getTipoRango(self):
        return self.tipado_rango
    
    def setTipoRango(self, tipo:Tipos):
        self.tipado_rango = tipo

    def setTipo(self, tipo: Tipos):
        self.tipo = tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor