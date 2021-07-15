from cx_Freeze import setup, Executable

build_exe_options = {
	'packages': ["importlib.metadata", "nltk_data", "spacy", "en_core_web_sm", "tkinter", "pathlib", "webbrowser"]
}

setup(name = "RQT" ,
   version = "0.1" ,
   description = "" ,
   options = {"build_exe": build_exe_options},
   executables = [Executable("BatchValidationClient.py")])
