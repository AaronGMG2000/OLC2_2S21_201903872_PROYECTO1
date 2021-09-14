
from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO
from ..GENERAL.error import Error

class BREAK(Instruccion):

    def __init__(self, fila, columna):
        super().__init__(CICLICO.BREAK, fila, columna)

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        if len(arbol.PilaCiclo):
            return True
        return Error("Sintactico","La funcion BREAK unicamente se puede usar en ciclos", self.fila, self.columna)


        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('FOR')
        return nodo