import sys
import platform

import boto3
import pkg_resources

if sys.version_info.major == 2 and sys.version_info.minor == 7:
    print("Python2x:{0}".format(platform.python_version()))

    for dist in pkg_resources.working_set:
        print("{0}=={1}".format(dist.project_name, dist.version))

    # boto3 version check
    if boto3.__version__ == '1.17.112':
        print("boto3 version:{0} {1}".format(boto3.__version__, "OK"))
