from enum import Enum


class Tipos(Enum):
    ENTERO = 'INT64'
    FLOAT = 'FLOAT64'
    BOOL = 'BOOL'
    CHAR = 'CHAR'
    STRING = 'STRING'
    ARRAY = 'ARREGLO'
    STRUCT = 'STRUCT'
    NULO = 'NULO'

class Aritmeticos(Enum):
    SUMA = '+'
    RESTA = '-'
    MULTIPLICACION = '*'
    DIVISION = '/'
    MENOSUNARIO = '-'
    POTENCIA = '^'
    MODULO = '%'

class Relacionales(Enum):
    MAYOR = '>'
    MENOR = '<'
    MAYORIGUAL = '>='
    MENORIGUAL = '<='
    IGUAL = '=='
    DISTINTO = '!='

class Logicas(Enum):
    OR = '||'
    AND = '&&'
    NOT = '!'

class TipoNativa(Enum):
    PARSE = 'PARSE'
    TRUNC = 'TRUNC'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    TYPEOF = 'TYPEOF'
    UPPERCASE = 'UPPERCASE'
    LOWERCASE = 'LOWERCASE'
    LOG10 = 'LOG10'
    LOG = 'LOG' 
    SIN = 'SIN' 
    COS = 'COS'
    TAN = 'TAN'
    SQRT = 'SQRT'
