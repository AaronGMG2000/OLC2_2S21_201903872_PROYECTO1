from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import tablaSimbolos
from ..GENERAL.Tipo import Tipos


class Primitivo(Instruccion):

    def __init__(self, tipo:Tipos, valor, linea, columna):
        super().__init__(tipo, linea, columna)
        self.valor = valor

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRIMITIVO')
        nodo.agregarHijo(str(self.valor))
        return nodo

    def Ejecutar(self, arbol: Arbol, tabla: tablaSimbolos):
        return self.valor

