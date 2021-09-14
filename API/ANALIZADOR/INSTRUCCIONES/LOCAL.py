
from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error

class LOCAL(Instruccion):

    def __init__(self, id, fila, columna, expresion = None, tipo = None):
        super().__init__(CICLICO.BREAK, fila, columna)
        self.id = id
        self.expresion = expresion
        self.tipoA = tipo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        try:
            variable = tabla.tabla.get[self.id]
            return Error("Sintactico","Ya existe una variable local con esta id", self.fila, self.columna)
        except:
            valor = "nothing"
            self.tipo = Tipos.NOTHING
            if self.expresion is not None:
                valor = self.expresion.Ejecutar(arbol, tabla)
                self.tipo = self.expresion.tipo
                if isinstance(valor, Error): return valor
                if self.tipoA is not None:
                    if self.expresion.valor != self.tipoA:
                        return Error("Sintactico","Los tipos de la asignacion local no coinciden", self.fila, self.columna)
            tabla.setVariable(Simbolo(valor, self.tipo, self.id, self.fila, self.columna))
            return
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('FOR')
        return nodo