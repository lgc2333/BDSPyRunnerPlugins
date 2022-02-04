import os


def install(pkg_name: str):
    """
    通过pip使用清华大学PyPI镜像站在插件目录下安装第三方Python软件包

    :param pkg_name: 软件包名称
    """
    command = 'pip3.7'
    if not os.system(command) == 0:
        command = 'pip'
        if not os.system(command) == 0:
            raise FileExistsError('pip3.7/pip not found')

    command += f' install "{pkg_name}" -i https://pypi.tuna.tsinghua.edu.cn/simple'
    command += f' -t {os.path.split(__file__)[0]}'

    ret = os.system(command)
    if not ret == 0:
        raise OSError((ret, 'install package failed'))


__version__ = '1.0.0'
