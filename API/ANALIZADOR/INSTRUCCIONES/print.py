from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class Imprimir(Instruccion):

    def __init__(self, expresion: List, fila, columna):
        super().__init__(Tipos.STRING, fila, columna)
        self.expresion = expresion

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        valor = ''
        tamaño = 1
        for ex in self.expresion:
            val = ex.Ejecutar(arbol, tabla)
            if isinstance(val, Error): return val
            if tamaño == len(self.expresion):
                valor += str(val)
            else:
                valor += str(val) + ' '
            
            tamaño+=1

        arbol.updateConsola(valor)
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        nodo.agregarHijo('PRINT')
        nodo.agregarHijo('(')
        a = 1
        for ex in self.expresion:
            nodo.agregarHijoNodo(ex.getNodo())
            if a != len(self.expresion):
                nodo.agregarHijo(',')
            a+=1
        nodo.agregarHijo(')')
        return nodo