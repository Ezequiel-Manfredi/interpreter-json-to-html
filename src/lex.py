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
  r'(\-?\d+[\.\,]\d+)'
  
  errors = []
  p = None
  
  if ('-' in t.value):
    errors.append('el numero debe ser real positivo o cero')
  if (',' in t.value):
    errors.append('el separador decimal debe ser . (un punto)')
    p = t.value.split(',')
  else:
    p = t.value.split('.')
  if (not (len(p[1]) == 2)):
    errors.append('los decimales del numero deben ser 2')
  if (not errors):
    return t
  
  t.lexer.numbers.append({
    'value': t.value,
    'type': t.type,
    'lineno': t.lineno,
    'lexpos': t.lexpos,
    'errors': errors
  })

def t_VALOR_ENTERO(t):
  r'\-?\d+'
  
  errors = []
  if ('-' in t.value):
    errors.append('el numero debe ser entero positivo o cero')
  else:
    return t
  
  t.lexer.numbers.append({
    'value': t.value,
    'type': t.type,
    'lineno': t.lineno,
    'lexpos': t.lexpos,
    'errors': errors
  })

def t_VALOR_FECHA(t):
  r'\"\d+\-\d+\-\d+\"'
  
  errors = []
  p = t.value[1:-1].split('-') # Avoid " and separate the pieces by -
  
  if (not len(p[0]) == 4):
    errors.append('el año debe tener 4 digitos')
  if (not len(p[1]) == 2):
    errors.append('el mes debe tener 2 digitos')
  if (not len(p[2]) == 2):
    errors.append('el dia debe tener 2 digitos')
  if (not (1900 <= int(p[0]) and int(p[0]) <= 2099)):
    errors.append('el año debe estar entre 1900 y 2099')
  if (not (1 <= int(p[1]) and int(p[1]) <= 12)):
    errors.append('el mes debe estar entre 1 y 12')
  if (not (1 <= int(p[2]) and int(p[2]) <= 31)):
    errors.append('el dia debe estar entre 1 y 31')
  if (not errors):
    return t
  
  t.lexer.dates.append({
    'value': t.value,
    'type': t.type,
    'lineno': t.lineno,
    'lexpos': t.lexpos,
    'errors': errors
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
  r'(\".*\")|(\'.*\')'
  
  errors = []
  if ("'" in t.value):
    errors.append('los strings deben estar entre " (comillas dobles)')
  else:
    t.type = cargos_estados_2.get(t.value,'VALOR_STRING') # Check for cargo or estado
    return t
  
  t.lexer.strings.append({
    'value': t.value,
    'type': t.type,
    'lineno': t.lineno,
    'lexpos': t.lexpos,
    'errors': errors
  })

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
  lexer.numbers = []
  lexer.dates = []
  lexer.strings = []
  lexer.errors = []
  lexer.empty = not bool(len(data))
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
    'numbers': lexer.numbers,
    'dates': lexer.dates,
    'strings': lexer.strings,
    'empty': lexer.empty
  }

if __name__ == '__main__':
  print('Lexer de json interactivo')
  while True:
    string_input = input('>>> ')
    print()
    tokens,errors,numbers,dates,strings,empty = lexer_module(string_input).values()
    if (empty):
      print('Error: imput vacio', end='\n\n')
    if (len(errors) > 0):
      print('Lexer Error (No_Tokens): los siguientes caracteres no se reconocen')
      for error in errors:
        print(f'  ◢ {error.get('value')} ►  error: caracter inlegal')
      print()
    if (len(numbers) > 0):
      print('Lexer Error (Numbers): los siguientes numeros no cumplen las condiciones')
      for number in numbers:
        print(f'  ◢ {number.get('value')}')
        for error in number.get('errors'):
          print(f'    ► error: {error}')
      print()
    if (len(dates) > 0):
      print('Lexer Error (Dates): las siguientes fechas no cumplen las condiciones')
      for date in dates:
        print(f'  ◢ {date.get('value')}')
        for error in date.get('errors'):
          print(f'    ► error: {error}')
      print()
    if (len(strings) > 0):
      print('Lexer Error (Strings): los siguientes strings no cumplen las condiciones')
      for string in strings:
        print(f'  ◢ {string.get('value')}')
        for error in string.get('errors'):
          print(f'    ► error: {error}')
      print()
    if (len(tokens) > 0):
      print('Lexer (Tokens): los siguientes tokens fueron encontrados')
      for token in tokens :
        print(f"  ◢ {token.get('value')} ►  tipo: {token.get('type')}")
      print()
