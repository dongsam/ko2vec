#-*- coding: utf-8 -*-
__author__ = 'dongsamb'
import pymysql
import json

# todo: list to pandas dataframe or named tuple, etc
# todo: loader return data class object


class AbstractLoader(object):
    data_list = []

    def __init__(self):
        if self.__class__ is AbstractLoader:
            raise TypeError('This is abstract class')

    def __len__(self):
        return len(self.data_list)

    def __iter__(self):
        for data in self.data_list:
            yield data

    def __getitem__(self, key):
        return self.data_list[key]

    def __str__(self):
        return json.dumps(self.data_list, ensure_ascii=False)

    def pprint(self):
        return_str = ""

        return_str += '[0][doc] '
        return_str += str(self.data_list[0][0]) + '\n'
        return_str += '[0][label] '
        return_str += str(self.data_list[0][1]) + '\n'

        return_str += '[1][doc] '
        return_str += str(self.data_list[1][0]) + '\n'
        return_str += '[1][label] '
        return_str += str(self.data_list[1][1]) + '\n'

        return_str += '\n[..][..]\n\n'

        return_str += '[{}][doc] '.format(len(self.data_list)-1)
        return_str += str(self.data_list[-1][0]) + '\n'
        return_str += '[{}][label] '.format(len(self.data_list)-1)
        return_str += str(self.data_list[-1][1]) + '\n'

        print(return_str)


class LoaderMysql(AbstractLoader):
    """
    have to select doc, label, name ~
    """

    def __init__(self, mysql_host, mysql_user, mysql_passwd, mysql_db, mysql_port=3306):
        self.conn = pymysql.connect(
            host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, port=mysql_port, charset='utf8')
        self.conn.autocommit(True)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)
        try:
            self.data_list = [[row[0], row[1], row[2]] for row in self.cur]
        except:
            self.data_list = [[row[0]] for row in self.cur]

    # @staticmethod
    # def read_data_from_mysql_cur(cur):
    #     try:
    #         data = [[row[0], row[1], row[2]] for row in cur]
    #     except:
    #         data = [[row[0]] for row in cur]
    #
    #     return data


class LoaderMongoDB(AbstractLoader):
    """
    have to select doc, label, name ~
    """
    def __init__(self, mysql_host, mysql_user, mysql_passwd, mysql_db):
        self.conn = pymysql.connect(
            host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, charset='utf8')
        self.conn.autocommit(True)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)
        try:
            self.data_list = [[row[0], row[1], row[2]] for row in self.cur]
        except:
            self.data_list = [[row[0]] for row in self.cur]



# class LoaderFile(AbstractLoader):
#     pass

# LoaderPath
# LoaderURL
# LoaderText

