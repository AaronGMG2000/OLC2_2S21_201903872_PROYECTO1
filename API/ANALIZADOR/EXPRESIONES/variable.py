from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class Variable(Instruccion):

    def __init__(self, id, fila, columna):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.id = id


    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        variable = tabla.getVariable(self.id)
        if variable is not None:
            self.tipo = variable.getTipo()
            return variable.getValor()
        else:
            return Error("Semantico", "La variable indicada no existe", self.fila, self.columna)


    def getNodo(self) -> NodoAST:
        nodo = NodoAST('VARIABLE')
        nodo.agregarHijo(self.id)
        return nodo