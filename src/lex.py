import ply.lex as lex
from utils import Result,print_errors,print_tokens

cargos_estados_1 = {
  '"Marketing"' : 'VALOR_CARGO',
  '"Developer"' : 'VALOR_CARGO',
  '"Devops"' : 'VALOR_CARGO',
  '"Canceled"' : 'VALOR_ESTADO',
  '"Done"' : 'VALOR_ESTADO'
}
cargos_estados_2 = {
  '"Product Analyst"' : 'VALOR_CARGO',
  '"Project Manager"' : 'VALOR_CARGO',
  '"UX designer"' : 'VALOR_CARGO',
  '"DB admin"' : 'VALOR_CARGO',
  '"To do"' : 'VALOR_ESTADO',
  '"In progress"' : 'VALOR_ESTADO',
  '"On hold"' : 'VALOR_ESTADO'
}

reserved = {
  '"empresas"' : 'CLAVE_EMPRESAS',
  '"version"' : 'CLAVE_VERSION',
  '"firma_digital"' : 'CLAVE_FIRMA_DIGITAL',
  '"nombre_empresa"' : 'CLAVE_NOMBRE_EMPRESA',
  '"fundacion"' : 'CLAVE_FUNDACION',
  '"direccion"' : 'CLAVE_DIRECCION',
  '"calle"' : 'CLAVE_CALLE',
  '"ciudad"' : 'CLAVE_CIUDAD',
  '"pais"' : 'CLAVE_PAIS',
  '"ingresos_anuales"' : 'CLAVE_INGRESOS_ANUALES',
  '"pyme"' : 'CLAVE_PYME',
  '"link"' : 'CLAVE_LINK',
  '"departamentos"' : 'CLAVE_DEPARTAMENTOS',
  '"nombre"' : 'CLAVE_NOMBRE',
  '"jefe"' : 'CLAVE_JEFE',
  '"subdepartamentos"' : 'CLAVE_SUBDEPARTAMENTOS',
  '"empleados"' : 'CLAVE_EMPLEADOS',
  '"edad"' : 'CLAVE_EDAD',
  '"cargo"' : 'CLAVE_CARGO',
  '"salario"' : 'CLAVE_SALARIO',
  '"activo"' : 'CLAVE_ACTIVO',
  '"fecha_contratacion"' : 'CLAVE_FECHA_CONTRATACION',
  '"proyectos"' : 'CLAVE_PROYECTOS',
  '"estado"' : 'CLAVE_ESTADO',
  '"fecha_inicio"' : 'CLAVE_FECHA_INICIO',
  '"fecha_fin"' : 'CLAVE_FECHA_FIN',
}

tokens = [
  'APERTURA_OBJETO',
  'CLAUSURA_OBJETO',
  'APERTURA_LISTA',
  'CLAUSURA_LISTA',
  'DOS_PUNTOS',
  'COMA',
  'VALOR_NULL',
  'VALOR_BOOL',
  'VALOR_STRING',
  'VALOR_FECHA',
  'VALOR_URL',
  'VALOR_ENTERO',
  'VALOR_REAL',
  'VALOR_CARGO',
  'VALOR_ESTADO'
] + list(reserved.values())

t_APERTURA_OBJETO = r'\{'
t_CLAUSURA_OBJETO = r'\}'
t_APERTURA_LISTA = r'\['
t_CLAUSURA_LISTA = r'\]'
t_DOS_PUNTOS = r'\:'
t_COMA = r'\,'
t_VALOR_NULL = r'(null)'
t_VALOR_BOOL = r'(true)|(false)'

def t_VALOR_REAL(t):
  r'(\-?(\d+[\.\,]\d+)|\-?(\d+[\.\,]\d+))'
  
  if (t.lexer.result.check_float(t.value,t.lineno,t.lexpos)):
    return t

def t_VALOR_ENTERO(t):
  r'\-?\d+'
  
  if (t.lexer.result.check_integer(t.value,t.lineno,t.lexpos)):
    return t

def t_VALOR_FECHA(t):
  r'\"\d+\-\d+\-\d+\"'
  
  if (t.lexer.result.check_date(t.value,t.lineno,t.lexpos)):
    return t

def t_VALOR_URL(t):
  r'\"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)\"'
  return t

def t_CLAVE(t):
  r'\"\w+\"'
   # Check for reserved words or cargo or estado
  t.type = (reserved | cargos_estados_1).get(t.value,'VALOR_STRING')
  return t

def t_VALOR_STRING(t):
  r'(\"([^\"])*\")|(\'([^\'])*\')'
  
  if (t.lexer.result.check_string(t.value,t.lineno,t.lexpos)):
    t.type = cargos_estados_2.get(t.value,'VALOR_STRING') # Check for cargo or estado
    return t

def t_new_line(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  t.lexer.last_pos = t.lexpos

t_ignore  = ' \t'

def t_error(t):
  t.lexer.result.add_result(t.value[0],t.lineno,t.lexpos,t.lexer.last_pos)
  t.lexer.skip(1)

def t_eof(t):
  t.lexer.lineno = 1
  t.lexer.last_pos = 0
lexer = lex.lex()
lexer.result = Result('')
lexer.last_pos = 0

def lexer_module(data):
  lexer.result = Result(data)
  lexer.input(data)
  
  while True:
    tok = lexer.token()
    if not tok:
      break # No more input
    
    lexer.result.add_result(tok.value,tok.lineno,tok.lexpos,lexer.last_pos,tok.type)
    
  return lexer.result.results()

if __name__ == '__main__':
  print('Lexer de json interactivo')
  while True:
    try:
      string_input = input('(escribe "fin" para terminar)>>> ')
    except KeyboardInterrupt:
      break
    if (string_input.lower() == 'fin'):
      break
    else:
      print()
      tokens,no_tokens,numbers,dates,strings,is_empty = lexer_module(string_input).values()
      
      if (is_empty):
        print('Error: imput vacio', end='\n\n')
      else:
        if (len(no_tokens) > 0):
          print_tokens(no_tokens,True)
        if (len(numbers) > 0):
          print_errors('Numbers','los siguientes numeros',numbers)
        if (len(dates) > 0):
          print_errors('Dates','las siguientes fechas',dates)
        if (len(strings) > 0):
          print_errors('Strings','los siguientes strings',strings)
        if (len(tokens) > 0):
          print_tokens(tokens)
