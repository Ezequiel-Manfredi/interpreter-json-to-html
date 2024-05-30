import ply.lex as lex

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
  'NO_TOKEN',
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
  'VALOR_REAL'
] + list(reserved.values())

t_APERTURA_OBJETO = r'\{'
t_CLAUSURA_OBJETO = r'\}'
t_APERTURA_LISTA = r'\['
t_CLAUSURA_LISTA = r'\]'
t_DOS_PUNTOS = r'\:'
t_COMA = r'\,'
t_VALOR_NULL = r'(null)'
t_VALOR_BOOL = r'(true)|(false)'
t_VALOR_STRING = r'\"(\w+\s*)*\"'
t_VALOR_FECHA = r'\"\d{4}\-\d{1,2}\-\d{1,2}\"'
t_VALOR_URL = r'\"((https?\:\/\/)?(www\.)?\w+\.\w+(\:\d+)?(\/.*)?)\"'

def t_VALOR_REAL(t):
  r'(\d+\.\d+)'
  t.value = float(t.value)
  return t

def t_VALOR_ENTERO(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_CLAVE(t):
    r'(\"\w+\")'
    t.type = reserved.get(t.value,'VALOR_STRING') # Check for reserved words
    return t

def t_new_line(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  
t_ignore  = ' \t'

def t_error(t):
  t.lexer.skip(1)
  t.type = "NO_TOKEN"
  return t
  
lexer = lex.lex()

def lexer_module(data):
  lexer.input(data)
  tokens_response = []
  is_no_token = False
  no_token = {
    'type': 'NO_TOKEN',
    'value': '',
    'lineno': 0,
    'lexpos': 0
  }
  while True:
    tok = lexer.token()
    if not tok:
      if is_no_token:
        tokens_response.append({
          'type': no_token['type'],
          'value': no_token['value'],
          'lineno': no_token['lineno'],
          'lexpos': no_token['lexpos']
        }) # Add accumulated no_token
      break      # No more input
    if tok.type == 'NO_TOKEN':
      if not is_no_token: # Initialize new no_token
        is_no_token = True
        no_token['lineno'] = tok.lineno
        no_token['lexpos'] = tok.lexpos
      no_token['value'] += tok.value[0] # Accumulate char no_token
    else:
      if is_no_token:
        is_no_token = False
        tokens_response.append({
          'type': no_token['type'],
          'value': no_token['value'],
          'lineno': no_token['lineno'],
          'lexpos': no_token['lexpos']
        }) # Add accumulated no_token
        no_token['value'] = ''
      tokens_response.append({
        'type': tok.type,
        'value': tok.value,
        'lineno': tok.lineno,
        'lexpos': tok.lexpos
      }) # Add new token
  return tokens_response

if __name__ == '__main__':
  print('Lexer de json interactivo')
  while True:
    string_input = input('>>> ')
    print()
    tokens = lexer_module(string_input)
    for token in tokens :
      print(f"{token.get('value')} ➜  ", end="")
      print(f"tipo: {token.get('type')} ,", end="")
      print(f"linea: {token.get('lineno')} ,", end="")
      print(f"posicion: {token.get('lexpos')}")
    print()
