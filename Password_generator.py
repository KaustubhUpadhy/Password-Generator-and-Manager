import random  
import mysql.connector 
import datetime
# Password length will be 12 characters
passwd_genetion= input("Do you want to generate a new password?:")
while passwd_genetion.upper()=="YES":
    def passwd_restrictions(): # Checking if password can contain special characters
     a = input("Are special characters allowed(Enter yes or no):")
     if a.upper()=="YES":
        print("Special characters are allowed")
        return True
     else:
        return False
    
    restrictions = passwd_restrictions()     
    special_chr = ["!","@","#","$","%","^","&","*","?"]
    passwd_spchr= []
    rep_value = None
# The loop will go through a list of special characters and will select four(4) random special characters 

    if restrictions is True:    
     for sp_chr in range (0,4):
        a =  random.choice(special_chr)
        while a==rep_value:
            a = random.choice(special_chr)
        rep_value = a
        passwd_spchr.append(a)
    
    alpha_chr=[]

    if restrictions is True:
     for i in range (0,2):
        upper_chr = chr(random.randrange(65,90))
        lower_chr = chr(random.randrange(97,122))
        alpha_chr.append(upper_chr)
        alpha_chr.append(lower_chr)
# The random function will go through a range of particular numbersets to generate a random number 
# That number will be later on converted into Alphabet on the basis of ASCII Values through chr() function.
    else:
     for i in range (0,3):
        upper_chr = chr(random.randrange(65,90))
        lower_chr = chr(random.randrange(97,122))
        alpha_chr.append(upper_chr)
        alpha_chr.append(lower_chr)

    num_chr=[]
    rep = 0
    # Then 4 random numbers will be generated through the range (0,9)
    if restrictions is True:
     for i in range(0,4):
        num = random.randint(0,9)
        while num==rep:
            num = random.randint(0,9)
        rep= num
        num_chr.append(num)
    else:
     for i in range(0,6):
        num = random.randint(0,9)
        while num==rep:
            num = random.randint(0,9)
        rep= num
        num_chr.append(num)
# The elements of the list will  get shuffled randomly and then will be put toogether.

    if restrictions is False:
        init_passwd = f"{alpha_chr[5]}{alpha_chr[4]}{num_chr[5]}{num_chr[4]}{num_chr[0]}{num_chr[1]}{num_chr[2]}{num_chr[3]}{alpha_chr[0]}{alpha_chr[1]}{alpha_chr[2]}{alpha_chr[3]}" 
        lst = init_passwd.split()
        random.shuffle(lst) # Shuffles the content of a list.
        password= "".join(lst)
        print("The Generated password is:",password)
    elif restrictions is True: 
        init_passwd = f"{passwd_spchr[0]} {passwd_spchr[1]} {passwd_spchr[2]} {passwd_spchr[3]} {num_chr[0]} {num_chr[1]} {num_chr[2]} {num_chr[3]} {alpha_chr[0]} {alpha_chr[1]} {alpha_chr[2]} {alpha_chr[3]}" 
        lst = init_passwd.split()
        random.shuffle(lst)
        password= "".join(lst)
        print("The Generated password is:",password)
    passwd_genetion= input("Do you want to generate a new password?:")

# Password generation process keeps running until user is satisfied with the generated password.

passwd_save = input("Do you want to save this password?(Or any other Password):")
now=datetime.datetime.utcnow()
modify_notif=now.strftime("%Y-%m-%d %H:%M:%S") # Object/Variable to store current date and time directly from system.
# Now if the user has agreed to save the password the next block of code will run to establish the connection with database and follow the next steps
def sql_connect():
   global con1 #Password for sql connection to be taken as input
   global my_cursor
   sql_passwd = input("Enter your MySQL Password:") 
   con1= mysql.connector.connect(host="localhost",user="root",passwd=sql_passwd)
   if con1.is_connected():
      print("Connections with database established successfully")
   my_cursor = con1.cursor()

while passwd_save.upper()=="YES":
    sql_connect()
    # Now the database will be created for the password storage if it does not exists.
    # Three different tables will be created for password management: Social Media accounts,Work accounts,Bank accounts
    my_cursor.execute("Create Database if not exists Password_Storage;")
    my_cursor.execute("use Password_Storage;")
    my_cursor.execute("create table if not exists Social(App_name varchar(40) NOT NULL, email_id varchar(50) NOT NULL, password varchar(20) NOT NULL, username varchar(25), Last_Modified datetime);")
    my_cursor.execute("create table if not exists Work(App_name varchar(40) NOT NULL, email_id varchar(50) NOT NULL, password varchar(20) NOT NULL, username varchar(25),  Last_Modified datetime);")
    my_cursor.execute("create table if not exists BANK(Bank_name  varchar(40) NOT NULL, Account_No  int(25) NOT NULL, Account_holder char(40), password varchar(20) NOT NULL,  Last_Modified datetime);")
    table_use=int(input("Which type of password do you want to save:Social,Work or bank?(Enter 1 for Social,2 for work and other for bank):"))
    if table_use==1:
        app=input("Enter App name:")
        email=input("Enter Email id:")
        passwd= input("Enter your Password:")
        username=input("Enter youR username:")
        query= "INSERT INTO social VALUES('{}','{}','{}','{}','{}')".format(app,email,passwd,username,modify_notif)
        my_cursor.execute(query)
        # Input for all columns and rows and insertion with date and time taken from system
    elif table_use==2:
        app=input("Enter App name:")
        email=input("Enter Email id:")
        passwd= input("Enter your Password:")
        username=input("Enter youR username:")
        query= "INSERT INTO work VALUES('{}','{}','{}','{}','{}')".format(app,email,passwd,username,modify_notif)
        my_cursor.execute(query)
    else :
        Bank = input("Enter Bank name:")
        Acc_num = input("Enter your Account Number:")
        Acc_holder= input("Enter Account Holder's name:")
        passwd = input("Enter your password:")
        query= "INSERT INTO Bank VALUES('{}',{},'{}','{}','{}')".format(Bank,Acc_num,Acc_holder,passwd,modify_notif)
        my_cursor.execute(query)
    passwd_save= input("Do you want to add more passwords?:")
    my_cursor.close()
    con1.commit()

passwd_extract = input("Do you want to an extract a Password?:")
# Now if the user wants to extract a password he can extract it.

while passwd_extract.upper()=="YES":
    sql_connect()
    my_cursor.execute("use Password_Storage;")
    # Input is taken from the user to select the table from which he wants to extract the password from.
    table_name = input("Enter the password type you want to extract (Or the table name):")
    if table_name =="social":
      app_name= input("Enter the App name:")
      email_id = input("Enter the email id:")
      query = "Select password from social WHERE App_name = %s AND email_id = %s" # Parametrized Query
      tup1= (app_name,email_id) 
      my_cursor.execute(query,tup1) # The values from tup1 are used as the values for the parameters set in the query.
      records = my_cursor.fetchall()
      print("Extracting Password ")
      for row in records:                   
         print("The Password is:",row[0])      
    elif table_name =="work":
      app_name= input("Enter the App name:")
      email_id = input("Enter the email id:")
      query = "Select password from work WHERE App_name = %s AND email_id = %s"
      tup1= (app_name,email_id)
      my_cursor.execute(query,tup1)
      records = my_cursor.fetchall()
      print("Extracting Password ")
      for row in records:
         print("The Password is:",row[0])
    else:
      Bankname= input("Enter the Bank name:")
      Acc_no = input("Enter the Account number :")
      query = "Select password from bank WHERE Bank_name  = %s AND Account_No  = %s"
      tup1= (Bankname,Acc_no)
      my_cursor.execute(query,tup1)
      records = my_cursor.fetchall()
      print("Extracting Bank Details")
      for row in records:
         print("The Password is:",row[0])
    passwd_extract = input("Do you want to an extract another Password?:")
    my_cursor.close()
    con1.commit()

# Now if the user wants to delete a record/data/password from the table/storage.
data_deletion = input("Do you want to Delete any data or Password?:")

while data_deletion.upper()=="YES":
    sql_connect()
    my_cursor.execute("use Password_Storage;")
    table_name=int(input("Select the table name or the type of data you want to delete from:(1 for social,2 for work and others for bank)"))
    if table_name==1:
      app_name=input("Enter the App you want to delete the data for:") 
      user_name = input("Enter the username(or account name you want to delete for):")
      query="Delete from social where App_name=%s AND username= %s" 
      tup1= (app_name,user_name)
      my_cursor.execute(query,tup1)
    elif table_name==2:
      app_name  = input("Enter the App you want to delete the data for:")
      user_name = input("Enter the username(or account name you want to delete for):")
      query="Delete from work where App_name=%s AND username= %s"
      tup1= (app_name,user_name)
      my_cursor.execute(query,tup1)
    else:
      Bankname= input("Enter the Bank name:")
      Acc_no = input("Enter the Account number :")
      query="Delete from bank where Bank_name  = %s AND Account_No  = %s"
      tup1=(Bankname,Acc_no)
      my_cursor.execute(query,tup1)
    data_deletion = input("Do you want to Delete another data or Password?:")
    my_cursor.close()
    con1.commit()
    print("Records Deleted Successfully")


