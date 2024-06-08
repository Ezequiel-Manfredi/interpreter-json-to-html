from lex import lexer_module
from yacc import parser_module
from flask import Flask, render_template, request

app = Flask(__name__)

@app.get("/")
def home_interface():
  return render_template('index.html')

@app.post("/parser")
def parser_files():
  body = request.json
  result = parser_module(body.get('content'))
  return result

@app.post("/lexer")
def lexer_strings():
  body = request.json
  results = lexer_module(body.get('string'))
  return results