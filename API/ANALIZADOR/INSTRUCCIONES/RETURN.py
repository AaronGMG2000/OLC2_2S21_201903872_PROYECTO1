from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO
from ..GENERAL.error import Error

class RETURN(Instruccion):

    def __init__(self, fila, columna, expresion=True):
        super().__init__(CICLICO.RETURN, fila, columna)
        self.expresion = expresion
        self.valor = None
        self.tipoA = None
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        if len(arbol.PilaFunc):
            valor = self.expresion.Ejecutar(arbol, tabla)
            self.valor = valor
            self.tipoA = self.expresion.tipo
            return self
        return Error("Sintactico","La funcion RETURN unicamente se puede usar en Funciones", self.fila, self.columna)

        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('FOR')
        return nodo