import ply.lex as lex

reserved = {
  '"empresas"' : 'KEY_EMPRESAS',
  '"version"' : 'KEY_VERSION',
  '"firma_digital"' : 'KEY_FIRMA_DIGITAL',
  '"nombre_empresa"' : 'KEY_NOMBRE_EMPRESA',
  '"fundacion"' : 'KEY_FUNDACION',
  '"direccion"' : 'KEY_DIRECCION',
  '"calle"' : 'KEY_CALLE',
  '"ciudad"' : 'KEY_CIUDAD',
  '"pais"' : 'KEY_PAIS',
  '"ingresos_anuales"' : 'KEY_INGRESOS_ANUALES',
  '"pyme"' : 'KEY_PYME',
  '"link"' : 'KEY_LINK',
  '"departamentos"' : 'KEY_DEPARTAMENTOS',
  '"nombre"' : 'KEY_NOMBRE',
  '"jefe"' : 'KEY_JEFE',
  '"subdepartamentos"' : 'KEY_SUBDEPARTAMENTOS',
  '"empleados"' : 'KEY_EMPLEADOS',
  '"edad"' : 'KEY_EDAD',
  '"cargo"' : 'KEY_CARGO',
  '"salario"' : 'KEY_SALARIO',
  '"activo"' : 'KEY_ACTIVO',
  '"fecha_contratacion"' : 'KEY_FECHA_CONTRATACION',
  '"proyectos"' : 'KEY_PROYECTOS',
  '"estado"' : 'KEY_ESTADO',
  '"fecha_inicio"' : 'KEY_FECHA_INICIO',
  '"fecha_fin"' : 'KEY_FECHA_FIN',
}

tokens = [
  'NO_TOKEN',
  'OPEN_OBJECT',
  'CLOSE_OBJECT',
  'OPEN_LIST',
  'CLOSE_LIST',
  'COLON',
  'COMMA',
  'VALUE_NULL',
  'VALUE_BOOL',
  'VALUE_STRING',
  'VALUE_DATE',
  'VALUE_URL',
  'VALUE_INTEGER',
  'VALUE_FLOAT'
] + list(reserved.values())

t_OPEN_OBJECT = r'\{'
t_CLOSE_OBJECT = r'\}'
t_OPEN_LIST = r'\['
t_CLOSE_LIST = r'\]'
t_COLON = r'\:'
t_COMMA = r'\,'
t_VALUE_NULL = r'(null)'
t_VALUE_BOOL = r'(true)|(false)'
t_VALUE_STRING = r'\"(\w+\s*)*\"'
t_VALUE_DATE = r'\"\d{1,2}\/\d{1,2}\/\d{4}\"'
t_VALUE_URL = r'\"((https?\:\/\/)?(www\.)?\w+\.\w+(\:\d+)?(\/.*)?)\"'

def t_VALUE_FLOAT(t):
  r'(\d+\.\d+)'
  t.value = float(t.value)
  return t

def t_VALUE_INTEGER(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_KEY(t):
    r'(\"\w+\")'
    t.type = reserved.get(t.value,'VALUE_STRING') # Check for reserved words
    return t

def t_new_line(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  
t_ignore  = ' \t\r'

def t_error(t):
  t.lexer.skip(len(t.value))
  t.type = "NO_TOKEN"
  return t
  
lexer = lex.lex()

def lexer_module(data):
  lexer.input(data)
  tokens_response = []
  while True:
    tok = lexer.token()
    if not tok: 
      break      # No more input
    tokens_response.append({
      'type': tok.type,
      'value': tok.value,
      'lineno': tok.lineno,
      'lexpos': tok.lexpos
    })
  return tokens_response