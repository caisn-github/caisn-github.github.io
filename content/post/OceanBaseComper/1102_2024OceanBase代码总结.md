# 1102_2024OceanBase代码总结
| 项目 | 完成情况 |
| --- | --- |
| 环境搭建 | 已完成 |
| 时间类型添加 - 总结|  |
| 删除表实现 -总结 |  |
| 更新表实现-总结 |  |

-- 目前: 已修改41份文件, 更新2k代码, 排名174/1200
https://github.com/caisn-github/miniob

## 1.环境搭建 -- 已总结
## 2.时间类型添加 

主要流程:
   时间类型是数据库的几种基础类型中的一种(int, char, varchar, datetime, timestamp, date, time, year)等, 所以在实现的时候, 需要继承type类, 并做到
   1. 实现char->date类型的转化, date -> char的转化(因为在用户输入的时候, 先识别到的是char类型, 落盘时候找到表中的元组), 所以需要实现char -> date

   2. 新增src/observer/common/type/date_type.cpp文件, 在char->date之后判断是否是正常时间类型

## 3.删除表实现
   主要流程:
   删除表的操作实现比较简单:
1. 删除表实际在磁盘中的存储位置, 找到表存储的数据库地址, 并删除对应的"del_tbale_name".data和"del_table_name".table文件
2. 删除内存缓存中的表信息. miniOB的缓存有一个统一的管理handle, 调用该Memeory_handle的对应drop函数

## 4.更新表实现
主要流程:
由于miniOB中没有update关键词, 所以从解析开始添加
1. 添加UPDATE关键词, 在解析时候传入updateSqlNode中的table name, 更新的attribute_name, attribute_value, update的过滤where condition条件
2. 生成UPDATE的logical plan(逻辑算子)
3. 生成UPDATE的physical plan(物理算子)
4. 其中物理算子的操作: 通过condition找到需要更新的record, 对于每条记录进行更新操作: 
   确认attribute_name与元组是否一致;
   替换attribute_value在record中的值
我的实现是使用了函数中自带的delete_record+insert_record来实现更新操作. 不确定这样的实现是否冗余.
