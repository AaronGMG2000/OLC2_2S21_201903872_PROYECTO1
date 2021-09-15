import re
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class Variable(Instruccion):

    def __init__(self, id, fila, columna, id2=None, posiciones = None):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.id = id
        self.id2= id2
        self.posiciones = posiciones

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        if self.id2 == None:
            variable = tabla.getVariable(self.id)
            if variable is not None:
                self.tipo = variable.getTipo()
                if self.tipo == Tipos.ARRAY:
                    if self.posiciones is not None:
                        try:
                            val = self.getArray(variable.getValor(), arbol, tabla)
                            if isinstance(val, Error): return val
                            if isinstance(val, Simbolo):
                                self.tipo = val.getTipo()
                                return val.getValor()
                            else:
                                self.tipo = Tipos.ARRAY
                                return val
                        except:
                            return Error("Sintactico","Posicion de Array fuera de rango", self.fila, self.columna)
                    else:
                        return variable.getValor()
                elif self.posiciones is not None:
                    return Error("Sintactico","La variable indicada no es un array", self.fila, self.columna)
                else:
                    return variable.getValor()
            else:
                return Error("Semantico", "La variable indicada no existe", self.fila, self.columna)
        else:       
            variable = self.id.Ejecutar(arbol, tabla)
            if isinstance(variable, Error):return variable
            self.tipo = self.id.tipo
            if self.tipo!=Tipos.OBJECT:
                return Error("Semantico","La variable indicada no corresponde a un objeto struct", self.fila, self.columna)
            try:
                get = variable[self.id2]
                self.tipo = get[1]
                if self.posiciones == None:
                    return get[0]
                else:
                    ress = self.getArray(get[0], arbol, tabla)
                    if isinstance(ress, Error): return ress
                    if isinstance(ress, Simbolo):
                        self.tipo = ress.getTipo()
                        return ress.getValor()
                    else:
                        self.tipo = Tipos.ARRAY
                        return ress
            except:
                return Error("Sintactico","La propiedad "+self.id2+" No existe en el struct indicado", self.fila, self.columna)
    
    def getArray(self, array, arbol, tabla):
        data = array
        for posicion in self.posiciones:
            res = posicion.Ejecutar(arbol, tabla)
            if isinstance(res, Error):return res
            if posicion.tipo != Tipos.ENTERO and posicion.tipo!= Tipos.RANGE:
                return Error("Sintactico","La posición del array debe ser un Int64 o un rango", self.fila, self.columna)
            if posicion.tipo == Tipos.ENTERO:
                res-=1
                if res < 0:
                    return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)
                data = data[res]
            if posicion.tipo == Tipos.RANGE:
                data = self.clonarSimbolos(data, res[0], res[1])
                if isinstance(data, Error): return data
        return data
        
    def clonarSimbolos(self, array, izquierda, derecha):
        array2 = None
        if izquierda != None and derecha!=None:
            izquierda -=1
            derecha -=1
            if izquierda <0 or derecha<0:
                return Error("Sintactico", "Valor fuera de rango del array", self.fila, self.columna)
            array2 = array[izquierda:derecha+1]
        else:
            array2 = array[:]
        newarray = []
        for sim in array2:
            if isinstance(sim, Simbolo):
                newarray.append(Simbolo(sim.valor, sim.tipo, "", sim.fila, sim.columna))
            else:
                newarray.append(sim)
        return newarray
              
            
    
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('VARIABLE')
        id = NodoAST("ID")
        if self.id2 == None:
            id.agregarHijo(self.id)
            nodo.agregarHijoNodo(id)
        else:
            nodo.agregarHijoNodo(self.id.getNodo())
            id2 = NodoAST("ID")
            nodo.agregarHijo(".")
            id2.agregarHijo(self.id2)
            nodo.agregarHijoNodo(id2)
            if self.posiciones is not None:
                anterior_pos = None
                nodo_posicion = None
                for pos in self.posiciones:
                    nodo_posicion = NodoAST("LISTA_ARRAY")
                    if anterior_pos is not None:
                        nodo_posicion.agregarHijoNodo(anterior_pos)
                    nodo_posicion.agregarHijo("[")
                    nodo_posicion.agregarHijoNodo(pos.getNodo())
                    nodo_posicion.agregarHijo("]")
                    anterior_pos = nodo_posicion
                nodo.agregarHijoNodo(nodo_posicion)
        return nodo