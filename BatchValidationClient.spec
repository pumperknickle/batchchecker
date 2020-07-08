# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['BatchValidationClient.py'],
             pathex=['/Users/jbao/Validator'],
             binaries=[],
             datas=[],
             hiddenimports=['srsly.msgpack.util', 'cymem.cymem', 'thinc.linalg', 'murmurhash.mrmr', 'cytoolz.utils', 'cytoolz._signatures', 'spacy.strings', 'spacy.morphology', 'spacy.lexeme', 'spacy.tokens', 'spacy.gold', 'spacy.tokens.underscore', 'spacy.parts_of_speech', 'dill', 'spacy.tokens.printers', 'spacy.tokens._retokenize', 'spacy.syntax', 'spacy.syntax.stateclass', 'spacy.syntax.transition_system', 'spacy.syntax.nonproj', 'spacy.syntax.nn_parser', 'spacy.syntax.arc_eager', 'thinc.extra.search', 'spacy.syntax._beam_utils', 'spacy.syntax.ner', 'thinc.neural._classes.difference', 'preshed.maps'],
             hookspath=['.'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='BatchValidationClient',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='BatchValidationClient.app',
             icon=None,
             bundle_identifier=None)
