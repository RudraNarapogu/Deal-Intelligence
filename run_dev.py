import subprocess
import time
import sys
import os

print("=" * 60)
print("🚀 Starting Deal Intelligence Sales Agent System")
print("=" * 60)

# 1. Start FastAPI Backend
print("[1/2] Launching FastAPI Backend on http://localhost:8000...")
backend_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "backend.main:app", "--port", "8000", "--reload"],
    cwd=os.path.dirname(os.path.abspath(__file__))
)

time.sleep(2)

# 2. Start React Frontend
print("[2/2] Launching React Vite Frontend on http://localhost:5173...")
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
frontend_process = subprocess.Popen(
    ["npm.cmd" if os.name == "nt" else "npm", "run", "dev"],
    cwd=frontend_dir
)

print("\n" + "=" * 60)
print("✅ Application is running!")
print("   • Backend API: http://localhost:8000")
print("   • API Interactive Docs: http://localhost:8000/docs")
print("   • React Dashboard: http://localhost:5173")
print("=" * 60 + "\n")

try:
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    print("\nShutting down processes...")
    backend_process.terminate()
    frontend_process.terminate()
