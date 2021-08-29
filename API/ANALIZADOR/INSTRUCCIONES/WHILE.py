from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class WHILE(Instruccion):

    def __init__(self, expresion, instruciones,fila, columna):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.expresion = expresion
        self.instruciones = instruciones

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        condicion = self.expresion.Ejecutar(arbol, tabla)
        if isinstance(condicion, Error): return condicion
        arbol.PilaCiclo.append("WHILE")
        if self.expresion.tipo == Tipos.BOOL:
            while condicion:
                nuevo_entorno = Tabla_Simbolo(tabla, "WHILE")
                for inst in self.instruciones:
                    res = inst.Ejecutar(arbol, nuevo_entorno)
                    if isinstance(res, Error): 
                        arbol.errores.append(res)
                condicion = self.expresion.Ejecutar(arbol, tabla)
            return True    
        else:
            return Error("Sintactico", "Se esperaba un valor booleano en la expresion del while", self.fila, self.columna)
                    
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('WHILE')
        nodo.agregarHijo("while")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        nodoInst = NodoAST('INSTRUCIONES')
        for ins in self.instruciones:
            nodoInst.agregarHijoNodo(ins.getNodo())
        nodo.agregarHijo("end")
        nodo.agregarHijo(";")
        return nodo