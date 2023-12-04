import subprocess
import sys
import os

def main() -> None:
    completed_process = subprocess.run(
        [os.path.join(os.path.dirname(__file__), "altjust"), *sys.argv[1:]]
    )
    sys.exit(completed_process.returncode)

if __name__ == "__main__":
    main()
