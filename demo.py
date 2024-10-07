
from tools import customer_common_funcs as ccf




def test_demo():
    list = ccf.list_files_in_directory("out/sr2/tmp")
    list1 = [  i + "aaaaaa" for i in list]
    print(list1)




if __name__ == '__main__':
    test_demo()
