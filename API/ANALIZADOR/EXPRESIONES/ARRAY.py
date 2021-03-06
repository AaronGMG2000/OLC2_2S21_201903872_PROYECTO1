from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class ARRAY(Instruccion):

    def __init__(self, expresion, fila, columna):
        super().__init__(Tipos.ARRAY, fila, columna)
        self.expresion = expresion

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        valor = []
        for exp in self.expresion:
            res = exp.Ejecutar(arbol, tabla)
            if isinstance(res, Error): return res
            if exp.tipo == Tipos.ARRAY:
                valor.append(res)
            else:
                valor.append(Simbolo(res, exp.tipo, "", self.fila, self.columna))
        return valor
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('ARRAY')
        lista = None
        anterior = None
        nodo.agregarHijo("[")
        for exp in self.expresion:
            lista = NodoAST('LISTA_ARRAY')
            if anterior is not None:
                lista.agregarHijoNodo(anterior)
                lista.agregarHijo(",")
            lista.agregarHijoNodo(exp.getNodo())
            anterior = lista
        nodo.agregarHijoNodo(lista)
        nodo.agregarHijo("]")
        return nodo