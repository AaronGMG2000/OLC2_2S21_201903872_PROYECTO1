from .Simbolo import Simbolo


class tablaSimbolos(object):

    def __init__(self, anterior=None):
        self.anterior = anterior
        self.tabla = {}
        self.Entorno = ""

    def setVariable(self, simbolo: Simbolo):
        entorno = self
        while entorno is not None:
            
            try:
                variable = entorno.getTable()[simbolo.getID()]
            except Exception:
                variable = None

            if variable is not None:
                return None
            else:
                entorno = entorno.getAnterior()

        self.tabla[simbolo.getID()] = simbolo

    def getVariable(self, ID):
        entorno = self
        while entorno is not None:
            
            try:
                variable = entorno.getTable()[ID]
            except Exception:
                variable = None

            if variable is not None:
                return variable
            else:
                entorno = entorno.getAnterior()
        return None

    def getTable(self):
        return self.tabla

    def getAnterior(self):
        return self.anterior
