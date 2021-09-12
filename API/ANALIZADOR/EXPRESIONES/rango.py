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
        if self.valor1.tipo!=Tipos.FLOAT and self.valor1.tipo!=Tipos.ENTERO:
            return Error("Sintactico","El rango unicamente puede tener valores numericos",self.fila, self.columna)
        if self.valor2.tipo!=Tipos.FLOAT and self.valor2.tipo!=Tipos.ENTERO:
            return Error("Sintactico","El rango unicamente puede tener valores numericos",self.fila, self.columna)
        
        if v1 > v2:
            return Error("Sintactico", "El primer valor del rango debe ser mayor al 2do", self.fila, self.columna)
        self.tipo = Tipos.RANGE
        return [v1, v2]