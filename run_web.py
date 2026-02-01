#!/usr/bin/env python
"""Quick launcher for web application"""
import sys
import subprocess
import os
from pathlib import Path

if __name__ == "__main__":
    # Get paths
    project_root = Path(__file__).parent
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    app_path = project_root / "src" / "ui" / "streamlit_app.py"
    
    # Use venv python if available, otherwise system python
    python_exe = str(venv_python) if venv_python.exists() else sys.executable
    
    # Run streamlit
    subprocess.run([python_exe, "-m", "streamlit", "run", str(app_path)], cwd=str(project_root))
