from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class CONDICION(Instruccion):

    def __init__(self, funcion_if,fila, columna, instrucionesElse=None):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.funcion_if = funcion_if
        self.InstrucionesElse = instrucionesElse

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        res = self.funcion_if.Ejecutar(arbol, tabla)
        if isinstance(res, Error): return res        
        if res:
            return True
        else:
            if self.InstrucionesElse is not None:
                nuevaTabla = Tabla_Simbolo(tabla, "Else")
                for ins in self.InstrucionesElse:
                    res = ins.Ejecutar(arbol, nuevaTabla)
                    if isinstance(res, Error):
                        arbol.errores.append(res)
            return True
                    
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('IF')
        nodo.agregarHijoNodo(self.funcion_if.getNodo())
        nodo.agregarHijo("Else")
        nodoInst = NodoAST('INSTRUCIONES')
        for ins in self.InstrucionesElse:
            nodoInst.agregarHijoNodo(ins.getNodo())
        nodo.agregarHijoNodo(nodoInst)
        nodo.agregarHijo("end")
        nodo.agregarHijo(";")
        return nodo