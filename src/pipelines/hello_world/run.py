from prefect import task, flow

@task
def mi_tarea():
    print("¡Tarea ejecutada!")

@flow
def hello_world():
    mi_tarea()

if __name__ == "__main__":
    hello_world()
