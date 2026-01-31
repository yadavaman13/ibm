#!/usr/bin/env python
"""Quick launcher for web application"""
import sys
import subprocess
from pathlib import Path

if __name__ == "__main__":
    # Get paths
    project_root = Path(__file__).parent
    streamlit_path = Path(sys.executable).parent / "streamlit.exe"
    if not streamlit_path.exists():
        streamlit_path = Path(sys.executable).parent / "streamlit"  # Unix
    
    app_path = project_root / "src" / "ui" / "streamlit_app.py"
    
    # Run streamlit with project root as working directory
    subprocess.run([str(streamlit_path), "run", str(app_path)], cwd=str(project_root))
