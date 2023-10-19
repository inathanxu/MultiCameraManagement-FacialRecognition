# 用于存放sql语句代码
import pymysql
'''
自己定义一个SQLfunction类 专门用于放SQL相关方法 
目的在于避免反复地连接数据库以及关闭数据库
'''
class SqlF:
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='1002',
            database='db_bishe'
        )
        self.cursor = self.db.cursor()

    def loginAccountPassword(self, loginaccount):
        sql = '''
        select password from login where account = '%s'
        ''' % loginaccount
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        return results

    def register(self, registerAccount, registerPassword):
        sql = '''
        insert into login(account, password)
        values ('%s', '%s')
        ''' % (registerAccount, registerPassword)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print('新注册用户失败！')
            print(e.args)
            print(str(e))
            print(repr(e))


    def getAllaccount(self):
        sql = '''
        select distinct account from login
        '''
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def saveNameTimePic(self, xcname, xcplace, xctime):
        # print('保存人员的姓名、出现的地点、出现的时间')
        sql = '''
            insert into log(name,place,time)
            values ('%s', '%s', '%s')
            ''' % (xcname, xcplace, xctime)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print('保存人员姓名、出现地点、出现时间失败！')
            print(e.args)
            print(str(e))
            print(repr(e))

    def resetDB(self):
        print('重置数据库内容，对表进行初始化操作')
        sql = '''
            delete from log where 1=1
        '''
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交修改
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()

    def tableWidgetDisplay(self):
        sql = '''
        select * from log order by time desc limit 100
        '''
        # mysql支持limit语句来选取指定条数的数据 选取最近50条数据
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        return results

    def getAllname(self):
        sql = '''
        select distinct name
        from log
        '''
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def getAllplace(self):
        sql = '''
        select distinct place
        from log
        '''
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results


    def dbclose(self):
        # 关闭数据库连接
        self.db.close()
