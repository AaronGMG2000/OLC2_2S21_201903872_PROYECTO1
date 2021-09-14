from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos, Aritmeticos
from ..GENERAL.error import Error
from ..DICCIONARIO.Diccionario import D_Aritmetica
import math
class Aritmetica(Instruccion):

    def __init__(self, operador: Aritmeticos, fila, columna, op1, op2=None):
        super().__init__(Tipos.ENTERO, fila, columna)
        self.operador = operador
        self.op1 = op1
        self.op2 = op2 
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        izq = None
        der = None
        operando = None
        if self.op2 is not None:
            izq = self.op1.Ejecutar(arbol, tabla)
            if isinstance(izq, Error): return izq
            der = self.op2.Ejecutar(arbol, tabla)
            if isinstance(der, Error): return der
            try:
                tipo = D_Aritmetica[self.op1.tipo.value+self.operador.value+self.op2.tipo.value]
                self.tipo = tipo[0]
                operando = tipo[1]
            except:
                return Error("Semantico", "No se puede operar los tipos "+self.op1.tipo.value+" y "+self.op2.tipo.value+
                             " con el operando "+self.operador.value, self.fila, self.columna)
            if operando.value == "^":
                res = math.pow(izq, der)
                if self.tipo == Tipos.ENTERO:
                    return int(res)
                else:
                    return res
            return eval(f'izq {operando.value} der')
        else:
            izq = self.op1.Ejecutar(arbol, tabla)
            if isinstance(izq, Error): return izq
            try:
                tipo = D_Aritmetica[self.operador.value+self.op1.tipo.value]
                self.tipo = tipo[0]
                operando = tipo[1]
            except:
                return Error("Semantico", "No se puede operar el tipo "+self.op1.tipo.value+
                             " con la operación de negativo", self.fila, self.columna)
            return eval(f'{operando.value} izq')

    def getNodo(self) -> NodoAST:
        nodo = NodoAST("ARITMETICA")
        if  self.op2 is None:
            nodo.agregarHijo(self.operador.value)
            nodo.agregarHijoNodo(self.op1.getNodo())
        else:
            nodo.agregarHijoNodo(self.op1.getNodo())
            nodo.agregarHijo(self.operador.value)
            nodo.agregarHijoNodo(self.op2.getNodo())
        return nodo
