import configparser
import subprocess

# 解析 setup.cfg 文件
config = configparser.ConfigParser()
config.read('setup.cfg')

try:
    # 获取 install_requires 部分的依赖
    dependencies = config.get('options', 'install_requires').strip().splitlines()
    dependencies = [dep.strip() for dep in dependencies if dep.strip()]

    # 安装依赖
    for dep in dependencies:
        subprocess.check_call(['pip', 'install', dep])
    print("Dependencies installed successfully.")
except configparser.NoOptionError:
    print("No 'install_requires' section found in setup.cfg.")
except Exception as e:
    print(f"An error occurred: {e}")