from .Lista_Simbolo import Lista_Simbolo


class List_Simbolo(object):

    def __init__(self):
        self.Lista = {}

    def Agregar(self, simbolo: Lista_Simbolo):
        try:
            self.Lista[simbolo.nombre +"-"+ simbolo.ambito]
            self.Lista[simbolo.nombre +"-"+ simbolo.ambito] = simbolo
        except:
            simbolo.numero = len(self.Lista)+1
            self.Lista[simbolo.nombre +"-"+ simbolo.ambito] = simbolo
        return
    
    def getLista(self):
        return list(self.Lista.values())