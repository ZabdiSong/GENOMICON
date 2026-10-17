# GENOMICON 上传与运行说明

## 这次收到了什么

已完整阅读两份附件：`Genomicon_final(2).py`（694 行）和 `Genomicon1(1).1`（216 行）。第二份虽然扩展名为 `.1`，内容也是 Python 源码，属于较早版本。两份附件都不是 ZIP，里面没有图片素材。

本次以 final 版本为基础整理为 `genomicon.py`。原附件没有被覆盖。

## 改了什么

- 增加分区注释和函数说明，便于阅读代码。
- 修正部分英文拼写、语法和操作说明，例如 Punnett 的拼写，以及基因剪切后应点哪个按钮。
- 保留游戏布局、颜色、图片大小、计算方式、关卡顺序、输入判定和状态变化。
- 添加启动入口、素材检查脚本和 README，方便放入 GitHub 后供别人下载。

没有重画素材、增加新关卡或更改游戏规则。每项文字调整见 `TEXT_CHANGES.md`。

## 还需要你提供的文件

请提供包含原版 **`assets/` 文件夹**的 ZIP，并保留内部 `gallery/` 和 `images/` 子文件夹。程序共引用 66 张图片；完整清单在 `ASSETS.md`。如果 ZIP 中还包含海报、论文或其他材料，也可以一起提供，之后再按实际内容整理。

当前包可以上传源码，但补齐图片之前，不能作为完整可玩的游戏包。

## 在自己的电脑运行

1. 解压本文件包。
2. 把原版 `assets/` 文件夹内容放入包内的 `assets/`，不要多套一层同名文件夹。
3. 在项目文件夹打开终端，依次运行：

```sh
python -m pip install -r requirements.txt
python check_assets.py
python run.py
```

如果电脑使用 `python3` 命令，把上面三处 `python` 换成 `python3`。

## 上传 GitHub

建议仓库名：`GENOMICON`。

如果通过 GitHub 网页上传，先在电脑解压本包，再把项目文件夹内的文件和文件夹上传到仓库根目录，包括 `genomicon.py`、`run.py`、`check_assets.py`、`requirements.txt`、`README.md`、`docs/` 和补全后的 `assets/`。

只把 ZIP 上传到仓库会让别人需要先下载和解压，GitHub 也不会自动把 ZIP 中的 README 展示为仓库首页。直接上传解压后的项目结构更便于查看。

申请材料可以放仓库链接。这个版本是 **Python/Pygame 桌面程序**；上传源码不会自动变成可以在浏览器里点击游玩的网页。仓库访问者可以阅读 README、查看源码，并下载到电脑运行。

当前没有创建或推送任何远程仓库。
