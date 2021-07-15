# HOOK FILE FOR SPACY
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import collect_data_files

# ----------------------------- Quantulum3 -----------------------------
data = collect_all('quantulum3')

datas = data[0]
binaries = data[1]
hiddenimports = data[2]


# ----------------------------- SPACY -----------------------------
data = collect_all('spacy')

datas = data[0]
binaries = data[1]
hiddenimports = data[2]

# ----------------------------- THINC -----------------------------
data = collect_all('thinc')

datas += data[0]
binaries += data[1]
hiddenimports += data[2]

# ----------------------------- CYMEM -----------------------------
data = collect_all('cymem')

datas += data[0]
binaries += data[1]
hiddenimports += data[2]

# ----------------------------- PRESHED -----------------------------
data = collect_all('preshed')

datas += data[0]
binaries += data[1]
hiddenimports += data[2]

# ----------------------------- BLIS -----------------------------

data = collect_all('blis')

datas += collect_data_files("en_core_web_sm")
datas += data[0]
binaries += data[1]
hiddenimports += data[2]


