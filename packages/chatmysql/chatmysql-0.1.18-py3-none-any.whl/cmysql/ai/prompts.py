INFER_MDATAKG_PROMPT = """请根据元数据 MData，生成包含了数据关联关系和数据定义的 MDataKG.

要求：
1. 生成的 MDataKG 是一个json格式的内容，包含2个属性：Entities、 Relationships
2. Entities中包含了数据库、表和字段三层实体。
3. Table和Column的 desc 默认从 MData 中的 comment 中提取，如果为空则需要根据name来推测。table的desc需要结合field来推测。
4. DB没有comment，所以 DB的 desc 需要根据table来推测，不少于10个字。
5. desc 请用中文表示，不要用英文
6. Relationships 中只包含1种关系：column_to_column，其中每个元素包含3个属性：from、to、precision_rate，分别表示关系的起点、终点、准确率。
如果B是主键，A是B的外键，则A是from，B是to。请根据字段名和他们所属的表名，来推测他们之间的关系，并给出准确率。
7. from和to需要包含完整的database.table.column名称。
8. 准确率precision_rate是一个0-1之间的小数，表示推测的准确率。
9. 请尽量多的推测关系，但是不要推测错误的关系，推测错误的关系会影响后续的数据查询。

{% raw %}

示例：
MDataKG = {
    "Entities": {
        "databases": {
            "test": {
                "desc": "",
                "tables": {
                    "t_shop": {
                        "desc": "商店表",
                        "columns": {
                            "id": "商店ID"
                        }
                    }
                }
            }
        },
    },
    "Relationships": {
        "column_to_column": [
            {
                "from": "test.t_product.shop_id",
                "to": "test.t_shop.id",
                "precision_rate": 0.7
            }
        ]
    }
}

{% endraw %}

提供的元数据如下：
MData = {{ mdata }}

那么
MDataKG=
"""


GENERATE_SQL_PROMPT = """
你是一名MySQL专家，请根据用户的 Question 和 Meta Data，生成SQL语句。
要求
1,SQL中的Table需要带上Database，例如：db1.table1
2,SQL中的列名和表名必须严格按照Meta Data中提供的来

注意
1，今年是2023年，如果问题中有提到日期没有说年份的话，就默认是2023年

Question: {{ question }}

Meta Data: {{ mdata }}

生成结果是JSON格式，Key是SQL。
结果：
"""

CHECK_SQL_PROMPT = """
你是一名MySQL专家，请根据下面的SQL和Meta Data，检查SQL中的表名和字段名是否正确。
如果正确，回答 valid，否则回答 invalid。

Meta Data : {{ mdata }}
SQL: {{ sql_cmd }}

回答：
"""

GENERATE_ANSWER_PROMPT = """
你是一名MySQL和数据分析专家，请根据用户的问题、Meta Data、SQL以及SQL结果，生成答案，用中文。

Question ：{{ question }}
Meta Data: {{ mdata }}
SQL: {{ sql_cmd }}
Result: {{ sql_result }}


答案：
"""


GLOBAL_KEY_CONCEPTS_PROMPT = """
一些关键概念：

1. Meta Data：简称 MData，MySQL中的数据字典、元数据，即表结构信息。
2. Meta Data Knowledge Graph：简称 MDataKG，根据MData推测出的数据字典的含义以及他们之间的关系。
3. MDataKG存储在向量（用于数据字典的近似检索）和图数据库（用于数据血缘关系的精确检索）中。
4. MDataKG 在图中的数据结构如下：
    4.1，Database 节点, 有 desc 和 name 属性
    4.2，Table 节点, 有 desc, name 和 short_name 属性
    4.3，Column 节点, 有 desc, name 和 short_name 属性
    4.4，Table 节点通过 T2D 关系连接到 Database
    4.5，Column 节点通过 C2T 关系连接到 Table
    4.6，Column 节点通过带有 precision_rate 属性的 C2C 关系连接到 Column
"""


GENERATE_MDATAKG_CHANGES_PROMPT = """
你是一名图数据库专家，请根据用户的反馈，生成MDataKG的修改内容，用JSON格式。

用户对 MDataKG 的Graph可能有如下修改诉求：
1，修改 Table 的 desc，要注意如果一个table的desc修改了，那么可能需要同步修改这个table下所有的column的desc
2，修改 Column 的 desc
3，修改 C2C关系 的 precision_rate
4，删除某一个或多个 C2C 关系
5，增加一个或多个 C2C 关系

请根据用户的反馈，生成修改内容 MDataKGChanges，示例如下：
MDataKGChanges = {
    "desc": {
        "test.t_product": "产品表",
        "test.t_product.shop_id": "产品所属商店标识",
        "test": "电商数据库"
    },
    "relationships": {
        "remove_c2c": [
            "test.t_product.shop_id -> test.t_shop.id",
        ],
        "add_c2c": [
            "test.t_product.shop_id -> test.t_shop.id : 0.8",
        ],
        "modify_c2c": [
            "test.t_product.shop_id -> test.t_shop.id : 0.9",
        ]
    }
}


用户的反馈：
{{ user_feedback }}
                
与用户反馈相关的表和字段：
{{ related_mdata }}

MDataKGChanges =
"""

