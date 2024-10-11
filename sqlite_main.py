from tools.sql4sqlite import SqliteTool
from tools import customer_common_funcs as ccf
import pandas as pd
import sqlite3

def createTable():
    db = SqliteTool('data.db')
    db.delete_table('url_mapping')
    db.create_table('url_mapping',
                    'uuid TEXT NOT NULL PRIMARY KEY,short_url TEXT NOT NULL,long_url TEXT NOT NULL')




def insert():
    db = SqliteTool('data.db')
    short01 = 'https://tinyurl.com/235wellk'
    long01 = 'https://claude.ai/chat/b866fad0-63ab-4517-b7be-7585363dcc64'
    db.insert('url_mapping', {'uuid': ccf.get_unique_value(short01 + long01),
              'short_url': short01, 'long_url': long01})

    short02 = 'https://tinyurl.com/2dosx6zr'
    long02 = 'https://app2.gravitywrite.com/content/new?category=27&prompt=147'
    db.insert('url_mapping', {'uuid': ccf.get_unique_value(short02 + long02),
              'short_url': short02, 'long_url': long02})
    
    short03 = 'https://tinyurl.com/2xq6bof2'
    long03 = 'https://piclumen.com/app/image-generator/create'
    db.insert('url_mapping', {'uuid': ccf.get_unique_value(short03 + long03),
              'short_url': short03, 'long_url': long03})
    
    short04 = 'https://tinyurl.com/29w24k3e'
    long04 = 'https://portal.azure.com/?quickstart=true#@yuxinqianxingproton.onmicrosoft.com/resource/subscriptions/74293bb9-ea60-4e2d-8b39-334469355078/resourceGroups/voice/providers/Microsoft.CognitiveServices/accounts/voice0001/overview'
    db.insert('url_mapping', {'uuid': ccf.get_unique_value(short04 + long04),
              'short_url': short04, 'long_url': long04})
   



def delete_record():
    db = SqliteTool('data.db')
    db.delete("url_mapping",
              "uuid='03a017cdadb6c4a1f487dcaa5e3493ddf9eff724e737bf1c195892d9b0726d1b'")

if __name__ == '__main__':
    #createTable()
   # insert()
    delete_record()

