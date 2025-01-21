# **Guía Paso a Paso para Ejecutar Hipo en una Instancia EC2**

Esta guía te llevará a través del proceso de configuración y ejecución del proyecto Hipo en una instancia Amazon Linux 2 EC2. Incluye desde la instalación de dependencias hasta el despliegue de flujos de trabajo con Prefect.

---

## **1. Actualiza tu Sistema**
Comienza actualizando todos los paquetes del sistema:

```bash
sudo yum update -y
```

---

## **2. Instala pyenv**

### **Paso 1: Instala Dependencias**
Instala las dependencias necesarias para `pyenv`:

```bash
sudo yum groupinstall -y "Development Tools"
sudo yum install -y gcc zlib zlib-devel bzip2 bzip2-devel readline readline-devel \
sqlite sqlite-devel openssl openssl-devel libffi-devel xz xz-devel git
```

### **Paso 2: Instala pyenv**
Ejecuta el instalador oficial de `pyenv`:

```bash
curl -fsSL https://pyenv.run | bash
```

Si ya tienes una instalación previa de `pyenv`, puedes eliminarla o renombrarla:

```bash
rm -rf ~/.pyenv
# O
mv ~/.pyenv ~/.pyenv_backup
```

### **Paso 3: Configura pyenv**
Agrega las siguientes líneas a tu archivo `~/.bashrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"
```

Aplica los cambios:

```bash
source ~/.bashrc
```

### **Paso 4: Instala Python 3.12.7**
Instala y configura Python 3.12.7 como la versión global:

```bash
pyenv install 3.12.7
pyenv global 3.12.7
pyenv rehash
```

Verifica la instalación:

```bash
python --version
```

Deberías ver `Python 3.12.7`.

---

## **3. Instala y Habilita Docker**

### **Paso 1: Instala Docker**
Instala Docker usando el gestor de paquetes `yum`:

```bash
sudo yum install -y docker
```

### **Paso 2: Inicia y Habilita el Servicio de Docker**
Inicia el servicio de Docker y configúralo para que se inicie automáticamente al arrancar:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### **Paso 3: Agrega tu Usuario al Grupo `docker`**
Agrega tu usuario al grupo `docker` para ejecutar Docker sin `sudo`:

```bash
sudo usermod -aG docker $USER
```

**Importante:** Cierra y vuelve a iniciar sesión, o refresca tu sesión con:

```bash
newgrp docker
```

### **Paso 4: Verifica la Instalación de Docker**
Revisa la versión de Docker:

```bash
docker --version
```

Ejecuta un contenedor de prueba para asegurarte de que Docker funciona:

```bash
docker run hello-world
```

---

## **4. Clona el Repositorio de Hipo**

### **Paso 1: Crea un Directorio de Proyecto**
Crea un directorio para el proyecto Hipo y navega a él:

```bash
mkdir hypo_project
cd hypo_project
```

### **Paso 2: Clona el Repositorio**
Clona el repositorio de Hipo:

```bash
git clone https://github.com/breatheco-de/hipo.git
```

---

## **5. Configura un Entorno Virtual e Instala Requisitos**

### **Paso 1: Navega al Directorio del Proyecto**
Muévete al directorio `hipo` (el repositorio clonado):

```bash
cd hipo
```

### **Paso 2: Crea un Entorno Virtual**
Usa `python` (instalado con `pyenv`) para crear un entorno virtual:

```bash
python -m venv venv
```

### **Paso 3: Activa el Entorno Virtual**
Activa el entorno virtual:

```bash
source venv/bin/activate
```

### **Paso 4: Instala las Dependencias**
Instala las dependencias requeridas desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## **6. Otorga Permisos de Ejecución a los Scripts**

El proyecto Hipo incluye scripts que necesitan permisos de ejecución.

### **Paso 1: Otorga Permisos**
Ejecuta el siguiente comando para hacer que los scripts sean ejecutables:

```bash
chmod +x check_redis_container.sh start.sh stop.sh
```

### **Paso 2: Verifica los Permisos**
Confirma los permisos:

```bash
ls -l
```

Deberías ver permisos `rwx` (ejecutables) para los scripts.

---

## **7. Usa el Script para Crear y Verificar el Contenedor de Redis**

El script `check_redis_container.sh` verifica si el contenedor de Redis está en ejecución y lo crea si es necesario.

### **Paso 1: Ejecuta el Script**
Ejecuta el script:

```bash
./check_redis_container.sh
```

### **Qué Hace el Script**
- Si el contenedor de Redis ya está corriendo, confirmará su estado.
- Si el contenedor de Redis no existe, el script lo creará usando Docker.

### **Paso 2: Verifica el Contenedor de Redis**
Después de ejecutar el script, puedes verificar manualmente que el contenedor de Redis esté en ejecución:

```bash
docker ps
```

Deberías ver el contenedor de Redis en la lista de contenedores en ejecución.

---

## **8. Copia `.env.example` a `.env`**

El proyecto requiere un archivo `.env` para la configuración.

### **Paso 1: Copia el Archivo de Ejemplo**
Crea una copia de `.env.example` con el nombre `.env`:

```bash
cp .env.example .env
```

### **Paso 2: Edita el Archivo `.env` (Opcional)**
Si es necesario, abre el archivo `.env` para modificar las variables de entorno específicas:

```bash
nano .env
```

Realiza los cambios necesarios, como credenciales de base de datos o claves de API.

Guarda y cierra el archivo:
- En `nano`, presiona `CTRL+O` para guardar y `CTRL+X` para salir.

---

## **9. Inicia el Programa Hipo**

El proyecto Hipo se inicia usando el script `start.sh`, que ejecuta el programa en segundo plano.

### **Paso 1: Inicia el Programa**
Ejecuta el script `start.sh`:

```bash
./start.sh
```

### **Qué Hace el Script `start.sh`**
- Usa `nohup` para ejecutar los procesos en segundo plano.
- Crea un archivo llamado `pids.txt`, que contiene los **IDs de los procesos (PIDs)** en ejecución.

### **Paso 2: Verifica que el Programa Está Corriendo**
Revisa el archivo `pids.txt` para ver los IDs de los procesos en ejecución:

```bash
cat pids.txt
```

También puedes usar el comando `ps` para confirmar que los procesos están corriendo:

```bash
ps -p $(cat pids.txt)
```

---

## **10. Detén el Programa Hipo**

Para detener el programa, usa el script `stop.sh`:

```bash
./stop.sh
```

### **Qué Hace el Script `stop.sh`**
- Lee el archivo `pids.txt` para obtener los IDs de los procesos.
- Termina los procesos en ejecución y elimina el archivo `pids.txt`.

---

## **11. Despliega los Flujos de Trabajo con Prefect**

El proyecto Hipo usa Prefect para la orquestación de flujos de trabajo.

### **Paso 1: Abre una Nueva Terminal**
Abre una nueva terminal y conecta a tu instancia EC2 vía SSH:

```bash
ssh -i YOUR_KEY.pem ec2-user@YOUR_EC2_IP
```

### **Paso 2: Navega al Directorio del Proyecto**
Navega al directorio `hipo`:

```bash
cd hypo_project/hipo
```

### **Paso 3: Activa el Entorno Virtual**
Activa el entorno virtual:

```bash
source venv/bin/activate
```

### **Paso 4: Despliega los Flujos de Trabajo**
Ejecuta el siguiente comando para desplegar los flujos de trabajo:

```bash
prefect deploy
```

### **Opcional: Ejecuta Despliegues Específicos**
Lista los despliegues disponibles:

```bash
prefect deployment ls
```

Ejecuta un despliegue específico:

```bash
prefect deployment run <deployment_name>
```

Reemplaza `<deployment_name>` con el nombre del despliegue que deseas ejecutar.

---

## **12. Verifica el Despliegue**
Revisa la salida en la terminal para confirmar que el despliegue fue exitoso. Si usas Prefect Cloud o un servidor Prefect, ingresa a la interfaz de usuario para verificar los flujos registrados.

---

