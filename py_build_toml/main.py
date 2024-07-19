import root_module
from sub import module


def sub_func():
    print(module.func())


def root_func():
    print(root_module.func())


if __name__ == "__main__":
    sub_func()
    root_func()
