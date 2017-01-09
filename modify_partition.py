"""
修改表指向位置
ALTER TABLE table_name SET LOCATION "new location";


删除分区
ALTER TABLE bingo_login DROP IF EXISTS PARTITION (dt='2016-08-11');


修改某个partitioin指向位置
ALTER TABLE table_name PARTITION (dt='2016-12-05')SET LOCATION "s3://papaya-log/fluentd/s3.newbingo_login/dt=2016-12-05";

批量执行可以将语句保存到文件中 hive -f filename 执行

hive -e "select * from table_name"

MSCK REPAIR TABLE table_name;、

"""

from datetime import datetime, timedelta
import argparse
import traceback


def generate_argparse():
    l_parser = argparse.ArgumentParser(prog="Generate Hive execute file",
                                       description="modify hive table partition location")

    l_parser.add_argument('-s', dest='start_date', help='the start partition you wanna operate')
    l_parser.add_argument('-e', dest='end_date', help='the end partition you wanna operate')
    l_parser.add_argument('-t', dest='tablename', help='the table name you wanna modify')
    l_parser.add_argument('-l', dest='location', help='the data store location')
    return l_parser.parse_args()


def generate_execfile(a_start_data, a_end_data, a_tablename, a_pre_location):
    l_format = "%Y-%m-%d"

    l_start_time = datetime.strptime(a_start_data, l_format)
    l_end_time = datetime.strptime(a_end_data, l_format)

    sql = "ALTER TABLE {tablename} PARTITION (dt='{dt}')SET LOCATION '{pre_location}/dt={dt}';\n"

    with open('exec_file', 'w') as f:
        while l_start_time <= l_end_time:
            f.write(sql.format(dt=l_start_time.strftime(l_format),
                               tablename=a_tablename,
                               pre_location=a_pre_location))
            l_start_time += timedelta(days=1)


if __name__ == '__main__':
    try:
        args = generate_argparse()

        generate_execfile(args.start_date, args.end_date, args.tablename, args.location)
    except Exception:
        traceback.print_exc()
