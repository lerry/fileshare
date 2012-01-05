from cx_Freeze import setup, Executable

setup(
        name = "SunP2P",
        version = "0.1",
        description = "SunP2P 1.0",
        executables = [Executable("gui.py",base = 'Win32GUI')])