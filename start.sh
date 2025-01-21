#!/bin/bash

# Colores para el output (opcional, para mejor visualización)
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # Sin color

echo -e "${GREEN}Iniciando servicios...${NC}"

# Archivo para guardar los PIDs
PID_FILE="pids.txt"
echo -e "${GREEN}Guardando PIDs en el archivo: $PID_FILE${NC}"
> $PID_FILE  # Limpiar el archivo (sobrescribir)

# 1. Detectar el sistema operativo y activar el entorno virtual
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${GREEN}Detectado sistema operativo: Linux${NC}"
    echo -e "${GREEN}Activando entorno virtual...${NC}"
    source venv/bin/activate
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo -e "${GREEN}Detectado sistema operativo: Windows${NC}"
    echo -e "${GREEN}Activando entorno virtual...${NC}"
    source venv/Scripts/activate
else
    echo -e "${RED}Sistema operativo no soportado para este script.${NC}"
    exit 1
fi

# Verificar si el entorno virtual fue activado correctamente
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${RED}Error: No se pudo activar el entorno virtual.${NC}"
    exit 1
else
    echo -e "${GREEN}Entorno virtual activado: $VIRTUAL_ENV${NC}"
fi

# 1. Fix directory
echo -e "${GREEN}Fixing directory...${NC}"
python src/utils/fix_directory.py

# 2. Configurar PREFECT_API_URL
echo -e "${GREEN}Configurando PREFECT_API_URL...${NC}"
export PREFECT_API_URL="http://127.0.0.1:8555"
echo -e "${GREEN}PREFECT_API_URL configurado como: $PREFECT_API_URL${NC}"

# 3. Iniciar el servidor de FastAPI con nohup
echo -e "${GREEN}Iniciando servidor FastAPI...${NC}"
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 &
FASTAPI_PID=$!
echo $FASTAPI_PID >> $PID_FILE
echo -e "${GREEN}FastAPI corriendo en PID $FASTAPI_PID${NC}"
echo -e "${GREEN}Puedes ver el servidor en: http://localhost:8000${NC}"

# 4. Iniciar el servidor de Prefect con nohup
echo -e "${GREEN}Iniciando servidor de Prefect...${NC}"
nohup prefect server start --host 0.0.0.0 > prefect_server.log 2>&1 &
PREFECT_SERVER_PID=$!
echo $PREFECT_SERVER_PID >> $PID_FILE
echo -e "${GREEN}Prefect Server corriendo en PID $PREFECT_SERVER_PID${NC}"
echo -e "${GREEN}Puedes ver el servidor en: http://localhost:4200${NC}"

# 5. Esperar 5 segundos antes de iniciar el worker de Prefect
echo -e "${GREEN}Esperando 5 segundos antes de iniciar el worker de Prefect...${NC}"
sleep 5

# 6. Iniciar el worker de Prefect con nohup
echo -e "${GREEN}Iniciando worker de Prefect...${NC}"
nohup prefect worker start --pool 'my-work-pool' > prefect_worker.log 2>&1 &
PREFECT_WORKER_PID=$!
echo $PREFECT_WORKER_PID >> $PID_FILE
echo -e "${GREEN}Prefect Worker corriendo en PID $PREFECT_WORKER_PID${NC}"

# Mostrar información de los procesos
echo -e "${GREEN}Todos los servicios han sido iniciados.${NC}"
echo -e "FastAPI corriendo en PID: $FASTAPI_PID (log: fastapi.log)"
echo -e "Prefect Server corriendo en PID: $PREFECT_SERVER_PID (log: prefect_server.log)"
echo -e "Prefect Worker corriendo en PID: $PREFECT_WORKER_PID (log: prefect_worker.log)"
echo -e "${GREEN}Los PIDs han sido guardados en el archivo: $PID_FILE${NC}"

# Mantener el script corriendo para monitorear procesos
echo -e "${GREEN}Presiona Ctrl+C para detener este script. Los procesos seguirán corriendo en segundo plano.${NC}"
wait
clear
