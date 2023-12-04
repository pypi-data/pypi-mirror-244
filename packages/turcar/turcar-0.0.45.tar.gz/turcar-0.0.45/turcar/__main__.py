from turcar import launch, report_time
import os
import requests

from turcar.check_for_updates import CheackUpdates
import platform

# 获取当前操作系统
current_os = platform.system()
print(current_os)
report_time("Before launch")
response = requests.get('https://pypi.org/pypi/turcar/json')
if response.status_code == 200:
    data = response.json()
    # 获取项目最新版本
    version = data["info"]["version"]
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 指定要获取内容的文件名
    file_name = "VERSION"
    # 拼接文件路径
    file_path = os.path.join(current_dir, file_name)
    # 空校验
    if os.path.exists(file_path):
        # 打开文件并读取内容
        with open(file_path, 'r') as file:
            content = file.read()
            # print(f"File: {file_name}")
            print(f"VERSION: {content}")
            if version != content:
                # if current_os == "Windows":
                #     pass
                # else:  # 默认为Ubuntu或其他Linux发行版
                    cheack = CheackUpdates()
                    cheack.cheack_version(version)

launch()
