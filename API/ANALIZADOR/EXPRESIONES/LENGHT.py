
from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error

class LENGHT(Instruccion):

    def __init__(self, expresion, fila, columna):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.expresion = expresion

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        valor = self.expresion.Ejecutar(arbol, tabla)
        if isinstance(valor, Error):return valor
        if self.expresion.tipo == Tipos.ARRAY:
            self.tipo = Tipos.ENTERO
            return len(valor)
        else:
            return Error("Sintactico","Solo se puede ejecutar push en una lista", self.fila, self.columna)
    
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('LENGTH')
        nodo.agregarHijo("length")
        nodo.agregarHijo("(")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijo(")")
        return nodo