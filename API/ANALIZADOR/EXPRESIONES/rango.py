from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error


class Rango(Instruccion):

    def __init__(self, tipo:Tipos, valor1, valor2, fila, columna, rango):
        super().__init__(tipo, fila, columna)
        self.valor1 = valor1
        self.valor2 = valor2

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRIMITIVO')
        nodo.agregarHijo(str(self.valor))
        return nodo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        v1 = self.valor1.Ejecutar(arbol, tabla)
        if isinstance(v1, Error): return v1
        v2 = self.valor2.Ejecutar(arbol, tabla)
        if isinstance(v2, Error): return v2
        if v1 > v2:
            return("Sintactico", "El primer valor del rango debe ser mayor al 2do", self.fila, self.columna)
        return [v1, v2]