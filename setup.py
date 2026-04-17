import sys
from cx_Freeze import setup, Executable

# Options for building the macOS bundle
build_exe_options = {
    "packages": ["os","wx"],  # List required packages here
    "excludes": ["tkinter"], # Exclude unnecessary modules
}

# Specific macOS bundle options
bdist_mac_options = {
    "bundle_name": "JereIDE", # Name of the .app file
    "iconfile": "BetaAppIcon.icns", # Path to your .icns icon
}

setup(
    name="MyCoolApp",
    version="1.0",
    description="A description of my app",
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
    },
    executables=[Executable("main.py", base=None)], # "main.py" is your entry script
)
