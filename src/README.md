## directorio src. archivos fuente del proyecto

-	Requisitos de ejecución, El programa fué ejecutado en Windows 11 y los requisitos son:
    * Python versión. 3.12.3
    * Paquete PLY (Python Lex-Yacc) ver 3.11
    * Flask versión 3.0.3

-	Instalación del programa:
    *	Instalar Python
    *	Luego en el terminal ejecutar: `pip install ply` y luego `pip install Flask`

-	Formas de ejecutar el programa, contamos con dos maneras de ejecutar el programa: la primera es por terminal y la segunda por UI (interfaz de usuario).
    * Por terminal:
        -	En el terminal en el directorio src ejecutar: `python ./lex.py`
        - Se ejecutará el Lexer interactivo, donde se puede ingresar los inputs y se mostraran los resultados del análisis Lexico.

    * Por interfaz gráfica:
        - En el terminal en el directorio src ejecutar: `flask --app ./server.py run`
        - Saldrá una url en donde estará la UI ejecutándose.

    - Para terminar los procesos presione `ctrl + C`

-   Compilacion del programa para generar el archivo.exe: `pip install pyinstaller`
    * Modulo lexer interactivo: `pyinstaller -D -F .\lex.py`
    * Modulo UI lexer parser integrados: `pyinstaller -D -F --add-data "templates;templates" --add-data "static;static" .\server.py`