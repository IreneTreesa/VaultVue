
import mysql.connector 
db=mysql.connector.connect(host='localhost', user='root', password='lfps',database= 'vaultvue')
cursor=db.cursor()

def create_account():
    
    while True:
        username= input('Enter User Name: ')
        password= input('Enter password: ')
        password2= input('Confirm your password: ')
        if password== password2:
            print('Updated successfully')
            break
    values= (username,password)
    query='insert into users(user_name,password) values(%s,%s)'
    cursor.execute(query,values)
    db.commit()
    
def set_budget():
    budget=float(input('Enter your budget: ')) 
    print('Budget amount Rs.',budget,'updated.')
    return budget
    



def edit_details(account):
    print('1. Edit username')
    print('2. Edit password')
    ch= int(input('Enter your choice: '))
    if ch==1:
        new_name= input('Enter new username: ')
        query='update users set user_name=%s where user_id=%s'
        values=(new_name,account[0])
        cursor.execute(query,values)
        db.commit()
        print('Name updated successfully')
    elif ch==2:
        new_password= input('Enter new password: ')
        query='update users set password=%s where user_id=%s'
        values=(new_password,account[0])
        cursor.execute(query,values)
        db.commit()
        print('Password updated successfully')
    else:
        print('Invalid choice')
        
 
        

def start():
    while True:
        print('---------------------')
        print(' WELCOME TO VAULTVUE')
        print('---------------------')
        print('1. Create Account')
        print('2. Login')
        print('3. Close')
        ch= int(input('Enter your choice: '))
        if ch==1:
            create_account()
        elif ch==2:
            login()
        elif ch==3:
            
            break
        else:
            print('Invalid choice. Please try again.')
    print('Thankyou for using VAULTVUE')
    
#start()
        
def add_expenses(account):
    while True:
        cursor.execute('select * from categories')
        rec= cursor.fetchall()
        for i in rec:
            print(i[0],'.',i[1])
        ch=int(input('Enter choice: '))
        if ch in [1,2,3,4,5,6,7,8,9,10,11]:
            try: 
                date= input('Enter date as YYYY/MM/DD: ')
                amount= float(input('Enter amount: '))
                query='insert into expenses(user_id,category_id,amount,date) values(%s,%s,%s,%s)'
                values=(account[0],ch,amount,date)
                cursor.execute(query,values)
                db.commit()
                print('Expense updated')
            except: 
                print('Invalid date or amount. Please try again')
                
        else:
            print('Invalid choice')
        choice= input('Do you want to continue(y/n): ')
        if choice.lower()=='n':
            menu(account)
        


    
def generate_report(budget,account):
    try:
        date1= input('Enter date1(YYYY/MM/DD): ')
        date2= input('Enter date1(YYYY/MM/DD): ')
        
        print()
        print("-----------------------------------------")
        print('\t\tREPORT')
        print("-----------------------------------------")
        print('Analysis from',date1,'to',date2)
        print()
        print('Budget set:',budget)
        
        query1= 'select sum(amount) from expenses where date between %s and %s and user_id=%s'
        values1=(date1,date2, account[0])
        cursor.execute(query1,values1)
        expenditure= cursor.fetchone()
        print('Total Expenditure:',expenditure[0])
        
        values2= account[0]
        query2= 'select category_name, sum(amount) from categories C,expenses E where C.category_id= E.category_id and user_id=%s group by category_name'%(values2)
        
        cursor.execute(query2)
        rec= cursor.fetchall()
        print()
        print('Category\t','Amount')
        for i in rec:
            print(i[0],'\t\t',i[1])
        print("-----------------------------------------")
        if expenditure[0]> budget:
            diff= expenditure[0] - budget
            print('You have exceeded your budget by Rs.',diff)
        elif expenditure[0]== budget:
            print('Budget amount= Expenditure')
            
        else:
            save= budget- expenditure[0]
            print('You have saved Rs.',save)
            print('WELL DONE!')
        
        print("-----------------------------------------")   
    except:
        print('Invalid date format. Please try again')
    


def menu(account):
    while True:
        print()
        print('Hi',account[1])
        print('1. Set Budget')
        print('2. Add Expenses')
        print('3. Generate Report')
        print('4. Edit details')
        print('5. Quit')
        ch= int(input('Enter your choice: '))
        if ch==1:
            budget= set_budget()
        elif ch==2:
            add_expenses(account)
        elif ch==3:
            generate_report(budget,account)
        elif ch==4:
            edit_details(account)
        elif ch==5:
            break
        else:
            print('Invalid Choice. Please try again.')
        


def login():
    global account
    while True:
        username= input('Enter User Name: ')
        password= input('Enter password: ')
        query= 'select * from users where user_name=%s and password= %s'
        values=(username,password)
        cursor.execute(query,values)
        account= cursor.fetchone()
        if account:
            print('Login successful')
            break
        else:
            print('Invalid username or password. Please try again')
              
    menu(account)

