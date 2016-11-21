from User_Table_Lite import User_Table_Lite


def main():
    new_table = User_Table_Lite('blobs.db')
    result = new_table.get_records(1,2)
    print(result)
    new_table.close_connection()

if __name__ == '__main__':
    main()
