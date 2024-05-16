import subprocess
import os


# Load environment variables
load_dotenv()

# Configuration constants
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def start_backend():
    os.chdir(os.path.dirname(__file__))
    subprocess.run(["uvicorn", "backend.app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"])

def start_frontend():
    os.chdir(os.path.dirname(__file__))
    subprocess.run(["python", "-m", "frontend.main"])

if __name__ == "__main__":
    from multiprocessing import Process

    backend_process = Process(target=start_backend)
    backend_process.start()

    frontend_process = Process(target=start_frontend)
    frontend_process.start()

    backend_process.join()
    frontend_process.join()
