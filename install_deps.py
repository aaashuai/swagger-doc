import toml
import subprocess

try:
    # 读取 pyproject.toml 文件
    pyproject = toml.load('pyproject.toml')

    # 获取 dependencies 列表
    dependencies = pyproject.get('project', {}).get('dependencies', [])
    if not dependencies:
        print("No dependencies found in pyproject.toml.")
    else:
        # 安装依赖
        for dep in dependencies:
            subprocess.check_call(['pip', 'install', dep])
        print("Dependencies installed successfully.")
except FileNotFoundError:
    print("pyproject.toml file not found.")
except Exception as e:
    print(f"An error occurred: {e}")