from dotenv import load_dotenv
from pathlib import Path

from util import monitor

if __name__ == "__main__":
    m1 = monitor.Monitor()
    load_dotenv(dotenv_path = Path('.env'))
    m1.run_health_check()

