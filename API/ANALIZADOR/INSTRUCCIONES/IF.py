from ..INSTRUCCIONES.BREAK import BREAK
from ..INSTRUCCIONES.CONTINUE import CONTINUE
from ..INSTRUCCIONES.RETURN import RETURN
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error

class IF(Instruccion):

    def __init__(self, expresionIf, instrucionesIf,fila, columna, elseif=None):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.ExpresionIf = expresionIf
        self.InstrucionesIf = instrucionesIf
        self.elseif = elseif

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        
        if self.elseif is not None:
                res = self.elseif.Ejecutar(arbol, tabla)
                if isinstance(res, Error): return res
                if res is not False:
                    return res
                
        condicion = self.ExpresionIf.Ejecutar(arbol, tabla)
        if isinstance(condicion, Error): return condicion        
        if self.ExpresionIf.tipo == Tipos.BOOL:
            if condicion:
                for ins in self.InstrucionesIf:
                    res = ins.Ejecutar(arbol, tabla)
                    if isinstance(res, Error):
                        arbol.errores.append(res)
                    elif isinstance(res, RETURN):                   
                        return res
                    elif isinstance(res, CONTINUE):
                        return res
                    elif isinstance(res, BREAK):
                        return res
                return True
            return False
        else:
            return Error("Semantico","La condición de la función if debe ser un booleano",self.fila, self.columna)
    
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('IF')
        if self.elseif is None:
            nodo.agregarHijo("if")
        else:
            nodo.agregarHijoNodo(self.elseif.getNodo())
            nodo.agregarHijo("elseif")
        nodo.agregarHijoNodo(self.ExpresionIf.getNodo())
        
        nodoInst = NodoAST('INSTRUCIONES')
        for ins in self.InstrucionesIf:
            inst = NodoAST("INSTRUCION")
            inst.agregarHijoNodo(ins.getNodo())
            nodoInst.agregarHijoNodo(inst)
        nodo.agregarHijoNodo(nodoInst)
        return nodo
        