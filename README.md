# Nodo Remoto para el Monitoreo de Temperatura y Humedad en Colmenas de Abejas Yateí
Este repositorio contiene el código fuente de un proyecto de IoT desarrollado para la asignatura "Internet de las Cosas, Sensores y Redes" de la carrera Ingeniería en Computación (UNaM - FI Oberá, Misiones, Argentina). El proyecto incluye un nodo remoto con ESP32 que mide temperatura y humedad en una colmena de abejas Yateí (Tetragonisca angustula) usando un sensor DHT22. Los datos se envían a un broker MQTT por WiFi y se almacenan en un servidor Raspberry Pi.

## Tips para comenzar
Debes crear un módulo llamado `settings.py` en el cual cargar las credenciales del WiFi y el Broker MQTT que usarás para enviar y almacenar los datos en tu servidor. Estas credenciales son importadas en el módulo `mqtt_local.py` dentro del directorio `lib`. Los nombres de las credenciales son: `SSID`, `PASS`, `BROKER`, `MQTT_PORT`, `MQTT_USER`, y `MQTT_PASS`
