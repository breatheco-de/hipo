# **Running Hipo in an EC2 Instance: Step-by-Step Guide**

This guide will walk you through setting up and running the Hipo project on an Amazon Linux 2 EC2 instance. It covers everything from installing dependencies to deploying workflows with Prefect.

---

## **1. Update Your System**
Start by updating all system packages:

```bash
sudo yum update -y
```

---

## **2. Install pyenv**

### **Step 1: Install Dependencies**
Install the necessary dependencies for `pyenv`:

```bash
sudo yum groupinstall -y "Development Tools"
sudo yum install -y gcc zlib zlib-devel bzip2 bzip2-devel readline readline-devel \
sqlite sqlite-devel openssl openssl-devel libffi-devel xz xz-devel git
```

### **Step 2: Install pyenv**
Run the official `pyenv` installer:

```bash
curl -fsSL https://pyenv.run | bash
```

If you already have a previous `pyenv` installation, you may need to remove or rename it:

```bash
rm -rf ~/.pyenv
# OR
mv ~/.pyenv ~/.pyenv_backup
```

### **Step 3: Configure pyenv**
Add the following lines to your `~/.bashrc` file:

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"
```

Apply the changes:

```bash
source ~/.bashrc
```

### **Step 4: Install Python 3.12.7**
Install and set Python 3.12.7 as the global version:

```bash
pyenv install 3.12.7
pyenv global 3.12.7
pyenv rehash
```

Verify the installation:

```bash
python --version
```

You should see `Python 3.12.7`.

---

## **3. Install and Enable Docker**

### **Step 1: Install Docker**
Install Docker using the `yum` package manager:

```bash
sudo yum install -y docker
```

### **Step 2: Start and Enable Docker Service**
Start the Docker service and configure it to start automatically on boot:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### **Step 3: Add Your User to the `docker` Group**
Add your user to the `docker` group to run Docker without `sudo`:

```bash
sudo usermod -aG docker $USER
```

**Important:** Log out and log back in, or refresh your session with:

```bash
newgrp docker
```

### **Step 4: Verify Docker Installation**
Check the Docker version:

```bash
docker --version
```

Run a test container to ensure Docker is working:

```bash
docker run hello-world
```

---

## **4. Clone the Hipo Repository**

### **Step 1: Create a Project Directory**
Create a directory for the Hipo project and navigate to it:

```bash
mkdir hypo_project
cd hypo_project
```

### **Step 2: Clone the Repository**
Clone the Hipo repository:

```bash
git clone https://github.com/breatheco-de/hipo.git
```

---

## **5. Set Up a Virtual Environment and Install Requirements**

### **Step 1: Navigate to the Project Directory**
Move into the `hipo` directory (the cloned repository):

```bash
cd hipo
```

### **Step 2: Create a Virtual Environment**
Use `python` (installed via `pyenv`) to create a virtual environment:

```bash
python -m venv venv
```

### **Step 3: Activate the Virtual Environment**
Activate the virtual environment:

```bash
source venv/bin/activate
```

### **Step 4: Install Dependencies**
Install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## **6. Grant Execution Permissions to Shell Scripts**

The Hipo project includes shell scripts that need execution permissions.

### **Step 1: Grant Permissions**
Run the following command to make the scripts executable:

```bash
chmod +x check_redis_container.sh start.sh stop.sh
```

### **Step 2: Verify Permissions**
Confirm the permissions:

```bash
ls -l
```

You should see `rwx` (executable) permissions for the scripts.

---

## **7. Use the Script to Create and Check the Redis Container**

The `check_redis_container.sh` script is used to check if the Redis container is running and to create it if necessary.

### **Step 1: Run the Script**
Execute the script:

```bash
./check_redis_container.sh
```

### **What the Script Does**
- If the Redis container is already running, it will confirm its status.
- If the Redis container does not exist, the script will create it using Docker.

### **Step 2: Verify the Redis Container**
After running the script, you can manually verify that the Redis container is running:

```bash
docker ps
```

You should see the Redis container in the list of running containers.

---

## **8. Copy `.env.example` to `.env`**

The project requires a `.env` file for configuration.

### **Step 1: Copy the Example File**
Create a copy of `.env.example` named `.env`:

```bash
cp .env.example .env
```

### **Step 2: Edit the `.env` File (Optional)**
If needed, open the `.env` file to modify specific environment variables:

```bash
nano .env
```

Make any necessary changes, such as database credentials or API keys.

Save and exit the file:
- In `nano`, press `CTRL+O` to save and `CTRL+X` to exit.

---

## **9. Start the Hipo Program**

The Hipo project is started using the `start.sh` script, which runs the program in the background.

### **Step 1: Start the Program**
Run the `start.sh` script:

```bash
./start.sh
```

### **What Happens When You Run `start.sh`**
- The script uses `nohup` to run processes in the background.
- It creates a file named `pids.txt`, which contains the **process IDs (PIDs)** of the background processes.

### **Step 2: Verify the Program is Running**
Check the `pids.txt` file to see the running process IDs:

```bash
cat pids.txt
```

You can also use the `ps` command to confirm the processes are running:

```bash
ps -p $(cat pids.txt)
```

---

## **10. Stop the Hipo Program**

To stop the program, use the `stop.sh` script:

```bash
./stop.sh
```

### **What Happens When You Run `stop.sh`**
- The script reads the `pids.txt` file to get the process IDs.
- It terminates the running processes and removes the `pids.txt` file.

---

## **11. Deploy the Workflows with Prefect**

The Hipo project uses Prefect for workflow orchestration.

### **Step 1: Open a New Terminal**
Open a new terminal and connect to your EC2 instance via SSH:

```bash
ssh -i YOUR_KEY.pem ec2-user@YOUR_EC2_IP
```

### **Step 2: Navigate to the Project Directory**
Navigate to the `hipo` directory:

```bash
cd hypo_project/hipo
```

### **Step 3: Activate the Virtual Environment**
Activate the virtual environment:

```bash
source venv/bin/activate
```

### **Step 4: Deploy Workflows**
Run the following command to deploy the workflows:

```bash
prefect deploy
```

### **Optional: Run Specific Deployments**
List available deployments:

```bash
prefect deployment ls
```

Run a specific deployment:

```bash
prefect deployment run <deployment_name>
```

Replace `<deployment_name>` with the name of the deployment you want to execute.

---

## **12. Verify Deployment**
Check the terminal output for confirmation of successful deployment. If you're using Prefect Cloud or a Prefect server, log in to the Prefect UI to verify the workflows.

---

With these steps, your Hipo project should be fully set up and running on your EC2 instance. Let me know if you need help with any part of this process! 🚀