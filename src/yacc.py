import ply.yacc as yacc
from lex import tokens
from utils import SYNTAX_ERROR_MESSAGES as SEM , SyntaxErrors

def p_json(p):
  'json : apertura_objeto contenido clausura_objeto'
  p[0] = p[2]

# producciones del contenido y error campo obligatorio empresas

def p_contenido_1(p):
  '''
  contenido : empresas coma version coma firma
            | empresas coma firma coma version
            | empresas coma version
            | empresas coma firma
            | empresas
  '''
  p[0] = p[1]
def p_contenido_2(p):
  '''
  contenido : version coma empresas coma firma
            | firma coma empresas coma version
            | version coma empresas
            | firma coma empresas
  '''
  p[0] = p[3]
def p_contenido_3(p):
  '''
  contenido : version coma firma coma empresas
            | firma coma version coma empresas
  '''
  p[0] = p[5]
def p_contenido_error_empresas_necesario(p):
  '''
  contenido : version coma firma
            | firma coma version
            | version
            | firma
            | vacio
  '''
  p.parser.error.add_error(SEM['OBLIGATORIO']['EMPRESAS'])
  pass

# produccion de version y error valor no valido

def p_version(p):
  '''
  version : CLAVE_VERSION dos_puntos VALOR_NULL
          | CLAVE_VERSION dos_puntos VALOR_STRING
  '''
  pass
def p_version_error_valor_invalido(p):
  'version : CLAVE_VERSION dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

# produccion de firma y error valor no valido

def p_firma(p):
  '''
  firma : CLAVE_FIRMA_DIGITAL dos_puntos VALOR_NULL
        | CLAVE_FIRMA_DIGITAL dos_puntos VALOR_STRING
  '''
  pass
def p_firma_error_valor_invalido(p):
  'firma : CLAVE_FIRMA_DIGITAL dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

# produccion de empresas y error de lista vacia

def p_empresas(p):
  'empresas : CLAVE_EMPRESAS dos_puntos apertura_lista lista_empresas clausura_lista'
  p[0] = p[4]
def p_empresas_error_vacio(p):
  'empresas : CLAVE_EMPRESAS dos_puntos apertura_lista vacio clausura_lista'
  p.parser.error.add_error(SEM['LISTA']['VACIO'])
  pass
def p_empresas_error_valor_invalido(p):
  'empresas : CLAVE_EMPRESAS dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_lista_empresas(p):
  '''
  lista_empresas : apertura_objeto empresa clausura_objeto coma lista_empresas
                 | apertura_objeto empresa clausura_objeto
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]

# atributos del objeto empresa
    
def p_empresa_1(p):
  'empresa : nombre_empresa coma fundacion coma direccion coma ingresos_anuales coma pyme coma link coma departamentos'
  p[0] = f'<div>{p[1]}{p[11]}{p[13]}</div>'
def p_empresa_2(p):
  'empresa : nombre_empresa coma fundacion coma ingresos_anuales coma pyme coma link coma departamentos'
  p[0] = f'<div>{p[1]}{p[9]}{p[11]}</div>'
def p_empresa_3(p):
  'empresa : nombre_empresa coma fundacion coma direccion coma ingresos_anuales coma pyme coma departamentos'
  p[0] = f'<div>{p[1]}{p[11]}</div>'
def p_empresa_4(p):
  'empresa : nombre_empresa coma fundacion coma ingresos_anuales coma pyme coma departamentos'
  p[0] = f'<div>{p[1]}{p[9]}</div>'

# pares clave-valor y sus errores

def p_nombre_empresa(p):
  'nombre_empresa : CLAVE_NOMBRE_EMPRESA dos_puntos VALOR_STRING'
  p[0] = f'<h1>{p[3]}</h1>'
def p_nombre_empresa_error_valor_invalido(p):
  'nombre_empresa : CLAVE_NOMBRE_EMPRESA dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_fundacion(p):
  'fundacion : CLAVE_FUNDACION dos_puntos VALOR_ENTERO'
  pass
def p_fundacion_error_valor_invalido(p):
  'fundacion : CLAVE_FUNDACION dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_direccion(p):
  '''
  direccion : CLAVE_DIRECCION dos_puntos VALOR_NULL
            | CLAVE_DIRECCION dos_puntos apertura_objeto clausura_objeto
            | CLAVE_DIRECCION dos_puntos apertura_objeto atributos_direccion clausura_objeto
  '''
  pass
def p_direccion_error_valor_invalido(p):
  'direccion : CLAVE_DIRECCION dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_ingresos_anuales(p):
  'ingresos_anuales : CLAVE_INGRESOS_ANUALES dos_puntos VALOR_REAL'
  pass
def p_ingresos_anuales_error_valor_invalido(p):
  'ingresos_anuales : CLAVE_INGRESOS_ANUALES dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_pyme(p):
  'pyme : CLAVE_PYME dos_puntos VALOR_BOOL'
  pass
def p_pyme_error_valor_invalido(p):
  'pyme : CLAVE_PYME dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_link(p):
  '''
  link : CLAVE_LINK dos_puntos VALOR_NULL
       | CLAVE_LINK dos_puntos VALOR_URL
  '''
  if (p[3]):
    p[0] = f'<a href="{p[3]}">{p[3]}</a>'
def p_link_error_valor_invalido(p):
  'link : CLAVE_LINK dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

# produccion de departamentos y error de lista vacia

def p_departamentos(p):
  'departamentos : CLAVE_DEPARTAMENTOS dos_puntos apertura_lista lista_departamentos clausura_lista'
  p[0] = p[4]
def p_departamentos_error_vacio(p):
  'departamentos : CLAVE_DEPARTAMENTOS dos_puntos apertura_lista vacio clausura_lista'
  p.parser.error.add_error(SEM['LISTA']['VACIO'])
  pass
def p_departamentos_error_valor_invalido(p):
  'departamentos : CLAVE_DEPARTAMENTOS dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

# atributos del objeto direccion

def p_atributos_direccion(p):
  '''
  atributos_direccion : calle coma ciudad coma pais
                      | calle coma pais coma ciudad
                      | ciudad coma calle coma pais
                      | ciudad coma pais coma calle
                      | pais coma calle coma ciudad
                      | pais coma ciudad coma calle
  '''
  pass

# pares clave-valor y sus errores

def p_calle(p):
  'calle : CLAVE_CALLE dos_puntos VALOR_STRING'
  pass
def p_calle_error_valor_invalido(p):
  'calle : CLAVE_CALLE dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_ciudad(p):
  'ciudad : CLAVE_CIUDAD dos_puntos VALOR_STRING'
  pass
def p_ciudad_error_valor_invalido(p):
  'ciudad : CLAVE_CIUDAD dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_pais(p):
  'pais : CLAVE_PAIS dos_puntos VALOR_STRING'
  pass
def p_pais_error_valor_invalido(p):
  'pais : CLAVE_PAIS dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_lista_departamentos(p):
  '''
  lista_departamentos : apertura_objeto departamento clausura_objeto coma lista_departamentos
                      | apertura_objeto departamento clausura_objeto
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]

# atributos del objeto departamento

def p_departamento_1(p):
  '''
  departamento : nombre_departamento coma subdepartamentos coma jefe
               | nombre_departamento coma jefe coma subdepartamentos
               | jefe coma nombre_departamento coma subdepartamentos
               | nombre_departamento coma subdepartamentos
  '''
  if (not p[1]):
    p[0] = p[3] + p[5]
  else:
    p[0] = p[1]
    if (not p[3]):
      p[0] += p[5]
    else:
      p[0] += p[3]
def p_departamento_2(p):
  '''
  departamento : subdepartamentos coma nombre_departamento coma jefe
               | subdepartamentos coma jefe coma nombre_departamento
               | jefe coma subdepartamentos coma nombre_departamento
               | subdepartamentos coma nombre_departamento
  '''
  if (not p[1]):
    p[0] = p[5] + p[3]
  else:
    if (not p[3]):
      p[0] = p[5]
    else:
      p[0] = p[3]
    p[0] += p[1]

# pares clave-valor y sus errores

def p_nombre_departamento(p):
  'nombre_departamento : CLAVE_NOMBRE dos_puntos VALOR_STRING'
  p[0] = f'<h2>{p[3]}</h2>'
def p_nombre_departamento_error(p):
  'nombre_departamento : CLAVE_NOMBRE dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_jefe(p):
  '''
  jefe : CLAVE_JEFE dos_puntos VALOR_NULL
       | CLAVE_JEFE dos_puntos VALOR_STRING
  '''
  pass
def p_jefe_error(p):
  'jefe : CLAVE_JEFE dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

# produccion de subdepartamentos y error de vacio

def p_subdepartamentos(p):
  'subdepartamentos : CLAVE_SUBDEPARTAMENTOS dos_puntos apertura_lista lista_subdepartamentos clausura_lista'
  p[0] = p[4]
def p_subdepartamentos_error_vacio(p):
  'subdepartamentos : CLAVE_SUBDEPARTAMENTOS dos_puntos apertura_lista vacio clausura_lista'
  p.parser.error.add_error(SEM['LISTA']['VACIO'])
  pass
def p_subdepartamentos_error(p):
  'subdepartamentos : CLAVE_SUBDEPARTAMENTOS dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_lista_subdepartamentos(p):
  '''
  lista_subdepartamentos : apertura_objeto subdepartamento clausura_objeto coma lista_subdepartamentos
                         | apertura_objeto subdepartamento clausura_objeto
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]

# atributos del objeto subdepartamento

def p_subdepartamento_1(p):
  '''
  subdepartamento : nombre_subdepartamento coma empleados coma jefe
                  | nombre_subdepartamento coma jefe coma empleados
                  | jefe coma nombre_subdepartamento coma empleados
                  | nombre_subdepartamento coma empleados
  '''
  if (not p[1]):
    p[0] = p[3] + p[5]
  else:
    p[0] = p[1]
    if (not p[3]):
      p[0] += p[5]
    else:
      p[0] += p[3]
def p_subdepartamento_2(p):
  '''
  subdepartamento : empleados coma nombre_subdepartamento coma jefe
                  | empleados coma jefe coma nombre_subdepartamento
                  | jefe coma empleados coma nombre_subdepartamento
                  | empleados coma nombre_subdepartamento
  '''
  if (not p[1]):
    p[0] = p[5] + p[3]
  else:
    if (not p[3]):
      p[0] = p[5]
    else:
      p[0] = p[3]
    p[0] += p[1]
def p_subdepartamento_3(p):
  '''
  subdepartamento : nombre_subdepartamento coma jefe
                  | jefe coma nombre_subdepartamento
                  | nombre_subdepartamento
  '''
  if (not p[1]):
    p[0] = p[3]
  else:
    p[0] = p[1]

# pares clave-valor y sus errores

def p_nombre_subdepartamento(p):
  'nombre_subdepartamento : CLAVE_NOMBRE dos_puntos VALOR_STRING'
  p[0] = f'<h3>{p[3]}</h3>'
def p_nombre_subdepartamento_error(p):
  'nombre_subdepartamento : CLAVE_NOMBRE dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

# produccion de empleados

def p_empleados(p):
  '''
  empleados : CLAVE_EMPLEADOS dos_puntos VALOR_NULL
            | CLAVE_EMPLEADOS dos_puntos apertura_lista clausura_lista
            | CLAVE_EMPLEADOS dos_puntos apertura_lista lista_empleados clausura_lista
  '''
  if (len(p) == 6):
    p[0] = f'<ul>{p[4]}</ul>'
def p_empleados_error(p):
  'empleados : CLAVE_EMPLEADOS dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_lista_empleados(p):
  '''
  lista_empleados : apertura_objeto empleado clausura_objeto coma lista_empleados
                  | apertura_objeto empleado clausura_objeto
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]

# atributos del objeto empleado

def p_empleado_1(p):
  'empleado : nombre_empleado coma edad coma cargo coma salario coma activo coma fecha_contratacion coma proyectos'
  p[0] = f'<li>{p[1]}</li>{p[13]}'
def p_empleado_2(p):
  'empleado : nombre_empleado coma cargo coma salario coma activo coma fecha_contratacion coma proyectos'
  p[0] = f'<li>{p[1]}</li>{p[11]}'
def p_empleado_3(p):
  'empleado : nombre_empleado coma edad coma cargo coma salario coma activo coma fecha_contratacion'
  p[0] = f'<li>{p[1]}</li>'

# pares clave-valor y sus errores

def p_nombre_empleado(p):
  'nombre_empleado : CLAVE_NOMBRE dos_puntos VALOR_STRING'
  p[0] = p[3]
def p_nombre_empleado_error(p):
  'nombre_empleado : CLAVE_NOMBRE dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_edad(p):
  '''
  edad : CLAVE_EDAD dos_puntos VALOR_NULL
       | CLAVE_EDAD dos_puntos VALOR_ENTERO
  '''
  pass
def p_edad_error(p):
  'edad : CLAVE_EDAD dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_cargo(p):
  'cargo : CLAVE_CARGO dos_puntos VALOR_CARGO'
  pass
def p_cargo_error(p):
  'cargo : CLAVE_CARGO dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_salario(p):
  'salario : CLAVE_SALARIO dos_puntos VALOR_REAL'
  pass
def p_salario_error(p):
  'salario : CLAVE_SALARIO dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_activo(p):
  'activo : CLAVE_ACTIVO dos_puntos VALOR_BOOL'
  pass
def p_activo_error(p):
  'activo : CLAVE_ACTIVO dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_fecha_contratacion(p):
  'fecha_contratacion : CLAVE_FECHA_CONTRATACION dos_puntos VALOR_FECHA'
  pass
def p_fecha_contratacion_error(p):
  'fecha_contratacion : CLAVE_FECHA_CONTRATACION dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

# produccion de proyectos

def p_proyectos(p):
  '''
  proyectos : CLAVE_PROYECTOS dos_puntos VALOR_NULL
            | CLAVE_PROYECTOS dos_puntos apertura_lista clausura_lista
            | CLAVE_PROYECTOS dos_puntos apertura_lista lista_proyectos clausura_lista
  '''
  if (len(p) == 6):
    head = '<thead><tr><th>Nombre</th><th>Estado</th><th>Fecha de inicio</th><th>Fecha de fin</th></tr></thead>'
    p[0] = f'<table>{head}<tbody>{p[4]}</tbody></table>'
def p_proyectos_error(p):
  'proyectos : CLAVE_PROYECTOS dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_lista_proyectos(p):
  '''
  lista_proyectos : apertura_objeto proyecto clausura_objeto coma lista_proyectos
                  | apertura_objeto proyecto clausura_objeto
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]

# atributos del objeto proyecto

def p_proyecto_1(p):
  'proyecto : nombre_proyecto coma estado coma fecha_inicio coma fecha_fin'
  p[0] = f'<tr>{p[1]}{p[3]}{p[5]}{p[7]}</tr>'
def p_proyecto_2(p):
  'proyecto : nombre_proyecto coma estado coma fecha_inicio'
  p[0] = f'<tr>{p[1]}{p[3]}{p[5]}<th></th></tr>'
def p_proyecto_3(p):
  'proyecto : nombre_proyecto coma fecha_inicio coma fecha_fin'
  p[0] = f'<tr>{p[1]}<th></th>{p[3]}{p[5]}</tr>'
def p_proyecto_4(p):
  'proyecto : nombre_proyecto coma fecha_inicio'
  p[0] = f'<tr>{p[1]}<th></th>{p[3]}<th></th></tr>'

# pares clave-valor y sus errores

def p_nombre_proyecto(p):
  'nombre_proyecto : CLAVE_NOMBRE dos_puntos VALOR_STRING'
  p[0] = f'<th>{p[3]}</th>'
def p_nombre_proyecto_error(p):
  'nombre_proyecto : CLAVE_NOMBRE dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_estado(p):
  '''
  estado : CLAVE_ESTADO dos_puntos VALOR_NULL
         | CLAVE_ESTADO dos_puntos VALOR_ESTADO
  '''
  p[0] = f'<th>{p[3]}</th>'
def p_estado_error(p):
  'estado : CLAVE_ESTADO dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_fecha_inicio(p):
  'fecha_inicio : CLAVE_FECHA_INICIO dos_puntos VALOR_FECHA'
  p[0] = f'<th>{p[3]}</th>'
def p_fecha_inicio_error(p):
  'fecha_inicio : CLAVE_FECHA_INICIO dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

def p_fecha_fin(p):
  '''
  fecha_fin : CLAVE_FECHA_FIN dos_puntos VALOR_NULL
            | CLAVE_FECHA_FIN dos_puntos VALOR_FECHA
  '''
  p[0] = f'<th>{p[3]}</th>'
def p_fecha_fin_error(p):
  'fecha_fin : CLAVE_FECHA_FIN dos_puntos error'
  p.parser.error.add_error(SEM['VALOR_INVALIDO'])
  pass

# producciones de apertura y clausura de objeto y sus errores

def p_apertura_objeto(p):
  'apertura_objeto : APERTURA_OBJETO'
  pass
def p_apertura_objeto_error_vacio(p):
  'apertura_objeto : vacio'
  p.parser.error.add_error(SEM['OBJETO']['APERTURA'])
  pass

def p_clausura_objeto(p):
  'clausura_objeto : CLAUSURA_OBJETO'
  pass
def p_clausura_objeto_error_vacio(p):
  'clausura_objeto : vacio'
  p.parser.error.add_error(SEM['OBJETO']['CLAUSURA'])
  pass
def p_clausura_objeto_error(p):
  'clausura_objeto : error CLAUSURA_OBJETO'
  p.parser.error.add_error(SEM['OBJETO']['COMA_EXTRA'])
  pass

# producciones de apertura y clausura de lista y sus errores

def p_apertura_lista(p):
  'apertura_lista : APERTURA_LISTA'
  pass
def p_apertura_lista_error_vacio(p):
  'apertura_lista : vacio'
  p.parser.error.add_error(SEM['LISTA']['APERTURA'])
  pass

def p_clausura_lista(p):
  'clausura_lista : CLAUSURA_LISTA'
  pass
def p_clausura_lista_error_vacio(p):
  'clausura_lista : vacio'
  p.parser.error.add_error(SEM['LISTA']['CLAUSURA'])
  pass
def p_clausura_lista_error(p):
  'clausura_lista : error CLAUSURA_LISTA'
  p.parser.error.add_error(SEM['LISTA']['COMA_EXTRA'])
  pass

# produccion de dos puntos y error

def p_dos_puntos(p):
  'dos_puntos : DOS_PUNTOS'
  pass
def p_dos_puntos_error_vacio(p):
  'dos_puntos : vacio'
  p.parser.error.add_error(SEM['DOS_PUNTOS'])
  pass

# produccion de coma y error

def p_coma(p):
  'coma : COMA'
  pass
def p_coma_error_vacio(p):
  'coma : vacio'
  p.parser.error.add_error(SEM['COMA'])
  pass

# produccion vacia

def p_vacio(p):
  'vacio :'
  pass

def p_error(p):
  print(p)
  if p:
    return p
  else:
    parser.error.add_error(SEM['EOF'])

parser = yacc.yacc(errorlog=yacc.NullLogger()) #debug=False errorlog=yacc.NullLogger()

def parser_module(data):
  parser.error = SyntaxErrors()
  result = parser.parse(data)
  errors = parser.error.get_errors()
  if len(errors) == 0:
    return { 'ok': True, 'content': result }
  else:
    return { 'ok': False, 'errors': errors }

if __name__ == '__main__':
  example = '''
    {
      "empresas": [{
        "nombre_empresa": "PacoSRL",
        "fundacion": 2005,
        "direccion": null,
        "ingresos_anuales": 200000.25,
        "pyme": false,
        "departamentos": [
        {
          "nombre": "Ventas",
          "subdepartamentos": [{
            "nombre": "Mc Donalds JUC",
            "empleados": [{
              "nombre": "Sideshow Mel",
              "cargo": "Product Analyst",
              "salario": 1250.65,
              "activo": true,
              "fecha_contratacion": "2023-09-10",
              "proyectos": [{
                "nombre": "Mc Flurry",
                "fecha_inicio": "2022-01-10",
                "fecha_fin": null
              }]
            }]
          }]
        }]
      }]
    }
  '''
  result = parser_module(example)
  print(result)
