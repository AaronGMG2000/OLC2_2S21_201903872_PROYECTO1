import re
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos, Tipos_Nativa
from ..GENERAL.error import Error
from ..DICCIONARIO.Diccionario import D_NATIVA
import math

class Nativas(Instruccion):

    def __init__(self, fila, columna, expresion, Nativa, valor2=None):
        super().__init__(Tipos.ENTERO, fila, columna)
        self.expresion = expresion
        self.Nativa = Nativa
        self.valor2 = valor2

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        inst = None
        if self.Nativa == Tipos_Nativa.LOG:
            valor = self.expresion.Ejecutar(arbol, tabla)
            if isinstance(valor, Error): return valor
            valor2 = self.valor2.Ejecutar(arbol, tabla)
            if isinstance(valor2, Error): return valor2
            
            try:
                inst = D_NATIVA[self.Nativa.value+"-"+self.expresion.tipo.value+"-"+self.valor2.tipo.value]
            except:
                return Error('Semantico', 'La funcion log() requiere valores numericos', self.fila, self.columna)
        elif self.valor2 is not None:
            valor = self.valor2.Ejecutar(arbol, tabla)
            if isinstance(valor, Error): return valor
            try:
                inst = D_NATIVA[self.Nativa.value+"-"+self.expresion.value+"-"+self.valor2.tipo.value]
            except:
                if self.Nativa == Tipos_Nativa.PARSE:
                    return Error('Semantico', 'No se puede convertir ' + valor + ' a Float64', self.fila, self.columna)
                if self.Nativa == Tipos_Nativa.TRUNC:
                    return Error('Semantico', 'No es posible realizar trunc de ' + valor, self.fila, self.columna)
        else:
            valor = self.expresion.Ejecutar(arbol, tabla)
            if isinstance(valor, Error): return valor
            try:
                inst = D_NATIVA[self.Nativa.value+"-"+self.expresion.tipo.value]
            except:
                if self.Nativa == Tipos_Nativa.UPPERCASE:
                    return Error('Semantico', 'La función uppercase unicamente acepta String', self.fila, self.columna)
                elif self.Nativa == Tipos_Nativa.LOWERCASE:
                    return Error('Semantico', 'La función lowercase unicamente acepta String', self.fila, self.columna)
                elif self.Nativa == Tipos_Nativa.STRING:
                    return Error('Semantico', 'No es posible convertir '+valor+" a string", self.fila, self.columna)
                else:
                    return Error('Semantico', 'La función '+self.Nativa.value.lower()+" requiere valores numericos", self.fila, self.columna)
        try:
            if self.Nativa == Tipos_Nativa.STRING and type(valor) == type([]):
                valor = valor[:]
                for x in range(0,len(valor)):
                    valor[x] = valor[x].getValor()
                self.tipo = inst[1]
                return valor
                
            self.tipo = inst[1]
            return eval(inst[0])
        except:
            return Error('Semantico', 'Error en la función '+self.Nativa.value.lower(), self.fila, self.columna)
                
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('NATIVA')
        if self.Nativa == Tipos_Nativa.LOG:
            nodo.agregarHijo(self.Nativa.value)
            nodo.agregarHijo('(')
            nodo.agregarHijoNodo(self.expresion.getNodo())
            nodo.agregarHijo(',')
            nodo.agregarHijoNodo(self.valor2.getNodo())
            nodo.agregarHijo(')')
        elif self.valor2 is not None:
            nodo.agregarHijo(self.Nativa.value)
            nodo.agregarHijo('(')
            nodo.agregarHijo(self.expresion.value)
            nodo.agregarHijo(',')
            nodo.agregarHijoNodo(self.valor2.getNodo())
            nodo.agregarHijo(')')
        else:
            nodo.agregarHijo(self.Nativa.value)
            nodo.agregarHijo('(')
            nodo.agregarHijoNodo(self.expresion.getNodo())
            nodo.agregarHijo(')')
        return nodo