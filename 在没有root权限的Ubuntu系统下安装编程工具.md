由于某些学校装的是 Ubuntu 系统（或者魔改版），还设了一个离谱密码。这导致一些同学想要学术，但是无法实现。因此，就有了这篇文章 -- 在没有 root 权限的 Ubuntu 系统下安装编程工具。

## 安装python/python库

很多学校的 python 环境十分老旧（python 3.10以下），还是阉割版（没有pip）。这就导致很多 python 项目无法正常运行。于是我们需要安装 conda 环境。

### step1 安装 conda 环境

`Ctrl` + `Alt` + `T` 打开终端。

终端通常应该是这样的 : `user@JF5003:~$`

在里面输入以下命令，粘贴需要 `Ctrl` + `Alt` + `C`。

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
```

待进度条走完再次出现 `user@JF5003:~$` 再次输入下列命令：

```bash
bash Miniconda3-latest-Linux-aarch64.sh
```

安装时需要按照下列步骤：

1.遇到 `Please, press ENTER to continue` 的时候按下回车键。

2.出现 `--More--` 的时候持续按回车键。

3.出现 `Do you accept the license terms? [yes|no]` 的时候输入 `yes`。

4.出现 `[/home/user/miniconda3] >>> ` 的时候按下回车键。

等到再次出现 `user@JF5003:~$` 就说明安装成功了。

### step2 激活 conda 环境

安装完成后，继续在终端里输入：

```bash
~/miniconda3/bin/conda init
source ~/.bashrc
```

如果终端变成了 `(base) user@JF5003:~$` 就说明环境创建成功了！

这样，python 环境就安装成功了！

在环境里面，python版本是很高的。且 `pip install` 也可以使用了。

## 安装 node.js

有些同学会写出高端的 js 代码，这是后就需要 Node.js 进行编译。

**前置：需要同样安装 conda 环境！**

### step1 确认环境

安装前请确认你的终端前面有 `(base)` 字样。

### step2 安装

1.添加频道

```bash
conda config --add channels conda-forge
```

2.执行安装

```
conda install nodejs
```

安装时，如果有选择，请选择 `a` (accept)。如果有 Y/N 请选择 Y。

这样，完整Node.js就安装完成了。

## 安装 Git

有些同学经常维护 Github，所以 Git 是必不可少的。然而在 Conda 环境中安装 Git 非常简单，只需要一条命令：

```bash
conda install git
```

安装完成后测试:

```bash
git --version
``` 

如果能看到类似 `git version 2.x.x` 的输出版本号，说明安装成功了。
