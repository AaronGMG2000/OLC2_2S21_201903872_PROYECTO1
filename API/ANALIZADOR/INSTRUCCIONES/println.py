from ..GENERAL.Simbolo import Simbolo
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class ImprimirEnter(Instruccion):

    def __init__(self, expresion: List, fila, columna):
        super().__init__(Tipos.STRING, fila, columna)
        self.expresion = expresion

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        valor = ''
        tamaño = 1
        for ex in self.expresion:
            val = ex.Ejecutar(arbol, tabla)
            if isinstance(val, Error): return val
            if ex.tipo == Tipos.OBJECT:
                val = self.getStruct("", val)
            elif ex.tipo == Tipos.STRUCT:
                val = val[1]
            elif ex.tipo == Tipos.FUNCTION:
                val = val[2]
            elif ex.tipo == Tipos.ARRAY :
                val = self.getArrayValue(val, "")
            elif ex.tipo == Tipos.BOOL:
                val = str(val).lower()
            if tamaño == len(self.expresion):
                valor += str(val)
            else:
                valor += str(val) + ' '
            
            tamaño+=1

        arbol.updateConsola(valor+'\n')

    def getStruct(self, val, struct):
        val += struct[1] + "("
        lista = list(struct.keys())
        for key in lista:
            if key == 1 or key == 2:
                continue
            if key != lista[2]:
                val +=","
            valor = struct[key]
            if valor[1] == Tipos.OBJECT:
                val = self.getStruct(val, valor[0])
            elif valor[1] == Tipos.ARRAY:
                val = str(self.getArrayValue(valor[0], val))
            elif valor[1] == Tipos.STRING:
                val +='"'+valor[0]+'"'
            elif valor[1] == Tipos.CHAR:
                val +='"'+valor[0]+'"'
            elif valor[1] == Tipos.BOOL:
                val += str(valor[0]).lower()
            elif valor[1] == Tipos.FUNCTION:
                val = valor[2]
            else:
                val += str(valor[0])
        val += ")"
        return val
    
    def getArrayValue(self, simb, val):
        val += '['
        for sim in simb:
            if sim != simb[0]:
                val+=","
            if not isinstance(sim, Simbolo):
                val = self.getArrayValue(sim, val)
            else:
                valor = sim.getValor()
                if sim.getTipo() == Tipos.OBJECT:
                    val = self.getStruct(val, valor)
                else:
                    if sim.getTipo() == Tipos.STRING:
                        val +='"'+valor+'"'
                    elif sim.getTipo() == Tipos.CHAR:
                        val +="'"+valor+"'"
                    elif sim.getTipo() == Tipos.FUNCTION:
                        val = valor[2]
                    elif sim.getTipo() == Tipos.BOOL:
                        val += str(valor).lower()
                    else:
                        val+=str(valor)
        val += ']'
        return val
    
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINTLN')
        nodo.agregarHijo('println')
        nodo.agregarHijo('(')
        a = 1
        for ex in self.expresion:
            nodo.agregarHijoNodo(ex.getNodo())
            if a != len(self.expresion):
                nodo.agregarHijo(',')
            a+=1
        nodo.agregarHijo(')')
        return nodo