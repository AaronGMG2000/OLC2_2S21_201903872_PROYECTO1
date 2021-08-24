from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import tablaSimbolos
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class ImprimirEnter(Instruccion):

    def __init__(self, expresion: List, linea, columna):
        super().__init__(Tipos.STRING, linea, columna)
        self.expresion = expresion

    def Ejecutar(self, arbol: Arbol, tabla: tablaSimbolos):
        valor = ''
        tamaño = 1
        for ex in self.expresion:
            if tamaño == len(self.expresion):
                valor += str(ex.Ejecutar(arbol, tabla))
            else:
                valor += str(ex.Ejecutar(arbol, tabla)) + ' '
            
            tamaño+=1

            if isinstance(ex, Error):
                return valor
        arbol.updateConsola(valor+'\n')

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINTLN')
        nodo.agregarHijo('println')
        nodo.agregarHijo('(')
        a = 1
        for ex in self.expresion:
            nodo.agregarHijoNodo(ex.getNodo())
            if a != len(self.expresion):
                nodo.agregarHijo(',')
            a+=1
        nodo.agregarHijo(')')
        return nodo