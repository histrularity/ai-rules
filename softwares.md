---
description: 强制加载
---

# 公共目录 /share/develop/softwares 说明

该目录主要用于存放无依赖、在任何x86 linux都能运行的程序, 包括cli工具、python包、python发布包(tar.gz)等。只要执行了`source ~/.bashrc`, 基本都会自动加载。

它下面有几个目录, bin (cli工具), py_packages (python已安装的包, 类似于site-packages), releases (python发布包, tar.gz), musl (musl编译器), cosmocc (cosmopolitan libc编译器)。具体查看该目录下的README.md。如果要看有哪些工具, 可以直接ls对应目录。

注意 /share/develop/softwares 可能因为容器挂载在不同路径, 如果有问题和我确认。

该目录是只读的, 没有写入权限, 即使是root也不行。