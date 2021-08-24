from ..GENERAL.Tipo import Tipos
from ..GENERAL.Tabla_Simbolo import tablaSimbolos
from ..GENERAL.Arbol import Arbol
from .NodoAST import NodoAST
from abc import ABC, abstractmethod


class Instruccion(ABC):

    def __init__(self, tipo, linea, columna):
        self.tipo = tipo
        self.linea = linea
        self.columna = columna
        super().__init__()

    @abstractmethod
    def Ejecutar(self, arbol: Arbol, tabla: tablaSimbolos):
        pass

    @abstractmethod
    def getNodo(self) -> NodoAST:
        pass
