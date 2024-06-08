import ply.yacc as yacc
from lex import tokens

def p_json(p):
  'json : APERTURA_OBJETO contenido CLAUSURA_OBJETO'
  p[0] = p[2]

def p_contenido1(p):
  '''
  contenido : empresas COMA version COMA firma
            | empresas COMA firma COMA version
            | empresas COMA version
            | empresas COMA firma
            | empresas
  '''
  p[0] = p[1]
def p_contenido2(p):
  '''
  contenido : version COMA empresas COMA firma
            | firma COMA empresas COMA version
            | version COMA empresas
            | firma COMA empresas
  '''
  p[0] = p[3]
def p_contenido3(p):
  '''
  contenido : version COMA firma COMA empresas
            | firma COMA version COMA empresas
  '''
  p[0] = p[5]

def p_version(p):
  '''
  version : CLAVE_VERSION DOS_PUNTOS VALOR_NULL
          | CLAVE_VERSION DOS_PUNTOS VALOR_STRING
  '''
  pass

def p_firma(p):
  '''
  firma : CLAVE_FIRMA_DIGITAL DOS_PUNTOS VALOR_NULL
        | CLAVE_FIRMA_DIGITAL DOS_PUNTOS VALOR_STRING
  '''
  pass

def p_empresas(p):
  'empresas : CLAVE_EMPRESAS DOS_PUNTOS APERTURA_LISTA lista_empresas CLAUSURA_LISTA'
  p[0] = p[4]

def p_lista_empresas(p):
  '''
  lista_empresas : APERTURA_OBJETO empresa CLAUSURA_OBJETO COMA lista_empresas
                 | APERTURA_OBJETO empresa CLAUSURA_OBJETO
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]
    
def p_empresa1(p):
  'empresa : nombre_empresa COMA fundacion COMA direccion COMA ingresos_anuales COMA pyme COMA link COMA departamentos'
  p[0] = f'<div>{p[1]}{p[11]}{p[13]}</div>'
def p_empresa2(p):
  'empresa : nombre_empresa COMA fundacion COMA ingresos_anuales COMA pyme COMA link COMA departamentos'
  p[0] = f'<div>{p[1]}{p[9]}{p[11]}</div>'
def p_empresa3(p):
  'empresa : nombre_empresa COMA fundacion COMA direccion COMA ingresos_anuales COMA pyme COMA departamentos'
  p[0] = f'<div>{p[1]}{p[11]}</div>'
def p_empresa4(p):
  'empresa : nombre_empresa COMA fundacion COMA ingresos_anuales COMA pyme COMA departamentos'
  p[0] = f'<div>{p[1]}{p[9]}</div>'

def p_nombre_empresa(p):
  'nombre_empresa : CLAVE_NOMBRE_EMPRESA DOS_PUNTOS VALOR_STRING'
  p[0] = f'<h1>{p[3]}</h1>'

def p_fundacion(p):
  'fundacion : CLAVE_FUNDACION DOS_PUNTOS VALOR_ENTERO'
  pass

def p_direccion(p):
  '''
  direccion : CLAVE_DIRECCION DOS_PUNTOS VALOR_NULL
            | CLAVE_DIRECCION DOS_PUNTOS APERTURA_OBJETO CLAUSURA_OBJETO
            | CLAVE_DIRECCION DOS_PUNTOS APERTURA_OBJETO atributos_direccion CLAUSURA_OBJETO
  '''
  pass

def p_ingresos_anuales(p):
  'ingresos_anuales : CLAVE_INGRESOS_ANUALES DOS_PUNTOS VALOR_REAL'
  pass

def p_pyme(p):
  'pyme : CLAVE_PYME DOS_PUNTOS VALOR_BOOL'
  pass

def p_link(p):
  '''
  link : CLAVE_LINK DOS_PUNTOS VALOR_NULL
       | CLAVE_LINK DOS_PUNTOS VALOR_URL
  '''
  if (p[3]):
    p[0] = f'<a href="{p[3]}">{p[3]}</a>'

def p_departamentos(p):
  'departamentos : CLAVE_DEPARTAMENTOS DOS_PUNTOS APERTURA_LISTA lista_departamentos CLAUSURA_LISTA'
  p[0] = p[4]

def p_atributos_direccion(p):
  '''
  atributos_direccion : calle COMA ciudad COMA pais
                      | calle COMA pais COMA ciudad
                      | ciudad COMA calle COMA pais
                      | ciudad COMA pais COMA calle
                      | pais COMA calle COMA ciudad
                      | pais COMA ciudad COMA calle
  '''
  pass

def p_calle(p):
  'calle : CLAVE_CALLE DOS_PUNTOS VALOR_STRING'
  pass

def p_ciudad(p):
  'ciudad : CLAVE_CIUDAD DOS_PUNTOS VALOR_STRING'
  pass

def p_pais(p):
  'pais : CLAVE_PAIS DOS_PUNTOS VALOR_STRING'
  pass

def p_lista_departamentos(p):
  '''
  lista_departamentos : APERTURA_OBJETO departamento CLAUSURA_OBJETO COMA lista_departamentos
                      | APERTURA_OBJETO departamento CLAUSURA_OBJETO
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]

def p_departamento1(p):
  '''
  departamento : nombre_departamento COMA subdepartamentos COMA jefe
               | nombre_departamento COMA jefe COMA subdepartamentos
               | jefe COMA nombre_departamento COMA subdepartamentos
               | nombre_departamento COMA subdepartamentos
  '''
  if (not p[1]):
    p[0] = p[3] + p[5]
  else:
    p[0] = p[1]
    if (not p[3]):
      p[0] += p[5]
    else:
      p[0] += p[3]
def p_departamento2(p):
  '''
  departamento : subdepartamentos COMA nombre_departamento COMA jefe
               | subdepartamentos COMA jefe COMA nombre_departamento
               | jefe COMA subdepartamentos COMA nombre_departamento
               | subdepartamentos COMA nombre_departamento
  '''
  if (not p[1]):
    p[0] = p[5] + p[3]
  else:
    if (not p[3]):
      p[0] = p[5]
    else:
      p[0] = p[3]
    p[0] += p[1]

def p_nombre_departamento(p):
  'nombre_departamento : CLAVE_NOMBRE DOS_PUNTOS VALOR_STRING'
  p[0] = f'<h2>{p[3]}</h2>'

def p_jefe(p):
  '''
  jefe : CLAVE_JEFE DOS_PUNTOS VALOR_NULL
       | CLAVE_JEFE DOS_PUNTOS VALOR_STRING
  '''
  p[0] = False

def p_subdepartamentos(p):
  'subdepartamentos : CLAVE_SUBDEPARTAMENTOS DOS_PUNTOS APERTURA_LISTA lista_subdepartamentos CLAUSURA_LISTA'
  p[0] = p[4]

def p_lista_subdepartamentos(p):
  '''
  lista_subdepartamentos : APERTURA_OBJETO subdepartamento CLAUSURA_OBJETO COMA lista_subdepartamentos
                         | APERTURA_OBJETO subdepartamento CLAUSURA_OBJETO
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]

def p_subdepartamento1(p):
  '''
  subdepartamento : nombre_subdepartamento COMA empleados COMA jefe
                  | nombre_subdepartamento COMA jefe COMA empleados
                  | jefe COMA nombre_subdepartamento COMA empleados
                  | nombre_subdepartamento COMA empleados
  '''
  if (not p[1]):
    p[0] = p[3] + p[5]
  else:
    p[0] = p[1]
    if (not p[3]):
      p[0] += p[5]
    else:
      p[0] += p[3]
def p_subdepartamento2(p):
  '''
  subdepartamento : empleados COMA nombre_subdepartamento COMA jefe
                  | empleados COMA jefe COMA nombre_subdepartamento
                  | jefe COMA empleados COMA nombre_subdepartamento
                  | empleados COMA nombre_subdepartamento
  '''
  if (not p[1]):
    p[0] = p[5] + p[3]
  else:
    if (not p[3]):
      p[0] = p[5]
    else:
      p[0] = p[3]
    p[0] += p[1]
def p_subdepartamento3(p):
  '''
  subdepartamento : nombre_subdepartamento COMA jefe
                  | jefe COMA nombre_subdepartamento
                  | nombre_subdepartamento
  '''
  if (not p[1]):
    p[0] = p[3]
  else:
    p[0] = p[1]

def p_nombre_subdepartamento(p):
  'nombre_subdepartamento : CLAVE_NOMBRE DOS_PUNTOS VALOR_STRING'
  p[0] = f'<h3>{p[3]}</h3>'

def p_empleados(p):
  '''
  empleados : CLAVE_EMPLEADOS DOS_PUNTOS VALOR_NULL
            | CLAVE_EMPLEADOS DOS_PUNTOS APERTURA_LISTA CLAUSURA_LISTA
            | CLAVE_EMPLEADOS DOS_PUNTOS APERTURA_LISTA lista_empleados CLAUSURA_LISTA
  '''
  if (len(p) == 6):
    p[0] = f'<ul>{p[4]}</ul>'

def p_lista_empleados(p):
  '''
  lista_empleados : APERTURA_OBJETO empleado CLAUSURA_OBJETO COMA lista_empleados
                  | APERTURA_OBJETO empleado CLAUSURA_OBJETO
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]

def p_empleado1(p):
  'empleado : nombre_empleado COMA edad COMA cargo COMA salario COMA activo COMA fecha_contratacion COMA proyectos'
  p[0] = f'<li>{p[1]}</li>{p[13]}'
def p_empleado2(p):
  'empleado : nombre_empleado COMA cargo COMA salario COMA activo COMA fecha_contratacion COMA proyectos'
  p[0] = f'<li>{p[1]}</li>{p[11]}'
def p_empleado3(p):
  'empleado : nombre_empleado COMA edad COMA cargo COMA salario COMA activo COMA fecha_contratacion'
  p[0] = f'<li>{p[1]}</li>'

def p_nombre_empleado(p):
  'nombre_empleado : CLAVE_NOMBRE DOS_PUNTOS VALOR_STRING'
  p[0] = p[3]

def p_edad(p):
  '''
  edad : CLAVE_EDAD DOS_PUNTOS VALOR_NULL
       | CLAVE_EDAD DOS_PUNTOS VALOR_ENTERO
  '''
  pass

def p_cargo(p):
  'cargo : CLAVE_CARGO DOS_PUNTOS VALOR_CARGO'
  pass

def p_salario(p):
  'salario : CLAVE_SALARIO DOS_PUNTOS VALOR_REAL'
  pass

def p_activo(p):
  'activo : CLAVE_ACTIVO DOS_PUNTOS VALOR_BOOL'
  pass

def p_fecha_contratacion(p):
  'fecha_contratacion : CLAVE_FECHA_CONTRATACION DOS_PUNTOS VALOR_FECHA'
  pass

def p_proyectos(p):
  '''
  proyectos : CLAVE_PROYECTOS DOS_PUNTOS VALOR_NULL
            | CLAVE_PROYECTOS DOS_PUNTOS APERTURA_LISTA CLAUSURA_LISTA
            | CLAVE_PROYECTOS DOS_PUNTOS APERTURA_LISTA lista_proyectos CLAUSURA_LISTA
  '''
  if (len(p) == 6):
    p[0] = f'<table><thead><tr><th>Nombre</th><th>Estado</th><th>Fecha de inicio</th><th>Fecha de fin</th></tr></thead><tbody>{p[4]}</tbody></table>'

def p_lista_proyectos(p):
  '''
  lista_proyectos : APERTURA_OBJETO proyecto CLAUSURA_OBJETO COMA lista_proyectos
                  | APERTURA_OBJETO proyecto CLAUSURA_OBJETO
  '''
  p[0] = p[2]
  if (len(p) == 6):
    p[0] += p[5]

def p_proyecto1(p):
  'proyecto : nombre_proyecto COMA estado COMA fecha_inicio COMA fecha_fin'
  p[0] = f'<tr>{p[1]}{p[3]}{p[5]}{p[7]}</tr>'
def p_proyecto2(p):
  'proyecto : nombre_proyecto COMA estado COMA fecha_inicio'
  p[0] = f'<tr>{p[1]}{p[3]}{p[5]}<th></th></tr>'
def p_proyecto3(p):
  'proyecto : nombre_proyecto COMA fecha_inicio COMA fecha_fin'
  p[0] = f'<tr>{p[1]}<th></th>{p[3]}{p[5]}</tr>'
def p_proyecto4(p):
  'proyecto : nombre_proyecto COMA fecha_inicio'
  p[0] = f'<tr>{p[1]}<th></th>{p[3]}<th></th></tr>'

def p_nombre_proyecto(p):
  'nombre_proyecto : CLAVE_NOMBRE DOS_PUNTOS VALOR_STRING'
  p[0] = f'<th>{p[3]}</th>'

def p_estado(p):
  '''
  estado : CLAVE_ESTADO DOS_PUNTOS VALOR_NULL
         | CLAVE_ESTADO DOS_PUNTOS VALOR_ESTADO
  '''
  p[0] = f'<th>{p[3]}</th>'

def p_fecha_inicio(p):
  'fecha_inicio : CLAVE_FECHA_INICIO DOS_PUNTOS VALOR_FECHA'
  p[0] = f'<th>{p[3]}</th>'

def p_fecha_fin(p):
  '''
  fecha_fin : CLAVE_FECHA_FIN DOS_PUNTOS VALOR_NULL
            | CLAVE_FECHA_FIN DOS_PUNTOS VALOR_FECHA
  '''
  p[0] = f'<th>{p[3]}</th>'

def p_error(p):
  if p == None:
    print(print("Syntax error in end of file"))
  else:
    print("Syntax error in input!",p)

parser = yacc.yacc(debug=False)

def parser_module(data):
  result = parser.parse(data)
  return result

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
