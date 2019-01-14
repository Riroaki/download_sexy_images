# 图片数据集爬取
- 数据集来源：https://github.com/alexkimxyz/nsfw_data_scrapper
- 多线程爬取，支持断点续爬；在url下面的文件是剩余待爬链接集合，每次文件内容会不断减少
- 使用方法：在项目目录下创建`porn`,`sexy`,`drawings`,`hentai`,`neutral`,`urls`,并将`url_raw`文件夹下所有文件复制到`urls`文件夹下，然后在项目目录下运行`download.py`
- 大部分图片需要科学上网……
