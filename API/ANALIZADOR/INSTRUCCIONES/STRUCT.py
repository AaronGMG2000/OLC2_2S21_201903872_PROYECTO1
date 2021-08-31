from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Lista_Simbolo import Lista_Simbolo
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class STRUCT(Instruccion):

    def __init__(self, id, parametros,fila, columna, mutable=False):
        super().__init__(Tipos.STRUCT, fila, columna)
        self.id = id
        self.parametros = parametros
        self.mutable = mutable
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        variable = tabla.getVariable(self.id)
        content = {}
        if variable is None:
            for par in self.parametros:
                content[par[0]] = [None, None, par[1]]
            arbol.Lista_Simbolo.Agregar(Lista_Simbolo(self.id, "STRUCT", tabla.Entorno, self.fila, self.columna))
            nuevoSimbolo = Simbolo(content, self.tipo, self.id, self.fila, self.columna, None, self.mutable)
            tabla.setVariable(nuevoSimbolo)
            return content
        else:
            return Error("Sintactico","No se puede crear un Struct con ese nombre debido que ya hay una variable asignada", self.fila, self.columna)
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST("STRUCT")
        return nodo
    
    