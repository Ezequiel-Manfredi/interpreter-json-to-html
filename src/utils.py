class Result:
  def __init__(self, len_input):
    self.tokens = []
    self.no_tokens = []
    self.numbers = []
    self.dates = []
    self.strings = []
    self.is_empty = not bool(len_input)
  
  def results(self):
    return {
      'tokens': self.tokens,
      'no_tokens': self.no_tokens,
      'numbers': self.numbers,
      'dates': self.dates,
      'strings': self.strings,
      'is_empty': self.is_empty
    }
  
  def add_result(self,value,line,pos,type = 'NO_TOKEN',is_error = False,errors = None):
    result = {
      'value': value,
      'type': type,
      'line': line,
      'pos': pos
    }
    
    if (not is_error):
      if (type == 'NO_TOKEN'):
        self.no_tokens.append(result)
      else:
        self.tokens.append(result)
    else:
      result['errors'] = errors
      if (type == 'VALOR_ENTERO' or type == 'VALOR_REAL'):
        self.numbers.append(result)
      elif (type == 'VALOR_FECHA'):
        self.dates.append(result)
      elif (type == 'VALOR_STRING'):
        self.strings.append(result)
      else:
        print('Error: tipo no reconocido')
  
  def check_float(self,value,line,pos):
    errors = []
    p = None
    
    if ('-' in value):
      errors.append('el numero debe ser real positivo o cero')
    if (',' in value):
      errors.append('el separador decimal debe ser . (un punto)')
      p = value.split(',')
    else:
      p = value.split('.')
    if (not (len(p[0]) >= 1)):
      errors.append('la parte entera del numero debe ser de al menos 1 digito')
    if (not (len(p[1]) == 2)):
      errors.append('la parte decimal del numero debe ser de 2 digitos')
    if (not errors):
      return True
    
    self.add_result(value,line,pos,'VALOR_REAL',True,errors)
    return False
  
  def check_integer(self,value,line,pos):
    errors = []
    if ('-' in value):
      errors.append('el numero debe ser entero positivo o cero')
    else:
      return True
    
    self.add_result(value,line,pos,'VALOR_ENTERO',True,errors)
    return False
  
  def check_date(self,value,line,pos):
    errors = []
    p = value[1:-1].split('-') # Avoid " and separate the pieces by -

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
      return True
    
    self.add_result(value,line,pos,'VALOR_FECHA',True,errors)
    return False
  
  def check_string(self,value,line,pos):
    errors = []
    if ("'" in value):
      errors.append('los strings deben estar entre " (comillas dobles)')
    else:
      return True
    
    self.add_result(value,line,pos,'VALOR_STRING',True,errors)
    return False

def print_errors(type,msj,data):
  print(f'Lexer Error ({type}): {msj} no cumplen las condiciones')
  for ele in data:
    print(f'  ◢ {ele.get('value')}')
    for error in ele.get('errors'):
      print(f'    ► error: {error}')
  print()

def print_tokens(data,is_not = False):
  if (is_not):
    print('Lexer Error (No_Tokens): los siguientes caracteres no se reconocen')
  else:
    print('Lexer (Tokens): los siguientes tokens fueron encontrados')
  for ele in data:
    print(f'  ◢ {ele.get('value')} ►  ',end='')
    if (is_not):
      print('error: caracter ilegal')
    else:
      print(f'tipo: {ele.get('type')}')
  print()

SYNTAX_ERROR_MESSAGES = {
  'OBJETO' : {
    'APERTURA': 'Se esperaba { (apertura de objeto)',
    'CLAUSURA': 'Se esperaba } (clausura de objeto)',
    'COMA_EXTRA': 'El ultimo elemento del objeto no debe llevar , (coma)'
  },
  'LISTA': {
    'APERTURA': 'Se esperaba [ (apertura de lista)',
    'CLAUSURA': 'Se esperaba ] (clausura de lista)',
    'COMA_EXTRA': 'El ultimo elemento de la lista no debe llevar , (coma)',
    'VACIO': 'La lista esta vacia, proporcione un elemento'
  },
  'OBLIGATORIO' : {
    'EMPRESAS': 'El elemento "empresas" es obligatorio',
  },
  'VALOR_INVALIDO' : 'Valor invalido para el campo',
  'DOS_PUNTOS' : 'Se esperaba : (dos puntos) para separa la clave del valor',
  'COMA' : 'Se esperaba , (coma) para separa los elementos',
  'EOF' : 'Problemas en el final del archivo'
}

class SyntaxErrors:
  def __init__(self):
    self.errors = []
  
  def get_errors(self):
    return self.errors
  
  def add_error(self,msj,value = None,line = None,pos = None,type = None):
    self.errors.append({
      'value': value,
      'type': type,
      'line': line,
      'pos': pos,
      'msj': msj
    })

def tabs(level):
  tabs = ''
  for i in range(level):
    tabs += '\t'
  return tabs