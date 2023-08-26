import tkinter as tk
import re

class Lexer:
    def tokenize(self, text):
        self.delimitador = ["{", "}", ";", "(", ")", ":"]
        self.reservada = ["public", "static", "void", "main", "for", "while"]
        self.tiposDato = ["int", "float", "double", "boolean", "char", "str", "list", "tuple", "dict", "set"]
        self.operadores = ["=", "+", "-", "*", "/"]
        self.number_pattern = r'\d+'
        arreglo = []
        current_token = ""
        numeroLinea = 1

        for char in text:
            if char == '\n':
                if current_token != "":
                    arreglo.append((current_token, numeroLinea))
                    current_token = ""
                numeroLinea += 1
                continue

            if char in self.delimitador:
                if current_token != "":
                    arreglo.append((current_token, numeroLinea))
                    current_token = ""

                arreglo.append((char, numeroLinea))
            elif char.isspace():
                if current_token != "":
                    arreglo.append((current_token, numeroLinea))
                    current_token = ""
            else:
                current_token += char
        if current_token != "":
            arreglo.append((current_token, numeroLinea))
        return arreglo

    def validar_identificador(self, token):
        if token.isalpha():
            return True
        return False

    def analyze(self, text):
        arreglo = self.tokenize(text)
        result = ""
        total_delimitadores = 0
        total_reservadas = 0
        total_tipos_dato = 0
        total_numeros = 0
        total_operadores = 0
        total_identificadores = 0

        for i, (token, numeroLinea) in enumerate(arreglo):
            if token in self.delimitador:
                result += f"Linea {numeroLinea} ({token}) es un delimitador\n"
                total_delimitadores += 1
            elif token in self.operadores:
                result += f"Linea {numeroLinea} ({token}) es un operador\n"
                total_operadores += 1
            elif token in self.reservada:
                result += f"Linea {numeroLinea} ({token}) es una palabra reservada\n"
                total_reservadas += 1
            elif re.match(self.number_pattern, token):
                result += f"Linea {numeroLinea} ({token}) es un número\n"
                total_numeros += 1
            elif token in self.tiposDato:
                result += f"Linea {numeroLinea} ({token}) es un tipo de dato\n"
                total_tipos_dato += 1
            elif self.validar_identificador(token) and i > 0 and arreglo[i - 1][0] in self.tiposDato:
                result += f"Linea {numeroLinea} ({token}) es un identificador\n"
                total_identificadores += 1
            else:
                result += f"Linea {numeroLinea} ({token}) error lexico\n"

        if text.strip():
            result += f"\nTotal delimitadores: {total_delimitadores}\n"
            result += f"Total reservadas: {total_reservadas}\n"
            result += f"Total tipos de dato: {total_tipos_dato}\n"
            result += f"Total operadores: {total_operadores}\n"
            result += f"Total identificadores: {total_identificadores}\n"
        else:
            result += f"No hay texto"
        return result

class LexerApp:
    def __init__(self):
        self.windows = tk.Tk()
        self.windows.title("Analizador léxico")

        self.text_input = tk.Text(self.windows, height=10, width=50)
        self.text_input.pack()

        self.analyze_button = tk.Button(self.windows, text="Analizar", command=self.analyze_text)
        self.analyze_button.pack()

        self.clean_button = tk.Button(self.windows, text="Eliminar", command=self.clean_text)
        self.clean_button.pack()

        self.result_label = tk.Label(self.windows, text="", height=30, width=50)
        self.result_label.pack()

    def analyze_text(self):
        lexer = Lexer()
        text = self.text_input.get("1.0", "end")
        result = lexer.analyze(text)
        self.result_label.config(text=result)

    def clean_text(self):
        self.text_input.delete("1.0", "end")
        self.result_label.config(text="")

    def run(self):
        self.windows.mainloop()

app = LexerApp()
app.run()
