#!/bin/bash

# Colores para el output (opcional, para mejor visualización)
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # Sin color

echo -e "${GREEN}Iniciando servicios...${NC}"

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

# 2. Iniciar el servidor de FastAPI
echo -e "${GREEN}Iniciando servidor FastAPI...${NC}"
uvicorn main:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!
echo -e "${GREEN}FastAPI corriendo en PID $FASTAPI_PID${NC}"

# 3. Iniciar el servidor de Prefect
echo -e "${GREEN}Iniciando servidor de Prefect...${NC}"
prefect server start &
PREFECT_SERVER_PID=$!
echo -e "${GREEN}Prefect Server corriendo en PID $PREFECT_SERVER_PID${NC}"

# 4. Esperar 5 segundos antes de iniciar el worker de Prefect
echo -e "${GREEN}Esperando 5 segundos antes de iniciar el worker de Prefect...${NC}"
sleep 5

# 5. Iniciar el worker de Prefect
echo -e "${GREEN}Iniciando worker de Prefect...${NC}"
prefect worker start --pool 'my-work-pool' &
PREFECT_WORKER_PID=$!
echo -e "${GREEN}Prefect Worker corriendo en PID $PREFECT_WORKER_PID${NC}"

# Mostrar información de los procesos
echo -e "${GREEN}Todos los servicios han sido iniciados.${NC}"
echo -e "FastAPI corriendo en PID: $FASTAPI_PID"
echo -e "Prefect Server corriendo en PID: $PREFECT_SERVER_PID"
echo -e "Prefect Worker corriendo en PID: $PREFECT_WORKER_PID"

# Mantener el script corriendo para monitorear procesos
echo -e "${GREEN}Presiona Ctrl+C para detener este script. Los procesos seguirán corriendo en segundo plano.${NC}"
wait
