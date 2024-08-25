# python3で動作するスクリプト
# Description: AMSで使っているモジュールのバージョンを確認するためのスクリプト
# Pythonのバージョンやboto3のバージョンを確認するためのモジュール
import sys
import platform
import pkg_resources

# AMSで使っているモジュール
import boto3

if sys.version_info.major == 3 and sys.version_info.minor == 9:
    print("Python3x:{0}".format(platform.python_version()))

for dist in pkg_resources.working_set:
    print(f"{dist.project_name}=={dist.version}")

# boto3 version check
if boto3.__version__ == '1.17.112':
    print(f"boto3 version: {boto3.__version__} OK")
