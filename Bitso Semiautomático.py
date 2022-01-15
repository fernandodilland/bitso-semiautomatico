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
# Programa "Semiautomático" hecho por: Fernando Mireles
# Github: https://github.com/fernandomireles/bitso-semiautomatico

import bitso # Para las consultas con los servidores de Bitso
import os.path # Para la consulta del archivo "llaves.txt"

aviso = "\n-----\nAviso: Este programa es su completa responsabilidad, cuide sus llaves API, el programa actual solo tendrá conexión con los servidores de Bitso, nadie se hará responsable de un mal uso ni es una recomendación de inversión, Bitso Internacional no creó, no revisó ni aprueba este programa, mismo hecho únicamente con fines educativos.\nUtilice este programa con cautela.\n-----\n"
aviso2 = "\nSus llaves API se almacenaron sin cifrar en el archivo \"llaves.txt\", se recomienda borrar el archivo cuando no lo vaya a usar"
aviso3 = "¡Cuidado! Puso una cantidad con la cual hubiera perdido dinero, intente de nuevo"

print(aviso)
print("Bienvenido(a) al programa gratuito Semiautomático para la API de Bitso")

if os.path.exists("llaves.txt"): # Si existe el archivo de llaves
    print("\nSe identificaron las llaves API:")
    llaves = open('llaves.txt', 'r') # Se abre el archivo de texto "llaves.txt"
    llaves = llaves.readlines()
    api_key = str(llaves[0].strip())
    api_secret = str(llaves[1].strip())
    print("API Key:", api_key)
    print("API Secret:", api_secret)


else: # Si no existe el archivo de llaves (primer uso)
    print("\n> Es la primera vez corriendo el programa <")
    print("\nA continuación se otorga el acceso a este programa con los servidores de Bitso, mediante su API")
    print("Esta información solo será almacenada en el archivo de texto: \"llaves.txt\" en el mismo directorio que este programa")
    api_key = str(input("\nLlave de API: ")) # Solicitud de API KEY
    api_secret = str(input("Clave secreta de API: ")) # Solicitud de Secret KEY
    api = bitso.Api(api_key, api_secret)
    llaves = open("llaves.txt", "a") # Creación del archivo de texto "llaves.txt"
    llaves.write(api_key+"\n"+api_secret)
    llaves.close() # Cierra del archivo
    print(aviso2)

api = bitso.Api(api_key, api_secret)

def limpieza_ordenes_abiertas(mercado):
    ordenesAbiertas = api.open_orders(mercado) # Contacto con servidor de Bitso
    if ordenesAbiertas == []: # Verificador
        print("No se identificaron órdenes abiertas")
    else:
        print("\nÓrden(es) localizada(s):",len(ordenesAbiertas),"\n")
        for Orden in ordenesAbiertas:
            print("Oid de la orden:", Orden.oid)
            api.cancel_order(Orden.oid) # Contacto con servidor de Bitso
            print("-> Orden eliminada")
while True:
    try:
        prueba_de_conexion = api.account_status() # Contacto con servidor de Bitso
        print("\nConfirmación del ID de usuario:", prueba_de_conexion.client_id)
        break
    except:
        print("\nError, las llaves API no funcionan")
        os.remove("llaves.txt")
        print("\nSe borró el archivo \"llaves.txt\" para que pueda volver a intentar con sus llaves")
        api_key = str(input("\nLlave de API: ")) # Solicitud de API KEY
        api_secret = str(input("Clave secreta de API: ")) # Solicitud de Secret KEY
        api = bitso.Api(api_key, api_secret)
        llaves = open("llaves.txt", "a") # Creación del archivo de texto "llaves.txt"
        llaves.write(api_key+"\n"+api_secret)
        llaves.close() # Cierra del archivo
        print(aviso2)

try:
    while True:
        print("\nMercados disponibles:")
        print(*api.available_books().books, sep = ", ") # Contacto con servidor de Bitso

        while True: # Ciclo general
            while True: # Ciclo para declarar y confirmar mercado
                mercado = str(input("\nMercado con el que trabajaremos (ejemplo: btc_mxn): "))
                if mercado in api.available_books().books: # Contacto con servidor de Bitso
                    mercado_lista = mercado.split('_') # Almacena el mercado por separado
                    break
                else:
                    print("\nError, escriba un mercado existente")

            opcion = int(input("\nMenú de opciones:\n1) Poner una orden\n2) Quitar una orden en específico\n3) Quitar todas las órdenes de "+ mercado+ "\n4) Salir\n> "))
            if opcion == 1:
                balances = api.balances() # Contacto con servidor de Bitso

                balances_detalle = balances.__dict__ # Convierte del formato Bitso a Python

                print("\nDisponible de", mercado_lista[1], ":",balances_detalle[mercado_lista[1]].available)
                print("Disponible de", mercado_lista[0], ":",balances_detalle[mercado_lista[0]].available)

                opcion = int(input("\nSubmenú:\n1) Postura de compra de "+ mercado_lista[0]+" con saldo "+ mercado_lista[1]+"\n2) Postura de venta de "+ mercado_lista[0]+" para conseguir "+ mercado_lista[1]+"\n> "))
                posturas = api.ticker(mercado) # Contacto con servidor de Bitso

                if opcion == 1:
                    print("\nHay disponible", balances_detalle[mercado_lista[1]].available, mercado_lista[1], "para comprar")
                    print("\nPrecio más alto de las posturas de compra:", posturas.bid,"con fecha:", posturas.created_at)
                    while True:
                        precio = float(input("Precio (ejemplo: "+str(posturas.bid)+" o menos cantidad): "))
                        if precio < float(posturas.bid):
                            break
                        else:
                            print(aviso3)
                    ejemplo = balances_detalle[mercado_lista[1]].available
                    total = format(float(input("Total: (ejemplo: "+ str(ejemplo) +" o menos): "))/precio, '.8f')
                    orden = api.place_order(book=mercado, side='buy', order_type='limit', major=str(total), price=str(precio)) # Contacto con servidor de Bitso
                    print("-> Orden puesta, con Oid:",orden['oid'])
                    opcion = 0
                if opcion == 2:
                    print("\nHay disponible", balances_detalle[mercado_lista[0]].available, mercado_lista[0], "para vender")
                    print("\nPrecio más bajo de las posturass de venta:", posturas.ask,"con fecha:", posturas.created_at)
                    while True:
                        precio = input("Precio (ejemplo: "+str(posturas.ask)+" o más cantidad): ")
                        if float(precio) > float(posturas.ask):
                            break
                        else:
                            print(aviso3)
                    ejemplo = balances_detalle[mercado_lista[0]].available
                    total = input("Total (ejemplo: "+ str(ejemplo) +" o menos): ")
                    orden = api.place_order(book=mercado, side='sell', order_type='limit', major=str(total), price=str(precio)) # Contacto con servidor de Bitso
                    print("-> Orden puesta, con Oid:", orden['oid'])
                    opcion = 0
            if opcion == 2:
                ordenesAbiertas = api.open_orders(mercado) # Contacto con servidor de Bitso
                if ordenesAbiertas == []: # Verificador
                    print("No se identificaron órdenes abiertas")
                else:
                    print("\nÓrden(es) localizada(s):",len(ordenesAbiertas),"\n")
                    for Orden in ordenesAbiertas:
                        print("Oid de la orden:", Orden.oid)
                        print("Posición de orden:", Orden.side)
                        print("Precio de la orden:", Orden.price)
                        print("Monto original:", Orden.original_amount)
                        print("---")
                    cancelacion = api.cancel_order(str(input("Oid de la orden a quitar: ")))
                    if not cancelacion == []:
                        print("Orden eliminada satisfactoriamente")
                    else:
                        print("No se localizó la orden a quitar")
                    opcion = 0
            if opcion == 3:
                limpieza_ordenes_abiertas(mercado)
            if opcion == 4:
                break

        input("Presione enter para salir")
        break
except:
    print("Hubo un error en el sistema")
    input("Presione enter para salir")
