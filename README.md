#Sapo asistente

Estos ficheros sirven para crear un bot de discord que pueda ayudar en la automatización de servidores de minecraft. Avisando a los jugadores cuando se añade o elimina un mod y añadiendo o eliminando esos mods en una carpeta de drive a la que pueden acceder los jugadores.

Para poder usarlo, primero es necesario instalar las dependencias de discord.py y pydrive2. Para ello recomiendo usar pip.
Se instalan de la siguiente forma:
```
pip install PyDrive2
pip install discord.py

```

También será necesario instalar en el servidor de linux el paquete inotify-tools usando el comando:
```
apt-get install inotify-tools
```
Una vez instaladas las dependencias, ejecuta el script crea_archivo_mods para crear el mensaje en discrod que contendrá todos los mods de tu servidor y el fichero que almacenará el nombre de los mods actuales en uso.
Tras eso, ejecutamos:
```
nano /etc/rc.local
```
Y escribimos lo siguiente:
```
screen -dm -S avisos /opt/scripts/monitor_mods.sh
```

Con ello ya tendríamos todo el proceso automatizado. Solo tener en cuenta cambiar las rutas para que coincidan con la estructura de vuestros servidores.