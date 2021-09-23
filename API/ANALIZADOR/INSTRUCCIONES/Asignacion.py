from ..GENERAL.Lista_Simbolo import Lista_Simbolo
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tabla_Simbolo import Tabla_Simbolo
from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error

class Asignacion(Instruccion):

    def __init__(self, tipo, fila, columna, expresion, id, id2=None, Posicion=None):
        super().__init__(tipo, fila, columna)
        self.expresion = expresion
        self.id = id
        self.id2 = id2
        self.Posiciones = Posicion
        self.ultimo = Tipos.ENTERO

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        variable = tabla.getVariable(self.id, tabla.funcion)
        content = self.expresion.Ejecutar(arbol, tabla)
        if self.id2==None:
            if isinstance(content, Error): return content
            if self.tipo is not None and self.tipo != self.expresion.tipo:
                return Error("Semantico", "Se esperaba un tipo "+self.tipo.value+" para poder asignar a la variable", self.fila, self.columna)
            if variable is None:
                if self.Posiciones is not None:
                    return Error("Sintactico","La variable indicada no existe", self.fila, self.columna)
                arbol.Lista_Simbolo.Agregar(Lista_Simbolo(self.id, self.expresion.tipo.value, tabla.Entorno, self.fila, self.columna))
                nuevoSimbolo = Simbolo(content, self.expresion.tipo, self.id, self.fila, self.columna)
                tabla.setVariable(nuevoSimbolo)
                return content
            else:
                if self.Posiciones is not None:
                    if variable.getTipo()!=Tipos.ARRAY:
                        return Error("Sintactico", "La variable indicada no es un array", self.fila, self.columna)
                    arr = variable.getValor()
                    arr = self.cambioArray(self.Posiciones, arr, arbol, tabla, len(self.Posiciones), 0, content)
                    if isinstance(arr, Error): return arr
                    self.tipo = self.expresion.tipo
                    if self.ultimo == Tipos.RANGE:
                        variable.setValor(arr)
                    return content                                        
                                        
                if variable.getTipo() == Tipos.STRUCT:
                    return Error("Sintactico","No se puede modificar un tipo Struct", self.fila, self.columna)
                if variable.getTipo() == Tipos.FUNCTION:
                    return Error("Sintactico","No se puede modificar un tipo FUNCTION", self.fila, self.columna)
                arbol.Lista_Simbolo.Agregar(Lista_Simbolo(self.id, self.expresion.tipo.value, tabla.Entorno, self.fila, self.columna))
                variable.setValor(content)
                variable.setTipo(self.expresion.tipo)
                return content
        else:
            id2 = None
            if isinstance(content, Error): return content
            if variable is None:
                return Error("Semantico", "La variable indicada no existe", self.fila, self.columna)
            
            if self.Posiciones is not None:
                if variable.getTipo()!=Tipos.ARRAY:
                    return Error("Sintactico", "La variable indicada no es un array", self.fila, self.columna)
                ar = self.getArrayNode(self.Posiciones, arbol, tabla)
                if isinstance(ar, Error): return ar
                try:
                    get = variable.getValor()
                    va = eval(f'get{ar}')
                    if isinstance(va, Simbolo):
                        variable = va
                    else: 
                        return Error("Sintactico","La variable indicada no es un Struct", self.fila, self.columna)
                except:
                    return Error("Sintactico", "Posición fuera de rango", self.fila, self.columna)
                    
            if variable.getTipo() == Tipos.OBJECT:
                try:
                    newDic = None
                    get = variable.getValor()
                    a = 1
                        
                    for id2 in self.id2:
                        if a < len(self.id2):
                            newDic = get
                            get = get[id2[0]][0]
                        else:
                            newDic = get
                            get = get[id2[0]]
                        if id2[1] is not None:
                            if a < len(self.id2):
                                ar = self.getArrayNode(id2[1], arbol, tabla)
                                if isinstance(ar, Error): return ar
                                try:
                                    va = eval(f'get{ar}')
                                    if isinstance(va, Simbolo):
                                        get = va.getValor()
                                        newDic = get
                                    else: 
                                        get = va
                                        newDic = get
                                except:
                                    return Error("Sintactico", "Posición fuera de rango", self.fila, self.columna)
                            else:
                                try:
                                    ar = self.getArrayNode(id2[1], arbol, tabla)
                                    va = eval(f'get[0]{ar}')
                                    if isinstance(va, Simbolo):
                                        if self.expresion.tipo == Tipos.ARRAY:
                                            arr = self.cambioArray(id2[1], get[0], arbol, tabla, len(id2[1]), 0, content)
                                            if isinstance(arr, Error): return arr
                                            get[0] = arr
                                        else:
                                            va.setValor(content)
                                        va.setTipo(self.expresion.tipo) 
                                        get = [va, va.getTipo(), get[2]]
                                    else:
                                        arr = self.cambioArray(id2[1], get[0], arbol, tabla, len(id2[1]), 0, content)
                                        if isinstance(arr, Error): return arr
                                        get[0] = arr
                                        
                                        self.tipo = self.expresion.tipo
                                        get[1] = self.expresion.tipo
                                        return content
                                except:
                                    return Error("Sintactico", "Posición fuera de rango", self.fila, self.columna)
                        a+=1
                    if get[2]!=None and get[2] != self.expresion.tipo:
                        return Error("Semantico", "Se esperaba un tipo "+self.tipo.value+" para poder asignar al parametro "+id2[0], self.fila, self.columna)
                    self.tipo = self.expresion.tipo
                    if not newDic[2]:
                        return Error("Semantico","el objeto struct no es mutable", self.fila, self.columna)
                    get[1] = self.expresion.tipo
                    get[0] = content
                    return content
                except:
                    return Error("Semantico","El parametro "+id2[0]+" no existe en el struct indicado", self.fila, self.columna)
            else:
                return Error("Semantico","La variable indicada no es un struct", self.fila, self.columna)

    
    def getArrayNode(self, list, arbol, tabla):
        ar = ''
        for posicion in list:
            ar +="["
            res = posicion.Ejecutar(arbol, tabla)
            if isinstance(res, Error):return res
            if posicion.tipo != Tipos.ENTERO and posicion.tipo!= Tipos.RANGE:
                return Error("Sintactico","La posición del array debe ser un Int64 o un rango", self.fila, self.columna)
            if posicion.tipo == Tipos.ENTERO:
                res-=1
                if res < 0:
                    return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)
            ar += str(res)
            ar +="]"
        return ar
    
    def cambioArray(self, list, array, arbol, tabla, max, pos, nuevo):
        if pos < max-1:
            posicion = list[pos]
            res = posicion.Ejecutar(arbol, tabla)
            if isinstance(res, Error): return res
            if posicion.tipo != Tipos.ENTERO and posicion.tipo!= Tipos.RANGE:
                return Error("Sintactico","La posición del array debe ser un Int64 o un rango", self.fila, self.columna)
            if posicion.tipo == Tipos.ENTERO:
                res-=1
                if res < 0:
                    return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)
                array[res] = self.cambioArray(list, array[res], arbol, tabla, max, pos+1, nuevo)
            elif posicion.tipo == Tipos.RANGE:
                if res[0] == None and res[1] == None:
                    array = self.cambioArray(list, array[:], arbol, tabla, max, pos+1, nuevo)
                else:
                    try:
                        izquierda = res[0]-1
                        derecha = res[1]-1
                        if izquierda<0 and derecha<0:
                            return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)
                        array = self.cambioArray(list, array[izquierda:derecha+1], arbol, tabla, max, pos+1, nuevo)
                    except:
                        return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)

            return array
        else:
            posicion = list[pos]
            res = posicion.Ejecutar(arbol, tabla)
            if isinstance(res, Error): return res
            if posicion.tipo != Tipos.ENTERO and posicion.tipo!= Tipos.RANGE:
                return Error("Sintactico","La posición del array debe ser un Int64 o un rango", self.fila, self.columna)
            if posicion.tipo == Tipos.ENTERO:
                self.ultimo = Tipos.ENTERO
                n=res-1
                if n < 0:
                    return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)
                if self.expresion.tipo == Tipos.ARRAY:
                    array[n] = nuevo
                else:
                    if isinstance(array[n], Simbolo):
                        array[n].setValor(nuevo)
                        array[n].setTipo(self.expresion.tipo)
                    else:
                        array[n] = Simbolo(nuevo, self.expresion.tipo, "", self.fila, self.columna)
                return  array
            else:
                self.ultimo = Tipos.RANGE
                izquierda = 0
                derecha = 0
                if res[0] == None and res[1] == None:
                    array = array[:]
                else:
                    try:
                        izquierda = res[0]-1
                        derecha = res[1]-1
                        if izquierda<0 and derecha<0:
                            return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)
                    except:
                        return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)

                if self.expresion.tipo == Tipos.ARRAY:
                    return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)
                else:
                    for ar in range(izquierda,derecha+1):
                        if isinstance(array[ar], Simbolo):
                            array[ar].setValor(nuevo)
                            array[ar].setTipo(self.expresion.tipo)
                        else:
                            array[ar] = Simbolo(nuevo, self.expresion.tipo, "", self.fila, self.columna)
                return  array
    
    
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('ASIGNACION')
        id = NodoAST("ID")
        id.agregarHijo(self.id)
        if self.Posiciones is not None:
            anterior_pos = None
            nodo_posicion = None
            for posicion in self.Posiciones:
                nodo_posicion = NodoAST("LISTA_ARRAY")
                if anterior_pos is not None:
                    nodo_posicion.agregarHijoNodo(anterior_pos)
                nodo_posicion.agregarHijo("[")
                nodo_posicion.agregarHijoNodo(posicion.getNodo())
                nodo_posicion.agregarHijo("]")
                anterior_pos = nodo_posicion
            id.agregarHijoNodo(nodo_posicion)
        nodo.agregarHijoNodo(id)
        if self.id2 is not None:
            id = None
            anterior = None
            for id2 in self.id2:
                id = NodoAST("LISTA_ID")
                idd = NodoAST("ID")
                if anterior is not None:
                    id.agregarHijoNodo(anterior)
                
                id.agregarHijo(".")
                idd.agregarHijo(id2[0])
                id.agregarHijoNodo(idd)
                if id2[1] is not None:
                    nodo_arr = None
                    anterior_arr = None
                    for arr in id2[1]:
                        nodo_arr = NodoAST("LISTA_ARRAY")
                        if anterior_arr is not None:
                            nodo_arr.agregarHijoNodo(anterior_arr)
                        nodo_arr.agregarHijo("[")
                        nodo_arr.agregarHijoNodo(arr.getNodo())
                        nodo_arr.agregarHijo("]")
                        anterior_arr = nodo_arr
                    id.agregarHijoNodo(nodo_arr)
                
                anterior = id
            nodo.agregarHijoNodo(id)
        else:
            pass
        nodo.agregarHijo('=')
        nodo.agregarHijoNodo(self.expresion.getNodo())
        if self.tipo is not None:
            nodo.agregarHijo('::')
            nodo.agregarHijo(self.tipo.value)
        return nodo
