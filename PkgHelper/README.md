# PkgHelper

Version: 1.0.0

Author: [student_2333](https://github.com/lgc2333)

插件需求
--

- 编写所用PYR版本：1.9.6，理论可用PYR版本：>=1.6.3

- 需要 `pip`（一般安装Python都会自带）

插件介绍
--
_其实是一个非常简单的玩意_

插件通过`pip`使用 清华大学PyPI镜像站 在插件目录下安装第三方Python软件包

当你的PYR插件需要第三方包而用户未安装时，可以很方便地下载

使用方法
--

- 直接安装
  ```python
  pkghelper.install('some-package')
  ```

- 指定版本
  ```python
  pkghelper.install('some-package==1.0.0')
  pkghelper.install('some-package>=1.0.0')
  ```

- 示例
  ```python
  import pkghelper
      
  while True:
      try:
          import requests
      except:
          pkghelper.install('requests')
      else:
          break
  ```

安装方法
--

- 将 `pkghelper.py` 文件放入 `BDS根目录/plugins/py` 文件夹内

更新日志
--

- 2022.2.4 插件发布
