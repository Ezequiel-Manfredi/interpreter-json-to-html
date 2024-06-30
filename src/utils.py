import os
import sys

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
  
  def add_result(self,value,line,pos,last_pos,type = 'NO_TOKEN',is_error = False,errors = None):
    result = {
      'value': value,
      'type': type,
      'line': line,
      'pos': (pos - last_pos) + 1
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
    
    self.add_result(value,line,pos,0,'VALOR_REAL',True,errors)
    return False
  
  def check_integer(self,value,line,pos):
    errors = []
    if ('-' in value):
      errors.append('el numero debe ser entero positivo o cero')
    else:
      return True
    
    self.add_result(value,line,pos,0,'VALOR_ENTERO',True,errors)
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
    
    self.add_result(value,line,pos,0,'VALOR_FECHA',True,errors)
    return False
  
  def check_string(self,value,line,pos):
    errors = []
    if ("'" in value):
      errors.append('los strings deben estar entre " (comillas dobles)')
    else:
      return True
    
    self.add_result(value,line,pos,0,'VALOR_STRING',True,errors)
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
  'OBLIGATORIO' : lambda e = 'no_elemento',o = 'no_object': 
    f'El elemento "{e}" es obligatorio en el objeto {o}',
  'VALOR_INVALIDO' : lambda e = 'no_elemento',t = 'no_type': 
    f'Valor invalido para el campo {e}, se esperaba {t}',
  'CARGOS': '"Marketing", "Developer", "Devops", "Product Analyst", "Project Manager", "UX designer", "DB admin"',
  'ESTADOS': '"Canceled", "Done", "To do", "In progress", "On hold"',
  'DOS_PUNTOS' : 'Se esperaba : (dos puntos) para separa la clave del valor',
  'COMA' : {
      'FALTA' : 'Se esperaba , (coma) para separa los elementos',
      'MULTIPLE' : 'se esperaba un elemento clave-valor encontrado , (coma) multiple'
    },
  'EOF' : 'Problemas en el final del archivo'
}

class SyntaxErrors:
  def __init__(self):
    self.errors = []
  
  def get_errors(self):
    return self.errors
  
  def add_error(self,msj,line = 0,pos = 0,last_pos = 0,value = None,type = None):
    band = False
    for err in self.errors:
      if (msj == err['msj'] and line == err['line']):
        band = True
        break
    if (not band):
      self.errors.append({
        'value': value,
        'type': type,
        'line': line,
        'pos': (pos - last_pos) if (last_pos != 0) else pos,
        'msj': msj
      })

def tabs(level):
  tabs = ''
  for i in range(level):
    tabs += '\t'
  return tabs

class FilesHandler:
  def __init__(self):
    self.files = []
    self.dir = os.path.dirname(__file__)
  
  def args_reader(self):
    print()
    if (len(sys.argv) > 1):
      # Los argumentos después del nombre del script son las rutas
      for i in range(1, len(sys.argv)):
        current_path = sys.argv[i]
        self.files_reader(current_path)
        print()  # Separador entre cada ruta procesada
    else:
      print('No se proporcionaron rutas como argumentos al ejecutar el parser.')
      print('Por favor, ingresa las rutas una por una (presiona Enter después de cada una):')
      print('(escribe "parse" para terminar la carga de archivos)')
      print('(escribe "." para analizar el directorio de ejecucion)')
      print('(escribe ".." para analizar el directorio padre de ejecucion)')
      print('(escribe ""(vacio) para analizar el directorio por defecto ../prueba)')
      print('(se aceptan rutas a un archivo individual o directorio a analizar)')
      print('(se aceptan rutas absolutas o relativas(desde el directorio de ejecucion))')
      while True:
        print()  # Separador entre cada ruta procesada
        try:
          ruta_usuario = input('Ruta: ')
        except KeyboardInterrupt:
          break
        if (ruta_usuario.lower() == 'parse'):
          break
        if (len(ruta_usuario) == 0):
          self.files_reader()
        else:
          self.files_reader(ruta_usuario)
  
  def files_reader(self,relative_path = '../prueba'):
    os.chdir(self.dir)
    try:
      special_case = relative_path == '.' or relative_path == '..'
      if (special_case):
        os.chdir(relative_path)
      else:
        os.chdir(os.path.dirname(relative_path))
      path = os.getcwd()
      if (not special_case):
        path = os.path.join(path,os.path.basename(relative_path))
    except :
      print(f'La ruta {relative_path} no existe o no se tiene permisos')
      return None
    print(f'Procesando ruta {path}')
    if (os.path.isfile(path)):
      # Es un archivo
      if (path.endswith('.json')):
        # Es un archivo JSON, cargo su contenido
        self.files.append(self.get_file_content(path))
      else:
        print(f'El archivo {path} no es un archivo JSON')
    elif (os.path.isdir(path)):
      # Es un directorio, buscar archivos JSON en la primera capa
      files = os.listdir(path)
      files_json = [file for file in files if file.endswith('.json')]
      if (files_json):
        print(f'Archivos JSON encontrados en el directorio {path}:')
        for file in files_json:
          self.files.append(self.get_file_content(os.path.join(path, file)))
      else:
        print(f'No se encontraron archivos JSON en el directorio {path}')
    else:
      print(f'La ruta {path} no corresponde a un archivo ni a un directorio válido')
  
  def get_file_content(self,file_path):
    with open(file_path, 'r') as f:
      file_name = os.path.basename(file_path)
      file_dir = os.path.dirname(file_path)
      print(f'Obteniendo contenido del archivo {file_name}')
      file_content = f.read()
      return {
        'path': file_dir,
        'name': file_name,
        'content': file_content
      }
  
  def file_writer(self,path,name,content):
    try:
      with open(os.path.join(path,name + '.html'), 'w') as f:
          f.write(content)
      print(f'         Archivo {name + '.html'} se ha guardado exitosamente en {path}')
    except IOError as e:
      print(f'         Error al intentar guardar el archivo en {path}: {e}')

RESYNC_TOK = ['COMA','CLAUSURA_OBJETO','CLAUSURA_LISTA']
