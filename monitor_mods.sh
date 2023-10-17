#!/bin/sh
while inotifywait -e create -e delete /opt/minecraft/mods; do
  python3 /opt/scripts/Sapo_asistente_avisador.py /opt/minecraft/mods
done
