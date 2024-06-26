import serial
import pygame
import time
import re

# Inicializa la conexión serial con el Arduino
arduino = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # Espera a que se establezca la conexión
# Inicializa pygame mixer
pygame.mixer.init()
# Carga el archivo MP3
pygame.mixer.music.load("saludo.mp3")
# Umbral de proximidad en centímetros
threshold_cm = 50

try:
    while True:
        # Lee la línea de datos del puerto serial
        data = arduino.readline().decode('utf-8').strip()
        
        # Buscar el valor de distancia en la cadena
        match = re.search(r"Distancia: (\d+\.\d+) cm", data)
        if match:
            distance = float(match.group(1))
            print(f"Distancia: {distance} cm")
            
            # Si la distancia es menor al umbral, reproduce el sonido
            if distance < threshold_cm:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
                    
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Interrupción por teclado")
finally:
    # Cierra la conexión serial y detiene la música
    arduino.close()
    pygame.mixer.music.stop()
