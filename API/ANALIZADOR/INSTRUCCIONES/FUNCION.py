from ..GENERAL.Lista_Simbolo import Lista_Simbolo
import re
from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error

class FUNCION(Instruccion):

    def __init__(self, id, instruciones,fila, columna, parametros=[]):
        super().__init__(Tipos.FUNCTION, fila, columna)
        self.id = id
        self.parametros = parametros
        self.instruciones = instruciones

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        variable = tabla.getVariable(self.id)
        if variable == None:
            nombre = self.id+"("
            para = False
            for par in self.parametros:
                nombre+=par[0]+","
                para = True
            if para:
                nombre = nombre[0:len(nombre)-1]
            nombre+=")"
            arbol.Lista_Simbolo.Agregar(Lista_Simbolo(self.id, nombre, tabla.Entorno, self.fila, self.columna))
            tabla.setVariable(Simbolo([self.parametros, self.instruciones, self.id], Tipos.FUNCTION, self.id, self.fila, self.columna))
        else:
            return Error("Sintactico","La función indicada ya existe", self.fila, self.columna)
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('FOR')
        
        return nodo