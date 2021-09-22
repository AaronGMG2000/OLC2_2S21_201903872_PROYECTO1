from ..INSTRUCCIONES.RETURN import RETURN
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error

class WHILE(Instruccion):

    def __init__(self, expresion, instruciones,fila, columna):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.expresion = expresion
        self.instruciones = instruciones

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        condicion = self.expresion.Ejecutar(arbol, tabla)
        if isinstance(condicion, Error): 
            arbol.PilaCiclo.pop()
            return condicion
        arbol.PilaCiclo.append("WHILE")
        if self.expresion.tipo == Tipos.BOOL:
            evaluado = False
            while condicion:
                nuevo_entorno = Tabla_Simbolo(tabla, "WHILE")
                for inst in self.instruciones:
                    res = inst.Ejecutar(arbol, nuevo_entorno)
                    if isinstance(res, Error) and evaluado:
                        arbol.errores.append(res)
                    elif isinstance(res, RETURN):
                        arbol.PilaCiclo.pop()                  
                        return res
                    elif inst.tipo == CICLICO.BREAK:
                        arbol.PilaCiclo.pop()
                        return True
                    elif inst.tipo == CICLICO.CONTINUE:
                        break
                evaluado = True
                condicion = self.expresion.Ejecutar(arbol, tabla)
                if isinstance(condicion, Error): return condicion
            arbol.PilaCiclo.pop() 
            return True    
        else:
            arbol.PilaCiclo.pop()
            return Error("Sintactico", "Se esperaba un valor booleano en la expresion del while", self.fila, self.columna)
                    
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('WHILE')
        nodo.agregarHijoNodo(self.expresion.getNodo())
        inst = NodoAST('INSTRUCCIONES')
        for ins in self.instruciones:
            instr = NodoAST("INSTRUCCION")
            instr.agregarHijoNodo(ins.getNodo())
            inst.agregarHijoNodo(instr)
        nodo.agregarHijoNodo(inst)
        return nodo