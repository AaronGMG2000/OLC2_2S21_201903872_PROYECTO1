from ..GENERAL.Tipo import Tipos
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Arbol import Arbol
from .NodoAST import NodoAST
from abc import ABC, abstractmethod


class Instruccion(ABC):

    def __init__(self, tipo, fila, columna):
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        super().__init__()

    @abstractmethod
    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        pass

    @abstractmethod
    def getNodo(self) -> NodoAST:
        pass
