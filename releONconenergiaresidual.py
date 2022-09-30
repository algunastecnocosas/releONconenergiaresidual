import RPi.GPIO as GPIO
import requests
import sys

nivel_para_encendido = 98    #Activamos el rele si el nivel de las baterias supera este valor

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 4      # actuamos sobre el rele 1 (puerto 4)
                       # puertos 22, 6 y 26 para los reles 2, 3 y 4

GPIO.setup(4, GPIO.OUT) # GPIO Assign mode: el pin 4 de la rpi es una salida

#Lectura del script de LuzparaelEko y almacenamiento del nivel de baterías en la variable 'nivel_baterias'
texto = requests.get('http://scripts.eslaeko.net/luzparaeleko/show_last_reading.php?network_id=92931712101193')

# gestion de errores
if texto.status_code == 200:
    print('Consulta a LuzparaelEko exitosa!')
else:  # si se produce un problema en la llamada anterior, el rele se apaga
    print('No hemos podido consultar a LuzparaelEko')
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW)  # apagar el rele
    sys.exit(666) # termina el programa


if '%' in texto.text:
    print('Las baterías están funcionando.')
else:
    print('Parece que el inversor no está devolviendo una lectura válida.')
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW)  # apagar el rele
    sys.exit(666) # termina el programa
    

f_list=texto.text.split(" ")
nivel_baterias = (int)(f_list[20])
print("Carga de las baterías: ",nivel_baterias)


# Actuamos sobre el rele si el nivel supera el 99%
if nivel_baterias > nivel_para_encendido:
    print('Encendemos el relé.')
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # encender el rele
else:
    print('Apagamos el relé.')
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW)  # apagar el rele

