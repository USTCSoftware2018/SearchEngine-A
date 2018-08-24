# Scrapy Projects

## Uniport
运用scrapy, 从网页多进程爬取www.uniprot.org域名下的五个数据库uniprot, uniref, uniparc, proteomes, taxonomy中对输入的索引的搜索结果.

运行时

1.  先进入setting.py, 将最后的FEED_URI项里的路径修改为想要其输出文件的路径
2.  进入包含scrapy.cfg文件的文件夹, 执行cmd命令

```cmd
scrapy crawl uniprot -a query=p53
# 也可以在后面加入其它参数如 -a sort=id, 实现根据entryID排序. 其它的筛选项需要根据网站规定的语法作出修改, 暂时还未实现.
```
## Rcsb
在scrapy框架下, 利用rcsb提供的REST服务爬取需要检索的内容的简介等信息

运行时

1.  先进入setting.py, 将最后的FEED_URI项里的路径修改为想要其输出文件的路径
2.  进入包含scrapy.cfg文件的文件夹, 执行cmd命令

```cmd
scrapy crawl uniprot -a argument=p53
# 也可以在后面加入其它参数如 -a sortMethod="Release Date", 实现根据发布时间排序. 后续希望按照别的检索依据查询可以加入参数 -a queryType=StructureIdQuery, 将argument当作数据库的id来检索, 不过这一部分尚未完善.
```
