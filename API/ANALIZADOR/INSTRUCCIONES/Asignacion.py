from ..GENERAL.Lista_Simbolo import Lista_Simbolo
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class Asignacion(Instruccion):

    def __init__(self, tipo, fila, columna, expresion, id):
        super().__init__(tipo, fila, columna)
        self.expresion = expresion
        self.id = id

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        variable = tabla.getVariable(self.id)
        content = self.expresion.Ejecutar(arbol, tabla)
        if isinstance(content, Error): return content
        if self.tipo is not None and self.tipo != self.expresion.tipo:
            return Error("Semantico", "Se esperaba un tipo "+self.tipo.value+" para poder asignar a la variable", self.fila, self.columna)

        if variable is None:
            arbol.Lista_Simbolo.Agregar(Lista_Simbolo(self.id, "VARIABLE", tabla.Entorno, self.fila, self.columna))
            nuevoSimbolo = Simbolo(content, self.expresion.tipo, self.id, self.fila, self.columna)
            tabla.setVariable(nuevoSimbolo)
            return content
        else:
            variable.setValor(content)
            variable.setTipo(self.expresion.tipo)
            return content


    def getNodo(self) -> NodoAST:
        nodo = NodoAST('ASIGNACION')
        nodo.agregarHijo(self.id)
        nodo.agregarHijo('=')
        nodo.agregarHijoNodo(self.expresion.getNodo())
        if self.tipo is not None:
            nodo.agregarHijo('::')
            nodo.agregarHijo(self.tipo.value)
        return nodo
