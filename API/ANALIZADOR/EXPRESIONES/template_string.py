from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class Template(Instruccion):

    def __init__(self, expresion: List, texto, fila, columna):
        super().__init__(Tipos.STRING, fila, columna)
        self.expresion = expresion
        self.texto = texto

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        valor = self.texto
        for ex in self.expresion:
            val = ex.Ejecutar(arbol, tabla)
            if isinstance(val, Error): return val
            valor += str(val)

        return valor
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRIMITIVO')
        nodo.agregarHijo(str(self.texto))
        return nodo