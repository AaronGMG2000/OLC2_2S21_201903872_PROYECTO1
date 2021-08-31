from ..GENERAL.Lista_Simbolo import Lista_Simbolo
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class Asignacion(Instruccion):

    def __init__(self, tipo, fila, columna, expresion, id, id2=None):
        super().__init__(tipo, fila, columna)
        self.expresion = expresion
        self.id = id
        self.id2 = id2

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        variable = tabla.getVariable(self.id)
        content = self.expresion.Ejecutar(arbol, tabla)
        if self.id2==None:
            if isinstance(content, Error): return content
            if self.tipo is not None and self.tipo != self.expresion.tipo:
                return Error("Semantico", "Se esperaba un tipo "+self.tipo.value+" para poder asignar a la variable", self.fila, self.columna)

            if variable is None:
                
                arbol.Lista_Simbolo.Agregar(Lista_Simbolo(self.id, "VARIABLE", tabla.Entorno, self.fila, self.columna))
                nuevoSimbolo = Simbolo(content, self.expresion.tipo, self.id, self.fila, self.columna, None, False)
                if self.expresion.tipo == Tipos.OBJECT:
                    nuevoSimbolo.mutable = self.expresion.mutable
                tabla.setVariable(nuevoSimbolo)
                return content
            else:
                variable.setValor(content)
                variable.setTipo(self.expresion.tipo)
                return content
        else:
            if isinstance(content, Error): return content
            if variable.getTipo() == Tipos.OBJECT:
                if not variable.mutable:
                    return Error("Semantico","el objeto struct no es mutable", self.fila, self.columna)
                try:
                    get = variable.getValor()[self.id2]
                    if get[2]!=None and get[2] != self.expresion.tipo:
                        return Error("Semantico", "Se esperaba un tipo "+self.tipo.value+" para poder asignar al parametro "+self.id2, self.fila, self.columna)
                    get[0] = content
                    return content
                except:
                    return Error("Semantico","El parametro "+self.id2+" no existe en el struct indicado", self.fila, self.columna)
            else:
                return Error("Semantico","La variable indicada no es un struct", self.fila, self.columna)

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('ASIGNACION')
        nodo.agregarHijo(self.id)
        nodo.agregarHijo('=')
        nodo.agregarHijoNodo(self.expresion.getNodo())
        if self.tipo is not None:
            nodo.agregarHijo('::')
            nodo.agregarHijo(self.tipo.value)
        return nodo
