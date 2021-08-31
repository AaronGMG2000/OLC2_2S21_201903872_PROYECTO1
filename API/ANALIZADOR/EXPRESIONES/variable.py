from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class Variable(Instruccion):

    def __init__(self, id, fila, columna, id2=None):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.id = id
        self.id2= id2

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        variable = tabla.getVariable(self.id)
        if variable is not None and self.id2 == None:
            self.tipo = variable.getTipo()
            return variable.getValor()
        elif variable is not None and self.id2 != None:
            self.tipo = variable.getTipo()
            if self.tipo!=Tipos.OBJECT:
                return Error("Semantico","La variable indicada no corresponde a un objeto struct", self.fila, self.columna)
            try:
                get = variable.getValor()[self.id2]
                self.tipo = get[1]
                return get[0]
            except:
                return Error("Sintactico","La propiedad "+self.id2+" No existe en el struct indicado", self.fila, self.columna)
        else:
            return Error("Semantico", "La variable indicada no existe", self.fila, self.columna)


    def getNodo(self) -> NodoAST:
        nodo = NodoAST('VARIABLE')
        nodo.agregarHijo(self.id)
        return nodo