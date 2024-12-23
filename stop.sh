#!/bin/bash

PID_FILE="pids.txt"

if [[ -f "$PID_FILE" ]]; then
    echo "Deteniendo procesos..."
    while read -r pid; do
        echo "Matando proceso con PID: $pid"
        kill $pid
    done < "$PID_FILE"
    echo "Todos los procesos han sido detenidos."
    rm $PID_FILE  # Eliminar el archivo después de detener los procesos
else
    echo "No se encontró el archivo $PID_FILE. No hay procesos para detener."
fi
