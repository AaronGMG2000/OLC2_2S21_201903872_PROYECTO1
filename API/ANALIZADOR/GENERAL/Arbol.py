from .error import Error
from .Tabla_Simbolo import Tabla_Simbolo
from .Lista_Simbolos import List_Simbolo
from ..ABSTRACT.NodoAST import NodoAST
import re
import os
class Arbol(object):

    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.consola = ""
        self.tabla_global = Tabla_Simbolo(None,"GLOBAL")
        self.errores = []
        self.Lista_Simbolo = List_Simbolo()
        self.raiz = NodoAST("INSTRUCCIONES")
        self.grafo = ""
        self.PilaCiclo = []
        self.PilaFunc = []
        self.c = 0
    def ejecutar(self):
        for inst in self.getInstrucciones():
            res = inst.Ejecutar(self, self.getGlobal())
            if isinstance(res, Error):
                self.errores.append(res)
            self.raiz.agregarHijoNodo(inst.getNodo())
        self.graphAST()
            
    def getInstrucciones(self):
        return self.instrucciones

    def getConsola(self):
        return self.consola

    def updateConsola(self, update):
        self.consola = f"{self.consola}{update}"

    def getGlobal(self):
        return self.tabla_global
    
    
    def graphAST(self):
        r = "AST"
        ext = "svg"
        stream = open(f'./reportes/{r}.dot','w');
        stream.write(self.getDot(self.raiz))
        stream.close()
        os.system(f'dot -T svg -o ./reportes/{r}.{ext} ./reportes/{r}.dot')
        os.system(f'start ./reportes/{r}.{ext}')
        
    def getDot(self, raiz):
    
        self.grafo = ""
        self.grafo += "digraph {\n"
        res = r'\"';
        self.grafo += "n0[label=\"" +  re.sub(res, '\\\"', raiz.getValor()) + "\"];\n";
        self.c = 1;
        self.recorrerAST("n0",raiz);
        self.grafo += "}";
        return self.grafo;
    
    
    def recorrerAST(self,padre , nPadre):
        for hijo in nPadre.getHijos():
            nombreHijo = "n" + str(self.c);
            res = r'\"'; 
            self.grafo += nombreHijo + "[label=\"" + re.sub(res, '\\\"', hijo.getValor())+ "\"];\n";
            self.grafo += padre + "->" + nombreHijo + ";\n";
            self.c+=1
            self.recorrerAST(nombreHijo,hijo);
        
    