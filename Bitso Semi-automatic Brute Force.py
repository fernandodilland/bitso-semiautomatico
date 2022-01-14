"""
MIT License

Copyright (c) 2022 Fernando Mireles

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# Programa "Semi-automatic Brute Force" hecho por: Fernando Mireles
# Github: https://github.com/fernandomireles/bitso-semi-automatic-brute-force

import bitso # Para las consultas con los servidores de Bitso
import os.path # Para la consulta del archivo "llaves.txt"

aviso = "\n-----\nAviso: Este programa es su completa responsabilidad, cuide sus llaves API, el programa original solo tendrá conexión con los servidores de Bitso, nadie se hará responsable de un mal uso ni es una recomendación de inversión, Bitso Internacional no creó, no revisó ni aprueba este programa, mismo hecho únicamente con fines educativos.\nUtilice este programa con cautela.\n-----\n"
aviso2 = "Sus llaves API se almacenan sin cifrar en el archivo \"llaves.txt\", se recomienda borrar el archivo cuando no lo vaya a usar"

print(aviso)
print("----------------\nBienvenido(a) al programa gratuito de Trading semi-automático")

if os.path.exists("llaves.txt"): # Si existe el archivo de llaves
    print("Se identificaron llaves API")
    llaves = open('llaves.txt', 'r') # Se abre el archivo de texto "llaves.txt"
    llaves = llaves.readlines()
    api_key = str(llaves[0].strip())
    secret_key = str(llaves[1].strip())

else: # Si no existe el archivo de llaves (primer uso)
    print("\nA continuación se otorga el acceso de este programa con los servidores de Bitso, mediante su API")
    print("Esta información será almacenada en el archivo de texto: \"llaves.txt\" en el mismo directorio")
    api_key = str(input("Llave de API: ")) # Solicitud de API KEY
    secret_key = str(input("Clave secreta de API: ")) # Solicitud de Secret KEY
    print("entro")
    llaves = open("llaves.txt", "a") # Creación del archivo de texto "llaves.txt"
    llaves.write(api_key+"\n"+secret_key)
    llaves.close() # Cierra del archivo

test = input("Prueba 3")
api = bitso.Api(api_key, secret_key)

# Libros de pedidos disponibles en Bitso
libros = api.available_books()
print("Libros disponibles:", libros)

# Extracción de lista
print("Lista:", libros.books)

# Extracción de elemento de lista
print("Elemento 0:", libros.books[0])

test = input("Prueba")
