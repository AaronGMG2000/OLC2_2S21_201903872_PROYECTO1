from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos, Relacionales
from ..GENERAL.error import Error
from ..DICCIONARIO.Diccionario import D_Relacional

class Relacional(Instruccion):

    def __init__(self, operador: Relacionales, fila, columna, op1, op2):
        super().__init__(Tipos.BOOL, fila, columna)
        self.operador = operador
        self.op1 = op1
        self.op2 = op2

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        izq = self.op1.Ejecutar(arbol, tabla)
        if isinstance(izq, Error): return izq

        der = self.op2.Ejecutar(arbol, tabla)
        if isinstance(der, Error): return der
        try:
            self.tipo = D_Relacional[self.op1.tipo.value+self.operador.value+self.op2.tipo.value]
        except:
            return Error("Semantico", "No se puede operar los tipos "+self.op1.tipo.value+" y "+self.op2.tipo.value+
                            " con el operando relacional "+self.operando.value, self.fila, self.columna)
        return eval(f'izq {self.operador.value} der')

    def getNodo(self) -> NodoAST:
        nodo = NodoAST("RELACIONAL")
        nodo.agregarHijoNodo(self.op1.getNodo())
        nodo.agregarHijo(self.operador.value)
        nodo.agregarHijoNodo(self.op2.getNodo())
        return nodo

    

