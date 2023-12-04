from jinja2 import Environment, FileSystemLoader
from string_utils import manipulation
import re
import argparse
import os
import pyperclip
import sys


def underscore_to_camelcase(name):
    parts = name.split('_')
    camelcase_name = ''.join(x.title() for x in parts)
    return camelcase_name


def parse_arguments():
    parser = argparse.ArgumentParser(description='DDL文件解析程序 by vison')
    parser.add_argument('--ddl_file', type=str, help='DDL文件路径')
    parser.add_argument('--output_file', type=str, help='输出文件路径')
    parser.add_argument('--p',type=bool, help='从粘贴板获取ddl内容')
    return parser.parse_args()


def read_file(filename: str) -> str:
    # 打开文件
    file = open(filename, "r")
    # 读取文件内容
    content = file.read()
    # 关闭文件
    file.close()
    return content


def parse_ddl(ddl):
    print('准备解析内容:'+ddl)
    # 匹配表名
    pattern_table = r"CREATE TABLE `(\w+)`"

    # 匹配字段
    pattern_fields = r"^\s+`([^`]+)` ([^.\s(]+)(?:[^']+)?[^']?(?:DEFAULT '([^']?)'\s?)?(?:COMMENT '([^']+)'\s?)"

    # 提取表名
    table_name = re.search(pattern_table, ddl, re.I).group(1)

    # 提取字段信息
    matches = re.findall(pattern_fields, ddl, re.MULTILINE | re.I)
    fields = [{
        'name': match[0].strip(),
        'type': match[1].strip(),
        'comment': match[3].strip() if match[3] else None,
        'default': match[2].strip() if match[2] else None
    } for match in matches]

    return table_name, fields


def main():
    args = parse_arguments()
    ddl_file = args.ddl_file
    output_file = args.output_file
    ddl_content = args.p
    if ddl_content:
        ddldata = pyperclip.paste()
    elif ddl_file:
        ddldata = read_file(ddl_file)
    else:
        print("必须至少选择一个ddl内容获取方式")
        sys.exit(1)
    # 获取当前执行文件的路径
    current_path = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(current_path))
    tpl = env.get_template('ddl2pojo.tpl')
    propertiesList: list = []
    if len(ddldata) == 0: 
        print("兄弟,看下粘贴板或文件内容是不是空的!")
        sys.exit(1)
    result = parse_ddl(ddldata)
    mysqlType2JavaMap: dict = {
        'int': 'Integer',
        'tinyint': 'byte',
        'smallint': 'short',
        'mediumint': 'int',
        'bigint': 'long',
        'float': 'float',
        'double': 'double',
        'decimal': 'BigDecimal',
        'bit': 'boolean',
        'longtext': 'String',
        'text':'String',
        'char': 'String',
        'varchar': 'String',
        'binary': 'byte[]',
        'varbinary': 'byte[]',
        'tinyblob': 'byte[]',
        'blob': 'byte[]',
        'mediumblob': 'byte[]',
        'longblob': 'byte[]',
        'date': 'Date',
        'datetime': 'Date',
        'timestamp': 'Timestamp',
        'time': 'Time',
        'year': 'int',
    }
    for item in result[1]:
        column: dict = {}
        column['name'] = manipulation.snake_case_to_camel(item['name'], False)
        column['javatype'] = mysqlType2JavaMap[item['type'].lower()]
        column['comment'] = item['comment']
        propertiesList.append(column)

    className = underscore_to_camelcase(result[0])
    render_content:str = tpl.render({
                "table_name": className,
                "columns": propertiesList
            })
    # 输出到文件或打印到控制台
    if output_file:
        with open('%s.java' % className, 'w+') as fout:
            fout.write(render_content)
    else:
        # 在这里将解析结果打印到控制台
        print("处理结果")
        print("\n================================")
        print(render_content)


if __name__ == '__main__':
    main()