class Error(object):

    def __init__(self, tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna

    def toString(self):
        return self.tipo + " - " + self.descripcion + " [" + self.fila + ", " + self.columna + "]\n"

    def getTipo(self):
        return self.tipo

    def getDesc(self):
        return self.descripcion

    def getFila(self):
        return  self.fila

    def getColumna(self):
        return self.columna