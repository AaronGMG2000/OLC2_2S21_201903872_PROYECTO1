from ..INSTRUCCIONES.BREAK import BREAK
from ..INSTRUCCIONES.CONTINUE import CONTINUE
from os import R_OK
from ..INSTRUCCIONES.RETURN import RETURN
from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Lista_Simbolo import Lista_Simbolo
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error

class LLAMADA_EXP(Instruccion):

    def __init__(self, id, parametros,fila, columna):
        super().__init__(Tipos.STRUCT, fila, columna)
        self.id = id
        self.parametros = parametros
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        variable = tabla.getVariable(self.id)
        if variable is None:
            return Error("Sintactico","La función o struct indicado no existe", self.fila, self.columna)
        else:
            if variable.getTipo() == Tipos.STRUCT:
                a = 0
                dic = dict(variable.getValor())
                diccionario = variable.getValor()
                t_p = len(self.parametros)
                t_v =len(list(dic.keys()))-2
                if  t_v != t_p:
                    return Error("Sintactico","Class Struct necesita "+str(t_v)+" parametros y esta recibiendo "+str(t_p)+" parametros", self.fila, self.columna)
                for key in list(dic.keys()):
                    if key == 1 or key == 2:
                        continue
                    valor = self.parametros[a].Ejecutar(arbol, tabla)
                    if isinstance(valor, Error): return valor
                    if dic[key][2] is not None and dic[key][2]!= self.parametros[a].tipo:
                        return Error("Sintactico","El parametro '"+key+"' del struct es tipo "+dic[key][2].value+" y se recibio un tipo "+self.parametros[a].tipo.value, self.fila, self.columna)
                    dic[key] = diccionario[key][:]
                    dic[key][0] = valor
                    dic[key][1] = self.parametros[a].tipo
                    a = a+1
                self.tipo = Tipos.OBJECT
                return dic
            elif variable.getTipo() == Tipos.FUNCTION:
                contenido = variable.getValor()
                x = 0
                if len(self.parametros)!=len(contenido[0]):
                    return Error("Sintactico","La función requiere "+str(len(contenido[0]))+"Parametros y esta recibiendo "+str(len(self.parametros), self.fila, self.columna) )
                nuevoEntorno = Tabla_Simbolo(tabla, self.id)
                nuevoEntorno.funcion = True
                for par in contenido[0]:
                    
                    variable2 = self.parametros[x].Ejecutar(arbol, tabla)
                    if par[1] != Tipos.NOTHING:
                        if self.parametros[x].tipo!= par[1]:
                            return Error("Semantico", "Tipo de variable de función invalido", self.fila, self.columna)
                    newData = Simbolo(variable2, self.parametros[x].tipo, par[0], self.fila, self.columna)
                    nuevoEntorno.tabla[par[0]] = newData
                    arbol.Lista_Simbolo.Agregar(Lista_Simbolo(par[0], newData.getTipo(), nuevoEntorno.Entorno, self.fila, self.columna))
                    x+=1
                    
                arbol.PilaFunc.append(self.id)
                for inst in contenido[1]:
                    res = inst.Ejecutar(arbol, nuevoEntorno)
                    if isinstance(res, Error):
                        arbol.errores.append(res)
                    if isinstance(res, RETURN):
                        arbol.PilaFunc.pop()
                        self.tipo = res.tipoA
                        return res.valor
                    elif isinstance(res, BREAK):
                        return Error("Sintactico","No se puede usar BREAK en una función", self.fila, self.columna)
                    elif isinstance(res, CONTINUE):
                        return Error("Sintactico","No se puede usar CONTINUE en una función", self.fila, self.columna)
                        
                arbol.PilaFunc.pop()
                self.tipo = Tipos.NOTHING
                return "nothing"
            else:
                return Error("Sintactico","la variable indicada no corresponde a un struct o una función", self.fila, self.columna)

        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST("LLAMADA")
        nodo.agregarHijo(self.id)
        nodo.agregarHijo("(")
        para = None
        anterior = None
        if len(self.parametros):
            for par in self.parametros:
                para = NodoAST("PARAMETROS")
                if anterior is not None:
                    para.agregarHijoNodo(anterior)
                para.agregarHijoNodo(par.getNodo())
                anterior = para
            nodo.agregarHijoNodo(para)
        nodo.agregarHijo(")")
        nodo.agregarHijo(";")
        return nodo
    
    