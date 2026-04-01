#!/usr/bin/env python3
"""
Build script for converting tool_vip.py to EarnApp-Checker.exe
Requires: pyinstaller and requests
"""

import os
import subprocess
import sys

def build_exe():
    print("=" * 60)
    print("🔧 EarnApp Checker - Build .EXE")
    print("=" * 60)
    
    # Check if tool_vip.py exists
    if not os.path.exists("tool_vip.py"):
        print("❌ Error: tool_vip.py not found in current directory")
        sys.exit(1)
    
    # Install dependencies
    print("
📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pyinstaller", "requests"], check=True)
    
    # Build EXE
    print("
🔨 Building EXE file...")
    cmd = [
        sys.executable,
        "-m", "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "EarnApp-Checker",
        "--distpath", "./dist",
        "--specpath", "./build",
        "--buildpath", "./build",
        "tool_vip.py"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        exe_path = "./dist/EarnApp-Checker.exe"
        if os.path.exists(exe_path):
            print("
" + "=" * 60)
            print("✅ Build successful!")
            print(f"📁 File location: {os.path.abspath(exe_path)}")
            print("=" * 60)
            return True
    
    print("
❌ Build failed!")
    return False

if __name__ == "__main__":
    build_exe()