import PyInstaller.__main__
import os
import shutil

def build():
    """一键打包成单文件可执行程序"""
    # 清理旧构建
    for d in ['dist', 'build']:
        if os.path.exists(d):
            shutil.rmtree(d)
    if os.path.exists('MimoMeter.spec'):
        os.remove('MimoMeter.spec')

    # PyInstaller 参数
    args = [
        'src/__main__.py',           # 入口文件
        '--name=MimoMeter',           # 输出名称
        '--onefile',                  # 单文件
        '--add-data=src/static;static',  # 打包静态文件
        '--paths=src',                # 添加模块搜索路径
        '--hidden-import=proxy',      # 隐式导入
        '--hidden-import=dashboard',
        '--hidden-import=db',
        '--hidden-import=logger',
        '--hidden-import=tray',
        '--clean',
        '--noconfirm',
    ]

    PyInstaller.__main__.run(args)
    print("Build complete: dist/MimoMeter.exe")

if __name__ == '__main__':
    build()
