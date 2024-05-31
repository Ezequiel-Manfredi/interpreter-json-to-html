import ply.lex as lex

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
  r'(\d+[\.\,]\d+)'
  
  error = ''
  p = t.value.split(',')
  if (1 < len(p)):
    error = 'el separador decimal debe ser . (un punto)'
  else:
    p = t.value.split('.')
    if (not (len(p[1]) == 2)):
      error = 'los decimales deben ser 2'
    else:
      return t
  
  t.lexer.floats.append({
    'value': t.value,
    'type': t.type,
    'lineno': t.lineno,
    'lexpos': t.lexpos,
    'error': error
  })

def t_VALOR_ENTERO(t):
  r'\d+'
  return t

def t_VALOR_FECHA(t):
  r'\"\d{4}\-\d{1,2}\-\d{1,2}\"'
  
  error = ''
  p = t.value[1:-1].split('-') # Avoid " and separate the pieces by -
  
  if (not (1900 <= int(p[0]) and int(p[0]) <= 2099)):
    error = 'el año debe estar entre 1900 y 2099'
  elif (not (1 <= int(p[1]) and int(p[1]) <= 12)):
    error = 'el mes debe estar entre 1 y 12'
  elif (not (1 <= int(p[2]) and int(p[2]) <= 31)):
    error = 'el dia debe estar entre 1 y 31'
  else:
    return t
  
  t.lexer.dates.append({
    'value': t.value,
    'type': t.type,
    'lineno': t.lineno,
    'lexpos': t.lexpos,
    'error': error
  })

def t_VALOR_URL(t):
  r'\"((https?\:\/\/)?(www\.)?\w+\.\w+(\:\d+)?(\/[\w\#\.\/\_\-]*)?)\"'
  return t

def t_CLAVE(t):
  r'\"\w+\"'
   # Check for reserved words or cargo or estado
  t.type = (reserved | cargos_estados_1).get(t.value,'VALOR_STRING')
  return t

def t_VALOR_STRING(t):
  r'\".*\"'
  t.type = cargos_estados_2.get(t.value,'VALOR_STRING') # Check for cargo or estado
  return t

def t_new_line(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
  t.lexer.errors.append({
    'value': t.value[0],
    'type': 'NO_TOKEN',
    'lineno': t.lineno,
    'lexpos': t.lexpos
  })
  t.lexer.skip(1)

lexer = lex.lex()

def lexer_module(data):
  lexer.floats = []
  lexer.dates = []
  lexer.errors = []
  lexer.emty = not bool(len(data))
  tokens_response = []
  
  lexer.input(data)
  while True:
    tok = lexer.token()
    if not tok:
      break # No more input
    tokens_response.append({
      'value': tok.value,
      'type': tok.type,
      'lineno': tok.lineno,
      'lexpos': tok.lexpos
    }) # Add new token
  return {
    'tokens': tokens_response,
    'errors': lexer.errors,
    'floats': lexer.floats,
    'dates': lexer.dates,
    'emty': lexer.emty
  }

if __name__ == '__main__':
  print('Lexer de json interactivo')
  while True:
    string_input = input('>>> ')
    print()
    tokens,errors,floats,dates,emty = lexer_module(string_input).values()
    if (emty):
      print('Error: imput vacio', end='\n\n')
    if (len(errors) > 0):
      print('Lexer Error (No_Tokens): los siguientes caracteres no se reconocen')
      for error in errors:
        print(f' {error.get('value')} ➜  error: caracter inlegal')
      print()
    if (len(floats) > 0):
      print('Lexer Error (Floats): los siguientes numeros reales no cumplen las condiciones')
      for fl in floats:
        print(f' {fl.get('value')} ➜  error: {fl.get('error')}')
      print()
    if (len(dates) > 0):
      print('Lexer Error (Dates): las siguientes fechas no cumplen las condiciones')
      for date in dates:
        print(f' {date.get('value')} ➜  error: {date.get('error')}')
      print()
    if (len(tokens) > 0):
      print('Lexer (Tokens): los siguientes tokens fueron encontrados')
      for token in tokens :
        print(f" {token.get('value')} ➜  tipo: {token.get('type')}")
      print()
