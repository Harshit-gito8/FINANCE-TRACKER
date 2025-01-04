import mysql.connector as cnt
con=cnt.connect(host="localhost",user="root",password="Harshit@08",database="EXPENSE_TRACKER")
cur=con.cursor()
def basic_details():
    id=int(input("enter your id:" ))
    query= "select*from expenses where ID=%s"
    cur.execute(query,(id,))
    dat=cur.fetchall()
    print("ID | NAME | TOTAL EXPENDETURE | TOTAL SAVINGS")
    for i in dat:
        print (i," ")

def cur_month_details():
    id=int(input("enter your id:" ))
    from datetime import date
    day=date.today()
    mon=day.strftime("%B")  #%B is a format code that reperesents the full name of the month
    #strftime() used to convert date or date time object into string
    year=str(day.year)
    moye=mon+" "+year
    query= "select*from monthly_expenses where MONTH_AND_YEAR=%s AND ID=%s"
    cur.execute(query,(moye,id,))
    dat=cur.fetchall()
    print("ID | MONTHLY LIMIT | MONTHLY EXPENSES | MONTHLY SAVINGS | OVERSPENDING | MONTH AND YEAR")
    for i in dat:
        print(i," ")

def all_monthly_expenses():

    id=int(input("enter your id:" ))
    query= "select*from monthly_expenses where ID=%s"
    cur.execute(query,(id,))
    dat=cur.fetchall()
    print("ID | MONTHLY LIMIT | MONTHLY EXPENSES | MONTHLY SAVINGS | OVERSPENDING | MONTH AND YEAR")
    for i in dat:
        print(i," ")

def daily_expenses():
    id=int(input("enter your id:" ))
    from datetime import date
    day=date.today()
    query= "select*from daily_expenses where id=%s AND date=%s"
    cur.execute(query,(id,day,))
    dat=cur.fetchall()
    print("ID | Date | CATEGORY | DESCRIPTION | AMOUNT")
    for i in dat:
        print(i," ")

def category_type():
    print("1. Educational Expenses")
    print("2. Living Expenses")
    print("3. Personal Expenses")
    print("4. Academic-Related Extracurricular Expenses")
    print("5. Entertainment and Leisure Expenses")
    print("6. Miscellaneous Expenses")
    print("7. Travel Expenses")
    print("8. Technology Expenses")
    print("9. Part-Time Job or Internship-Related Expenses")
    ex=int(input("Enter type of expense: "))
    if ex == 1:
        return "Educational Expenses"
    elif ex == 2:
        return "Living Expenses"
    elif ex == 3:
        return "Personal Expenses"
    elif ex == 4:
        return "Academic-Related Extracurricular Expenses"
    elif ex == 5:
        return "Entertainment and Leisure Expenses"
    elif ex == 6:
        return "Miscellaneous Expenses"
    elif ex == 7:
        return "Travel Expenses"
    elif ex == 8:
        return "Technology Expenses"
    elif ex == 9:
        return "Part-Time Job or Internship-Related Expenses"
    else:
        return "Invalid choice! Please enter a number between 1 and 9."

def input_expenses():
    id=int(input("enter your id:" ))
    from datetime import date
    day=date.today()
    amount = float(input("Enter amount: "))
    category = category_type()
    description = input("Enter descryption: ")
    query = "INSERT INTO daily_expenses VALUES (%s, %s, %s, %s, %s)"
    ex=(id,day,category, description,amount)
    cur.execute(query,ex)
    con.commit()
    inner_working(id,amount)

def create_new():
    print("WLECOME TO FINANCE MANAGEMENT SYSTEM")
    id=int(input("ENTER A NUMBER TO BE USED AS ID: "))
    query="select ID from expenses;"
    cur.execute(query)
    dat=cur.fetchall()
    for i in dat:
        if i[0]==id:
            print("This ID no. already exists create a different no.")
            return
    nam=input("Enter your name: ")
    MonLmt=float(input("set a monthly spending limit goal : "))
    query = "INSERT INTO expenses (ID,NAME) VALUES (%s, %s);"
    cur.execute(query,(id,nam))
    con.commit()
    query="INSERT INTO  monthly_expenses (ID,MONTHLY_LIMIT) VALUES (%s,%s);"
    cur.execute(query,(id,MonLmt))
    con.commit()
    from datetime import date
    day=date.today()
    amount = float(input("Enter amount: "))
    category = category_type()
    description = input("Enter descryption: ")
    query = "INSERT INTO daily_expenses VALUES (%s, %s, %s, %s, %s)"
    ex=(id,day,category,description,amount)
    cur.execute(query,ex)
    con.commit()
    mon=day.strftime("%B")  #%B is a format code that reperesents the full name of the month
    #strftime() used to convert date or date time object into string
    year=str(day.year)
    moye=mon+" "+year
    query="UPDATE monthly_expenses SET MONTH_AND_YEAR = %s WHERE ID = %s;"
    ex=(moye,id)
    cur.execute(query,ex)
    con.commit()
    query="UPDATE monthly_expenses SET MONTHLY_EXPENSE = %s WHERE ID= %s AND MONTH_AND_YEAR= %s;"
    cur.execute(query,(amount,id,moye))
    con.commit() 

def inner_working(id,amount):
    from datetime import date
    day=date.today()
    mon=day.strftime("%B")  #%B is a format code that reperesents the full name of the month
    #strftime() used to convert date or date time object into string
    year=str(day.year)
    moye=mon+" "+year
    query="select MONTHLY_EXPENSE from monthly_expenses where id=%s AND MONTH_AND_YEAR=%s;"
    cur.execute(query,(id,moye))
    dat=cur.fetchall()
    if dat:  # Check if any result was returned
        ne= dat[0][0]  # dat[0] is the tuple, dat[0][0] is the first column value
        amt = ne + amount
    query="UPDATE monthly_expenses SET MONTHLY_EXPENSE = %s WHERE ID=%s AND MONTH_AND_YEAR=%s;"
    cur.execute(query,(amt,id,moye))
    con.commit() 
    query="select MONTHLY_LIMIT from monthly_expenses where id=%s AND MONTH_AND_YEAR=%s;"
    ex=(id,moye)
    cur.execute(query,ex)
    dat=cur.fetchall()
    lim=dat[0][0]
    if amt>lim:
        os=amt-lim
        query="UPDATE monthly_expenses SET OVERSPENDING=%s WHERE ID=%s AND MONTH_AND_YEAR=%s;"
        cur.execute(query,(os,id,moye))
        con.commit() 
        query="UPDATE monthly_expenses SET MONTHLY_SAVINGS = 0.00 WHERE ID=%s AND MONTH_AND_YEAR=%s;"
        cur.execute(query,(id,moye))
        con.commit() 
    else:
        s=lim-amt
        query="UPDATE monthly_expenses SET MONTHLY_SAVINGS = %s WHERE ID=%s AND MONTH_AND_YEAR=%s;"
        cur.execute(query,(s,id,moye))
        con.commit()
        query="UPDATE monthly_expenses SET OVERSPENDING=0.00 WHERE ID=%s AND MONTH_AND_YEAR=%s;"
        cur.execute(query,(id,moye))
        con.commit()
    query="SELECT MONTHLY_EXPENSE from monthly_expenses where ID=%s;"
    cur.execute(query,(id,))
    dat=cur.fetchall()
    sv=0.0
    for i in dat:
      sv+=i[0]
    query="UPDATE expenses SET TOTAL_EXPENDETURE=%s WHERE ID=%s;"
    cur.execute(query,(sv,id))
    con.commit()
    query="SELECT MONTHLY_SAVINGS from monthly_expenses where ID=%s;"
    cur.execute(query,(id,))
    dat=cur.fetchall()
    sv=0.0
    for i in dat:
      sv+=i[0]
    query="UPDATE expenses SET TOTAL_SAVINGS=%s WHERE ID=%s;"
    cur.execute(query,(sv,id))
    con.commit()
def main():
    print("Welcome to the Finance Management System")
    while True:
        print("\nChoose an option:")
        print("1. View Basic Details")
        print("2. View Current Month Details")
        print("3. View All Monthly Expenses")
        print("4. View Daily Expenses")
        print("5. Input New Expense")
        print("6. Create a New User")
        print("7. Exit")
        
        choice = int(input("Enter your choice (1-7): "))

        if choice == 1:
            basic_details()
        elif choice == 2:
            cur_month_details()
        elif choice == 3:
            all_monthly_expenses()
        elif choice == 4:
            daily_expenses()
        elif choice == 5:
            input_expenses()
        elif choice == 6:
            create_new()
        elif choice == 7:
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 7.")
main()