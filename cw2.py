import json
import datetime
import tkinter as tk
from tkinter import messagebox
#add all user inputs to a list, they dont need uniform attributes meaning expenses and incomes can have differnt end attributes.
#filter by the attributes youy want
#when making table get the type of transaction, then filter by just that so then its organised

#validation for date
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

#get the user input using th eprompt, gets if it is valid or not, if it is invalid it shows the error message and repeats until is true
#if it is true it returns the user input to the function   
def check_input_is_valid(prompt, validation_function, error_message):
    while True:
        user_input = input(prompt)
        if validation_function(user_input):
            return user_input
        else:
            print(error_message)

#checks the input is a float above 0            
def is_valid_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount > 0:
            return True
        else:
            return False
    except ValueError:
        return False
 
#checks input is an integer above 0     
def is_valid_integer(id_str):
  try:
    id = int(id_str)
    if id > 0:
      return True 
    else:
      return False
  except ValueError:
      return False

#checks user input against valid instance of transaction
#for debugging all types have a capital letter at the start    
def is_valid_type(type):
    valid_types = ['Income', 'Expense', 'RecurringBill']
    valid = bool(type.strip())
    type_count = False
    if valid == True:

        for t in valid_types:
            if type == t:
                type_count = True
        if type_count == True:
            return True
    else:
        return False

#checks that the user inputted t or f       
def is_valid_bool(boolean):
  boolean = boolean.upper()
  if boolean == "T" or boolean == "F":
    return True
  else:
    return False

# ensures importance level i snot going higher then 10 
def valid_importance_level(level_str):
    try:
        level = int(level_str)
        return 1 <= level <= 10
    except ValueError:
        return False

#super class of transaction
class Transaction:
  def __init__(self, ID, Date, Amount, Description):
    self.ID = ID
    self.Date = Date
    self.Amount = Amount
    self.Description = Description
  
  #converts the data into a dictionary to be added to json database  

  def to_database(self):
    return {
        "ID": self.ID,
        "Date": self.Date,
        "Amount": self.Amount,
        "Description": self.Description
    }
  
  #only in for debugging, can be removed at end, just shows values without using database 
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}"

#inheritance from super class
class Income(Transaction):
  def __init__(self, ID, Date, Amount, Description, Source, isTaxable):
    super().__init__(ID, Date, Amount, Description)
    self.Source = Source
    self.isTaxable = isTaxable
  
  #only in for debugging, can be removed at end, just shows values without using database   
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Income, Source: {self.Source}, isTaxable: {self.isTaxable}"
  
  #converts the data into a dictionary to be added to json database  

  def to_database(self):
    data = super().to_database()
    data["Type"] = "Income"
    data["Source"] = self.Source
    data["IsTaxable"] = self.isTaxable
    return data

#inheritance from super class
class Expense(Transaction):
  def __init__(self, ID, Date, Amount, Description, Category, ImportanceLevel):
    super().__init__(ID, Date, Amount, Description)
    self.Category = Category
    self.ImportanceLevel = ImportanceLevel
  
  #only in for debugging, can be removed at end, just shows values without using database   
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Expense, Category: {self.Category}, ImportanceLevel: {self.ImportanceLevel}"
  
  #converts the data into a dictionary to be added to json database
  def to_database(self):
      data = super().to_database()
      data["Type"] = "Expense"
      data["Category"] = self.Category
      data["ImportanceLevel"] = self.ImportanceLevel
      return data
    

#inheritance from super class
class RecurringBill(Transaction):
  def __init__(self, ID, Date, Amount, Description, Frequency, NextDueDate):
    super().__init__(ID, Date, Amount, Description)
    self.Frequency = Frequency
    self.NextDueDate = NextDueDate
    
     #only in for debugging, can be removed at end, just shows values without using database  
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Recurring, Frequency: {self.Frequency}, NextDueDate: {self.NextDueDate}"

  #converts the data into a dictionary to be added to json database
  def to_database(self):
    data = super().to_database()
    data["Type"] = "RecurringBill"
    data["Frequency"] = self.Frequency
    data["NextDueDate"] = self.NextDueDate
    return data
  
class TransactionManager:
  def __init__(self, filename="transactions"):
    self.filename = filename
    self.transactions = []
    #opens database and stores it inside of data
    try: 
      with open(f"{filename}.json", "r") as f:
        data =json.load(f)
      #loops through data and then gets the type and adds them to the dictionary inside each type
      for item in data:
        tx_type = item.get("Type")

        if tx_type == "Income":
          self.transactions.append(
            Income(
              item["ID"],
              item["Date"],
              float(item["Amount"]),
              item["Description"],
              item["Source"],
              item["IsTaxable"]

            )
          )
        
        elif tx_type == "Expense":
          self.transactions.append(
              Expense(
                  item["ID"],
                  item["Date"],
                  float(item["Amount"]),
                  item["Description"],
                  item["Category"],
                  item["ImportanceLevel"]
              )
          )

        elif tx_type == "RecurringBill":
          self.transactions.append(
              RecurringBill(
                  item["ID"],
                  item["Date"],
                  float(item["Amount"]),
                  item["Description"],
                  item["Frequency"],
                  item["NextDueDate"]
              )
          )


    except (FileNotFoundError, json.JSONDecodeError):
      print("no database exists, starting new database")
      
#saves the transactions using to database to convert to a dictionary, adding them to the database stored in transactions
#then dumps them into transactions.json
  def save_transactions(self, filename):
    with open(f"{filename}.json", "w") as f:
        json.dump([t.to_database() for t in self.transactions], f, indent=4)
  
  
  #adds transactions to database  
  def add_transaction(self, transaction):
    self.transactions.append(transaction)
    self.save_transactions(self.filename)
    print("transaction added successfully")

  #prints database, may only need 218 - 221, if someone wants to test then you can
  def view_transactions(self, filename):
    try:
        with open(f"{filename}.json", "r") as f:
            data=json.load(f)
        print(data)
        return (data)
    except FileNotFoundError:
        print("file doesnt exist already, creating database now")
        self.save_transactions( filename)
    except json.JSONDecodeError:
        print("save file is corrupted! Starting fresh")
        self.save_transactions(filename)

#  Simple forecasting calculations using transaction data.
class ForecastService:
  def __init__(self, transaction_manager):
      # Uses the same TransactionManager object so it can access stored transactions.
      self.manager = transaction_manager
      self.transactionsexpense = []
      self.transactionsincome = []
      self.transactionsrecurring = []
      self.transactionsrecurring30day = []
      self.transactionsrecurringamount = []

      self.total_balance = float(0)
      self.total_income = float(0)
      self.total_expense = float(0)
      self.total_recurring = float(0)

      self.current_date = datetime.now()

  # Returns all recurring bills stored in the transaction list.
  def forecast_recurring_bills(self):
      self.transactionsrecurring = [t for t in self.manager.transactions if isinstance(t, RecurringBill)]
      return self.transactionsrecurring
  # Returns total amount of recuring bills due in 30 days
  def forecast_recurring_bills_30days(self):
      self.transactionsrecurring = self.forecast_recurring_bills
      for bill in self.transactionsrecurring:
        # convert NextDueDate to datetime
        due_date = datetime.strptime(bill.NextDueDate, "%Y-%m-%d")

        #Checks if its within the next 30 days
        if self.current_date <= due_date <= self.future_date:
          self.transactionsrecurring30day.append(bill)

      self.transactionsrecurringamount = [t.Amount for t in self.transactionsrecurring30day]
      return self.transactionsrecurring30day, self.transactionsrecurringamount
  
  # Returns a total amount for recurring bills
  def forecast_recurring_amount(self):
      self.transactionsrecurringamount = self.forecast_recurring_bills_30days()
      self.total_recurring = sum(float(self.transactionsrecurringamount))
      return self.total_recurring
  
  # Calculates the expense amount.
  def forecast_monthly_expenses(self):
      self.transactionsexpense = [t.Amount for t in self.manager.transactions if isinstance(t, Expense)]
      self.total_expense = float(sum(self.transactionsexpense))
      return self.total_expense

  # Calculates the income amount
  def forecast_income_amount(self):
      self.transactionsincome = [t.Amount for t in self.manager.transactions if isinstance(t, Income)]
      self.total_income = sum(float(self.transactionsincome))
      return self.total_income
  
  # Calculates the total balance
  def forecast_balance(self):
      self.total_balance = float(self.total_income - self.total_expense)
      return self.total_balance
  
  # Calculates balance after recurring bills are taken off
  def forecast_balance_recurring(self):
     self.total_balance - self.total_recurring


#  Budget calculations.
class BudgetManager:
  def __init__(self, monthly_budget):
      # Stores the user's monthly budget.
      self.monthly_budget = monthly_budget

  # Calculates total spending by adding expenses and recurring bills.
  def calculate_total_expenses(self, transaction_manager):
      return sum(t.Amount for t in transaction_manager.transactions if isinstance(t, Expense) or isinstance(t, RecurringBill))

  # Calculate how much budget is left.To prevent errorosit will round the number to 2 decimal places  to keep them accurate and relaistic 
  def remaining_budget(self, transaction_manager):
      spent = self.calculate_total_expenses(transaction_manager)
      return round(self.monthly_budget - spent, 2)

  # Ensure user has not gone over monthly budget
  def is_over_budget(self, transaction_manager):
      return self.remaining_budget(transaction_manager) < 0

  # Tells the user a visual message depending on the budget, 2f rouds it to 2 decimal places 
  def budget_status(self, transaction_manager):
      remaining = self.remaining_budget(transaction_manager)

      if remaining < 0:
          return f" You are over budget by {abs(remaining):.2f}"
      elif remaining < self.monthly_budget * 0.2:
          return f" Warning: Only {remaining:.2f} left in your budget"
      else:
          return f" You have {remaining:.2f} remaining"


# Report for the transactions 
class ReportGenerator:
    def __init__(self, transaction_manager):
        # Allows the report generator to access all stored transactions.
        self.manager = transaction_manager

    # Summary report of all the billings
    def summary_report(self):
        incomes = [t.Amount for t in self.manager.transactions if isinstance(t, Income)]
        expenses = [t.Amount for t in self.manager.transactions if isinstance(t, Expense)]
        recurring = [t.Amount for t in self.manager.transactions if isinstance(t, RecurringBill)]

        # Calculates totals before placing them into the report dictionary.
        total_income = sum(incomes)
        total_expenses = sum(expenses)
        total_recurring = sum(recurring)

        return {
            "Total Income": round(total_income, 2),
            "Total Expenses": round(total_expenses, 2),
            "Total Recurring Bills": round(total_recurring, 2),
            "Net Balance": round(total_income - total_expenses - total_recurring, 2)
        }

    # Seperate expenses by catagory and produces a total amount 
    def category_breakdown(self):
        breakdown = {}

        for t in self.manager.transactions:
            if isinstance(t, Expense):
                breakdown.setdefault(t.Category, 0)
                breakdown[t.Category] += t.Amount

        return breakdown

    # creates a json file with all the transactions 
    # try/except there to prevent any crashes 
    def export_to_json(self, filename="transactions_export"):
      try:
          data = [
              t.to_database() if hasattr(t, "to_database") else t.__dict__
              for t in self.manager.transactions
          ]

          with open(f"{filename}.json", "w") as f:
              json.dump(data, f, indent=4)

          return f"{filename}.json saved successfully"

      except Exception as error:
          return f"Export failed: {error}"
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Transaction Manager")
        self.geometry("400x300")
        self.transaction_manager = TransactionManager()
        self.create_widgets()
    def create_widgets(self):
        self.add_button = tk.Button(self, text="Add Transaction", command=self.add_transaction)
        self.add_button.pack(pady=10)
        self.view_button = tk.Button(self, text="View Transactions", command=self.view_transactions)
        self.view_button.pack(pady=10)
        self.report_button = tk.Button(self, text="Generate Report", command=self.report_generator)
        self.report_button.pack(pady=10)
    def add_transaction(self):
       new_window = tk.Toplevel(self)
       new_window.title("Add Transaction")
       new_window.geometry("300x400")
       tk.Label(new_window, text="ID:").pack()
       id_entry = tk.Entry(new_window)
       id_entry.pack()
       tk.Label(new_window, text="Date (yyyy-mm-dd):").pack()
       date_entry = tk.Entry(new_window)
       date_entry.pack()
       tk.Label(new_window, text="Amount:").pack()
       amount_entry = tk.Entry(new_window)
       amount_entry.pack()
       tk.Label(new_window, text="Description:").pack()
       description_entry = tk.Entry(new_window)
       description_entry.pack()
       tk.Label(new_window, text="Type (Income, Expense, RecurringBill):").pack()
       type_entry = tk.Entry(new_window)
       type_entry.pack()
       tk.Button(new_window, text="Submit", command=lambda: self.submit_transaction(id_entry.get(), date_entry.get(), amount_entry.get(), description_entry.get(), type_entry.get())).pack(pady=10)
    def submit_transaction(self, id, date, amount, description, type):
        if not is_valid_integer(id):
            messagebox.showerror("Error", "ID must be an integer above 0")
            return
        if not is_valid_date(date):
            messagebox.showerror("Error", "Date must be in format yyyy-mm-dd")
            return
        if not is_valid_amount(amount):
            messagebox.showerror("Error", "Amount must be a number above 0")
            return
        if not is_valid_type(type):
            messagebox.showerror("Error", "Type must be Income, Expense, or RecurringBill")
            return
        transaction = None
        if type == "Income":
            transaction = Income(id, date, float(amount), description, "Source", "T")
        elif type == "Expense":
            transaction = Expense(id, date, float(amount), description, "Category", 1)
        elif type == "RecurringBill":
          new_window = tk.Toplevel(self)
          new_window.title("Recurring Bill Details")
          new_window.geometry("300x200")
          tk.Label(new_window, text="Frequency:").pack()
          frequency_entry = tk.Entry(new_window)
          frequency_entry.pack()
          tk.Label(new_window, text="Next Due Date (yyyy-mm-dd):").pack()
          next_due_date_entry = tk.Entry(new_window)
          next_due_date_entry.pack()
          submit_recurring_bill = lambda: self.submit_recurring_bill(id, date, amount, description, frequency_entry.get(), next_due_date_entry.get(), new_window)
          tk.Button(new_window, text="Submit", command=submit_recurring_bill).pack(pady=10)
          return
        # only add & show success for transactions created synchronously
        if transaction is not None:
            self.transaction_manager.add_transaction(transaction)
            messagebox.showinfo("Success", "Transaction added successfully")

    def submit_recurring_bill(self, id, date, amount, description, frequency_str, next_due_date_str, window):
        if not is_valid_integer(frequency_str):
            messagebox.showerror("Error", "Frequency must be an integer above 0")
            return
        if not is_valid_date(next_due_date_str):
            messagebox.showerror("Error", "Next Due Date must be in format yyyy-mm-dd")
            return
        try:
            freq = int(frequency_str)
            amt = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Frequency must be an integer and Amount a number")
            return
        transaction = RecurringBill(id, date, amt, description, freq, next_due_date_str)
        self.transaction_manager.add_transaction(transaction)
        window.destroy()
        messagebox.showinfo("Success", "Recurring bill added successfully")
    def view_transactions(self):
        transactions = self.transaction_manager.view_transactions("transactions")
        view_window = tk.Toplevel(self)
        view_window.title("View Transactions")
        view_window.geometry("400x300")
        text = tk.Text(view_window)
        text.pack()
        for t in transactions:
            text.insert(tk.END, f"{t}\n")
    def report_generator(self):
        report = ReportGenerator(self.transaction_manager)
        summary = report.summary_report()
        breakdown = report.category_breakdown()
        export_message = report.export_to_json()
        report_window = tk.Toplevel(self)
        report_window.title("Report")
        report_window.geometry("400x300")
        text = tk.Text(report_window)
        text.pack()
        text.insert(tk.END, "Summary Report:\n")
        for key, value in summary.items():
            text.insert(tk.END, f"{key}: {value}\n")
        text.insert(tk.END, "\nCategory Breakdown:\n")
        if breakdown:
            for category, amount in breakdown.items():
                text.insert(tk.END, f"{category}: {round(amount, 2)}\n")
        else:
            text.insert(tk.END, "No expenses found\n")
        text.insert(tk.END, f"\n{export_message}\n")

if __name__ == "__main__":
  gui_cli = input("Enter 1 for CLI or 2 for GUI: ")
  if gui_cli == "2":
      app = App()
      app.mainloop()    
  else:
     manager = TransactionManager()
     user_error = 0
     while True:
        print("Welcome to the transaction manager")
        print("Enter 1 to add to the database")
        print("Enter 2 to view the database")
        print("Enter 3 to use the forcast service")
        print("Enter 4 to set a budget")
        print("Enter 5 for a report")
        print("Enter 0 to exit the program")
        try:
           choice = int(input("Enter your choice: "))
      
           if 0 <= choice <6:
            if choice == 0:
             print("closing program")
             break
           elif choice == 1:
             #need to check if id exists inside of the database already
             while user_error == 0:
               #loop to prevent duplicat IDs
               while True:
                 ID = check_input_is_valid("Enter the ID of the transaction: ", is_valid_integer, "Enter an integer above 0 that isnt in the database")  
                 ID=ID.strip()
                 #assumes that its the only one with that ID
                 exists=False
                 #checck all the transations for that ID
                 for t in  manager.transactions:
                    #uses boolen,if it is a duplicate tthen exists becomes true 
                    if t.ID==ID:
                       exists= True
                 if not exists:
                    break
                 else:
                    print("This Id already exists ")
               Date = check_input_is_valid("Enter the date of the expense(yyyy-mm-dd): ", is_valid_date, "Enter date in format yyyy-mm-dd")
               Amount = check_input_is_valid("Insert the amount: ", is_valid_amount, "Enter a float above 0")
               Amount=float(Amount)
               Description = input("Enter Description: ")
               type = check_input_is_valid("enter the type of transaction,these are Income, Expense, RecurringBill: ", is_valid_type, "Enter a valid type of transaction")
               
               if type == "Income":
                 Source = input("Enter the Source: ")
                 isTaxable = check_input_is_valid("is it taxable T or F: ", is_valid_bool, "Enter T or F")
                 
                 T = Income(ID, Date, Amount, Description, Source, isTaxable)
                 
               elif type == "Expense":
                 Category = input("Enter the Category of expense: ")
                 ImportanceLevel = check_input_is_valid("Enter Importance Level 1-10: ", valid_importance_level, "Enter a valid integer 1-10 ")
                 T = Expense(ID, Date, Amount, Description, Category, ImportanceLevel)
                 
               elif type == "RecurringBill":
                 Frequency = check_input_is_valid("Enter the Frequency of expense: ", is_valid_integer, "Enter an integer above 0 that isnt in the database")
                 NextDueDate = check_input_is_valid("When is the next due date in the (format yyyy-mm-dd): ", is_valid_date, "Enter date in format yyyy-mm-dd")
                 T = RecurringBill(ID, Date, Amount, Description, Frequency, NextDueDate)
               else:
                 print("wrong input")
                 
               manager.add_transaction(T)
               break
             
           elif choice == 2:
             manager.view_transactions("transactions")
           elif choice == 3:
             forecast=ForecastService(manager)
             #call the alll the forcat methods from the class 
             average_expense=forecast.forecast_monthly_expenses()
             average_income=forecast.forecast_income_amount()
             recurring_bills=forecast.forecast_recurring_bills()
             #this will print the visual message 
             print("The average monly expense is ",average_expense)
             print("the average income ",average_income)
             print("The recurring bill amount is ",recurring_bills)
           elif choice == 4:
             monthly_budget = check_input_is_valid(
                 "Enter your monthly budget: ",
                 is_valid_amount,
                 "Enter a number above 0"
             )
             monthly_budget = float(monthly_budget)
             budget = BudgetManager(monthly_budget)
             total = budget.calculate_total_expenses(manager)
             remaining = budget.remaining_budget(manager)
             status = budget.budget_status(manager)
             print("Total expenses:", total)
             print("Remaining budget:", remaining)
             print(status)
           elif choice == 5:
             report = ReportGenerator(manager)

             summary = report.summary_report()
             breakdown = report.category_breakdown()
             export_message = report.export_to_json()

             print("Summary Report:")
             # loops thorugh the summary dictionary
             for key, value in summary.items():
                 print(key, ":", value)
             #prints heading and creates a new line 
             print("\nCategory Breakdown:")
             if breakdown:
                 #loop through categories 
                 for category, amount in breakdown.items():
                     print(category, ":", round(amount, 2))
             else:
                 print("No expenses found")

             print(export_message)
           else:
             print("Number is out of range, Enter a number between 0 and 5")
        except ValueError:
            print("please enter an integer between 0 and 5")
