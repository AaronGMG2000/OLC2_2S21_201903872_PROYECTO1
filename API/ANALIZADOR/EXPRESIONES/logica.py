from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos, Logicas
from ..GENERAL.error import Error
from ..DICCIONARIO.Diccionario import D_LOGICA


class Logica(Instruccion):

    def __init__(self, operador:Logicas, fila, columna, op1, op2=None):
        super().__init__(Tipos.BOOL, fila, columna)
        self.operador = operador
        self.op1 = op1
        self.op2 = op2

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        izq = None
        der = None        
        operando = ''        
        if self.op2 is not None:
            
            izq = self.op1.Ejecutar(arbol, tabla)
            if isinstance(izq, Error): return izq
            if self.operador.value == "&&":
                if not izq: return izq
            if self.operador.value == "||":
                if izq: return izq
            der = self.op2.Ejecutar(arbol, tabla)
            if isinstance(der, Error): return der
            try:
                operando = D_LOGICA[self.op1.tipo.value+self.operador.value+self.op2.tipo.value]
            except:
                return Error("Semantico", "No se puede operar los tipos "+self.op1.tipo.value+" y "+self.op2.tipo.value+
                             " con el operando logico "+operando, self.fila, self.columna)
            return eval(f'izq {operando} der')
        else:
            izq = self.op1.Ejecutar(arbol, tabla)
            if isinstance(izq, Error): return izq
            try:
                operando = D_LOGICA[self.operador.value+self.op1.tipo.value]
            except:
                return Error("Semantico", "No se puede negar el tipo "+self.op1.tipo.value, self.fila, self.columna)

            return eval(f'{operando} izq')

    def getNodo(self) -> NodoAST:
        nodo = NodoAST("LOGICA")
        if not self.op2 is None:
            nodo.agregarHijo(self.operador.value)
            nodo.agregarHijoNodo(self.op1.getNodo())
        else:
            nodo.agregarHijoNodo(self.op1.getNodo())
            nodo.agregarHijo(self.operador.value)
            nodo.agregarHijoNodo(self.op2.getNodo())
        return nodo
