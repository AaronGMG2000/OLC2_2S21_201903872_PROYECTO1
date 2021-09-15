
from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error

class GLOBAL(Instruccion):

    def __init__(self, id, fila, columna, expresion = None, tipo = None):
        super().__init__(CICLICO.BREAK, fila, columna)
        self.id = id
        self.expresion = expresion
        self.tipoA = tipo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        try:
            res = tabla.tabla[self.id]
            return Error("Sintactico","no se puede declarar global a una variable existente", self.fila, self.columna)
        except:
            simbolo = arbol.tabla_global.getVariable(self.id)
            simbolo2 = tabla.getVariable(self.id)
            if simbolo!=None and simbolo2!=None and simbolo!=simbolo2:
                return Error("Sintactico","No se puede declarar una variable global y local al mismo tiempo", self.fila, self.columna)
            valor = None
            self.tipo = Tipos.NOTHING
            if self.expresion!=None:
                valor = self.expresion.Ejecutar(arbol, tabla)
                self.tipo = self.expresion.tipo
                if self.tipoA is not None:
                    if self.expresion.valor != self.tipoA:
                        return Error("Sintactico","Los tipos de la asignacion local no coinciden", self.fila, self.columna)
            if isinstance(valor, Error): return valor
            if simbolo is None:
                simbolo = Simbolo(valor, self.tipo, self.id, self.fila, self.columna)
                tabla.setVariable(simbolo)
                aux = tabla.anterior
                while aux.anterior!=None:
                    aux.setVariable(simbolo)
                    aux = aux.anterior
            else:
                if self.expresion is not None:
                    simbolo.setValor(valor)
                    simbolo.setTipo(self.tipo)
                while tabla.anterior!=None:
                    tabla.setVariable(simbolo)
                    tabla = tabla.anterior
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('GLOBAL')
        nodo.agregarHijo("global")
        nodo.agregarHijo(self.id)
        if self.expresion is not None:
            nodo.agregarHijo("=")
            nodo.agregarHijoNodo(self.expresion.getNodo())
            if self.tipo is not None:
                nodo.agregarHijo("::")
                if self.tipo.value == Tipos.OBJECT:
                    nodo.agregarHijo(Tipos.STRUCT.value)
                else:
                    nodo.agregarHijo(self.tipo.value)
        nodo.agregarHijo(";")
        return nodo