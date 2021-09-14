
from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error

class PUSH(Instruccion):

    def __init__(self, array, expresion, fila, columna):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.expresion = expresion
        self.array = array

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        arr = self.array.Ejecutar(arbol, tabla)
        if isinstance(arr, Error):return arr
        if self.array.tipo == Tipos.ARRAY:
            value = self.expresion.Ejecutar(arbol, tabla)
            if isinstance(arr, Error):return value
            if self.expresion.tipo == Tipos.ARRAY:
                arr.append(value)
            else:
                arr.append(Simbolo(value, self.expresion.tipo, "", self.fila, self.columna))            
        else:
            return Error("Sintactico","Solo se puede ejecutar push en una lista", self.fila, self.columna)
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('FOR')
        return nodo