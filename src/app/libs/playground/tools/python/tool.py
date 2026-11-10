import docker
from langchain_core.tools import tool

client = docker.from_env()


@tool
def execute_python(code: str) -> str:
    """
    A Python shell. Use this to execute python commands.
    Args:
        code: Input should be a valid python command.
            If you want to see the output of a value,
            you should print it out with `print(...)`.

    Returns:
    """
    client.images.pull("python:latest")
    container = client.containers.run("python:latest", ["python", "-u", "-c", code], detach=True)
    try:
        container.wait()
        output = container.logs()
        return output.decode("utf-8")
    finally:
        container.remove(force=True)
