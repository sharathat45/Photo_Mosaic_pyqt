# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['path\\to\\project_dir'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
             
a.datas += [('images\\favicon.ico','path\\to\\project_dir\\images\\favicon.ico',"DATA")]
a.datas += [('images\\camera-solid.png','path\\to\\project_dir\\images\\camera-solid.png',"DATA")]
a.datas += [('images\\check-solid.png','path\\to\\project_dir\\images\\check-solid.png',"DATA")]
a.datas += [('images\\down-arrow.png','path\\to\\project_dir\\images\\down-arrow.png',"DATA")]
a.datas += [('images\\thumb_1.jpg','path\\to\\project_dir\\images\\thumb_1.jpg',"DATA")]
a.datas += [('images\\thumb_2.jpg','path\\to\\project_dir\\images\\thumb_2.jpg',"DATA")]
a.datas += [('images\\thumb_3.jpg','path\\to\\project_dir\\images\\thumb_3.jpg',"DATA")]
a.datas += [('images\\thumb_4.jpg','path\\to\\project_dir\\images\\thumb_4.jpg',"DATA")]
a.datas += [('fonts\\Anurati-Regular.otf','path\\to\\project_dir\\fonts\\Anurati-Regular.otf',"DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Photo Mosaic',
          icon = 'images\\favicon.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Photo Mosaic')
