from .Tabla_Simbolo import tablaSimbolos


class Arbol(object):

    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.consola = ""
        self.tabla_global = tablaSimbolos()
        self.errores = []
        self.listaTablas = []

    def ejecutar(self):
        for m in self.getInstrucciones():
            m.Ejecutar(self, self.getGlobal())
            
    def getInstrucciones(self):
        return self.instrucciones

    def getConsola(self):
        return self.consola

    def updateConsola(self, update):
        self.consola = f"{self.consola}{update}"

    def getGlobal(self):
        return self.tabla_global
    