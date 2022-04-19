import mysql.connector
from json import load
from os.path import join, dirname

class tables:               #class containing all table related functions

    def create_tables(cursor):          
        cursor.execute('CREATE TABLE Job_Types1 (Category varchar(100) NOT NULL, PRIMARY KEY(Category))')
        cursor.execute('CREATE TABLE Job_Types2 (Subcategory varchar(100) NOT NULL, Category varchar(100) NOT NULL, PRIMARY KEY(Subcategory), FOREIGN KEY (Category) REFERENCES Job_Types1(Category))')
        cursor.execute('CREATE TABLE States (State varchar(45) NOT NULL, PRIMARY KEY(State))')
        cursor.execute('CREATE TABLE Company_Details (Serial_Number int NOT NULL, Name varchar(100) NOT NULL, Description varchar(4000) NULL, State varchar(45) NOT NULL, Subcategory varchar(100) NOT NULL, PRIMARY KEY (Serial_Number), FOREIGN KEY (State) REFERENCES States(State), FOREIGN KEY (Subcategory) REFERENCES Job_Types2(Subcategory))')
        cursor.execute('CREATE TABLE Jobs (Serial_Number int NOT NULL, Company varchar(100) NOT NULL, Job_Position varchar(200) NOT NULL, Location varchar(200) NOT NULL, PRIMARY KEY (Serial_Number))')


    def update_table1(cursor, conn):
        insert_stmt ="INSERT INTO Job_Types1 (Category) VALUES (%s)"     # Preparing SQL query to INSERT a record into the database.
        data_1 = load(open(join(dirname(__file__), 'step1.json'), "r", encoding='utf-8')) #loading the required json file into a dictionary
        
        for x in data_1.keys():
            try:
                cursor.execute(insert_stmt, (x,))            # Executing the SQL command            
                conn.commit()               # Commit your changes in the database
                print("Data inserted")
            except:
                conn.rollback()             # Rolling back in case of error    
                       

    def update_table2(cursor, conn):
        insert_stmt ="INSERT INTO Job_Types2 (Subcategory, Category) VALUES (%s, %s)"
        data_1 = load(open(join(dirname(__file__), 'step1.json'), "r", encoding='utf-8'))
        for x in data_1:
            for y in data_1.get(x):
                try:
                    cursor.execute(insert_stmt, (y, x))                    
                    conn.commit()               
                    print("Data inserted")
                except:
                    conn.rollback()  
        


    def update_table3(cursor, conn):
        insert_stmt ="INSERT INTO States (State) VALUES (%s)"
        data_2 = load(open(join(dirname(__file__), 'step2.json'), "r", encoding='utf-8'))
        for x in data_2:
            try:
                cursor.execute(insert_stmt, (x,))                    
                conn.commit()               
                print("Data inserted")
            except:
                conn.rollback()  
        


    def update_table4(cursor, conn):
        insert_stmt ="INSERT INTO Company_Details (Serial_Number, Name, Description, State, Subcategory) VALUES (%s, %s, %s, %s, %s)"
        data_2 = load(open(join(dirname(__file__), 'step2.json'), "r", encoding='utf-8'))
        data_3 = load(open(join(dirname(__file__), 'step3.json'), "r", encoding='utf-8'))
        count=1
        for x in data_2:              
            for y in data_2.get(x):
                for z in data_2.get(x).get(y):
                    try:
                        desc=data_3.get(z['company_name']).get('Description')
                        if(desc): desc=desc.replace('\n', ' ')      #checking if the description is empty
                        cursor.execute(insert_stmt, (count, z['company_name'], desc, x, y))
                        conn.commit()               
                        count+=1
                        print("Data inserted")
                    except:
                        conn.rollback()  
        
    def update_table5(cursor, conn):
        insert_stmt ="INSERT INTO Jobs (Serial_Number, Company, Job_Position, Location) VALUES (%s, %s, %s, %s)"
        data_2 = load(open(join(dirname(__file__), 'step2.json'), "r", encoding='utf-8'))
        count=1     #serial number count
        temp=[]

        for x in data_2.values():
            for y in x:
                for z in x.get(y):
                    try:
                        #checking for duplicacies
                        if([z['company_name'], z['job_title'][:70], z['location'][:z['location'].find('\n')]] not in temp):
                            temp.append([z['company_name'], z['job_title'][:70], z['location'][:z['location'].find('\n')]])
                        
                            cursor.execute(insert_stmt, (count, z['company_name'], z['job_title'][:70], z['location'][:z['location'].find('\n')]))
                            conn.commit()               
                            count+=1
                            print("Data inserted")
                    except:
                        conn.rollback()  
        


def mysql_test():
    #establishing the connection
    
    conn=mysql.connector.connect(user='ENTER YOUR USERNAME', password='ENTER PASSWORD', host='127.0.0.1', database='ENTER DATABASE NAME')

    cursor = conn.cursor()          #Creating a cursor object using the cursor() method
    
    tables.create_tables(cursor)    #Creating the 5 required tables

    tables.update_table1(cursor, conn)             #updating the 5 databases one-by-one
    tables.update_table2(cursor, conn)
    tables.update_table3(cursor, conn)
    tables.update_table4(cursor, conn)
    tables.update_table5(cursor, conn)
    conn.close()        # Closing the connection  

mysql_test()

