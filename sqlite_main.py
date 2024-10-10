from tools.sql4sqlite import SqliteTool



def createTable():
    db = SqliteTool('data.db')
    db.delete_table('software_accounts')
    db.create_table('software_accounts',
                    'uuid TEXT NOT NULL PRIMARY KEY,software_name TEXT NOT NULL,account TEXT NOT NULL,password TEXT NOT NULL,is_available TEXT NOT NULL,remark TEXT')




def insert():
    db = SqliteTool('data.db')
    db.insert('software_accounts', {'uuid': 'runnway1',
              'software_name': 'runnway1', 'account': 'aaaa1', 'password': 'aaaa', 'is_available': '可用'})

    db.insert('software_accounts', {'uuid': 'runnway2',
        'software_name': 'runnway1', 'account': 'aaaa2', 'password': 'aaaa', 'is_available': '可用'})
    

if __name__ == '__main__':
    createTable()
    # insert()

