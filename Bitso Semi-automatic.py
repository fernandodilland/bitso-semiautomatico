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
# Programa "Semi-automatic" hecho por: Fernando Mireles
# Github: https://github.com/fernandomireles/bitso-semi-automatic

import bitso # Para las consultas con los servidores de Bitso
import os.path # Para la consulta del archivo "llaves.txt"

aviso = "\n-----\nAviso: Este programa es su completa responsabilidad, cuide sus llaves API, el programa original solo tendrá conexión con los servidores de Bitso, nadie se hará responsable de un mal uso ni es una recomendación de inversión, Bitso Internacional no creó, no revisó ni aprueba este programa, mismo hecho únicamente con fines educativos.\nUtilice este programa con cautela.\n-----\n"
aviso2 = "Sus llaves API se almacenan sin cifrar en el archivo \"llaves.txt\", se recomienda borrar el archivo cuando no lo vaya a usar"

print(aviso)
print("----------------\nBienvenido(a) al programa gratuito Semi-automatic")

if os.path.exists("llaves.txt"): # Si existe el archivo de llaves
    print("\nSe identificaron las llaves API:")
    llaves = open('llaves.txt', 'r') # Se abre el archivo de texto "llaves.txt"
    llaves = llaves.readlines()
    api_key = str(llaves[0].strip())
    api_secret = str(llaves[1].strip())
    print("API Key:", api_key)
    print("API Secret:", api_secret)

else: # Si no existe el archivo de llaves (primer uso)
    print("\nA continuación se otorga el acceso de este programa con los servidores de Bitso, mediante su API")
    print("Esta información será almacenada en el archivo de texto: \"llaves.txt\" en el mismo directorio")
    api_key = str(input("Llave de API: ")) # Solicitud de API KEY
    api_secret = str(input("Clave secreta de API: ")) # Solicitud de Secret KEY
    api = bitso.Api(api_key, api_secret)
    llaves = open("llaves.txt", "a") # Creación del archivo de texto "llaves.txt"
    llaves.write(api_key+"\n"+api_secret)
    llaves.close() # Cierra del archivo

api = bitso.Api(api_key, api_secret)

try:
    prueba_de_conexion = api.account_status()
    print("\nConfirmación del ID de usuario:",prueba_de_conexion.client_id)

    while True:
        while True:
            print("\nMercados disponibles:",api.available_books().books)
            while True:
                mercado = str(input("\nMercado con el que trabajaremos (ejemplo: btc_mxn): "))
                if mercado in api.available_books().books:
                    mercado_lista = mercado.split('_') # Almacena el mercado por separado
                    break
                else:
                    print("\nError, escriba un mercado existente")

            opcion = int(input("\nMenú de opciones:\n1) Sistemas sencillos\n2) Sistemas automáticos\n3) Salir\n> "))
            if opcion == 1:
                while True:
                    opcion = int(input("\nSubmenú:\n1) Poner una orden\n2) Quitar una orden\n3) Quitar todas las órdenes\n4) Regresar al menú\n> "))
                    if opcion == 1:
                        balances = api.balances() # Guarda balances del usuario al momento

                        balances_detalle = balances.__dict__ # Convierte del formato Bitso a Python

                        print("\nDisponible de",mercado_lista[1],":",balances_detalle[mercado_lista[1]].available)
                        print("Disponible de",mercado_lista[0],":",balances_detalle[mercado_lista[0]].available)

                        opcion = int(input("\nSubmenú:\n1) posturas de compra "+ mercado+"\n2) posturas de venta "+ mercado+"\n> "))
                        posturas = api.ticker(mercado) # Guarda posturas del mercado al momento

                        if opcion == 1:
                            print("\nHay disponible",balances_detalle[mercado_lista[1]].available,mercado_lista[1], "para comprar")
                            print("\nPrecio más alto de las posturas de compra:", posturas.bid,"con fecha:", posturas.created_at)
                            precio = float(input("Precio (ejemplo: "+str(posturas.bid)+" o menos cantidad): "))
                            total = format(float(input("Total: "))/precio, '.8f')
                            orden = api.place_order(book=mercado, side='buy', order_type='limit', major=str(total), price=str(precio))
                            print("Orden puesta, con oid:",orden['oid'])
                        if opcion == 2:
                            print("\nHay disponible",balances_detalle[mercado_lista[0]].available,mercado_lista[0], "para vender")
                            print("\nPrecio más bajo de las posturass de venta:", posturas.ask,"con fecha:", posturas.created_at)
                            precio = input("Precio (ejemplo: "+str(posturas.ask)+" o más cantidad): ")
                            ejemplo = balances_detalle[mercado_lista[0]].available
                            total = input("Total (ejemplo: "+ str(ejemplo) +" o menos): ")
                            orden = api.place_order(book=mercado, side='sell', order_type='limit', major=str(total), price=str(precio))
                            #orden = api.place_order(book=mercado, side='sell', order_type='limit', major='0.00001133', price='890000')
                            print("Orden puesta, con oid:",orden['oid'])
                    if opcion == 4:
                        break
            elif opcion == 2:
                pass
            elif opcion == 3:
                break
        break

    input("Presione enter para salir")
except:
    print("Hubo un error en el sistema")
    input("Presione enter para salir")
