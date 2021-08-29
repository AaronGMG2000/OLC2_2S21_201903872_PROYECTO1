from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos


class Primitivo(Instruccion):

    def __init__(self, tipo:Tipos, valor, fila, columna):
        super().__init__(tipo, fila, columna)
        self.valor = valor

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRIMITIVO')
        nodo.agregarHijo(str(self.valor))
        return nodo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        return self.valor

