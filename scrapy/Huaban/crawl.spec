# -*- mode: python -*-

block_cipher = None


a = Analysis(['crawl.py'],
             pathex=['e:\\github\\hsuna\\python-test\\scrapy\\Huaban'],
             binaries=[],
             datas=[(".\\scrapy.cfg",".")],
             hiddenimports=["Huaban.items","Huaban.middlewares",'Huaban.pipelines','Huaban.settings','Huaban.spiders'],
             hookspath=[".\\hooks\\"],
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
          [],
          exclude_binaries=True,
          name='crawl',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='crawl')
