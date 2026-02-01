#!/usr/bin/env python
"""Quick launcher for new FasalMitra multi-page app"""
import sys
import subprocess
from pathlib import Path

if __name__ == "__main__":
    # Get paths
    project_root = Path(__file__).parent
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    app_path = project_root / "src" / "ui" / "fasal_mitra_app.py"
    
    # Use venv python if available, otherwise system python
    python_exe = str(venv_python) if venv_python.exists() else sys.executable
    
    # Run streamlit
    subprocess.run([python_exe, "-m", "streamlit", "run", str(app_path)], cwd=str(project_root))
