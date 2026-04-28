import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime,timedelta
#add all user inputs to a list, they dont need uniform attributes meaning expenses and incomes can have differnt end attributes.
#filter by the attributes youy want
#when making table get the type of transaction, then filter by just that so then its organised

#validation for date
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
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
#validates for Need and Want ensure it is one of them no matter the format entered it will get rid of spaces and capitlise the first letter 
def is_valid_need_want(value):
    value = value.strip().capitalize()
    return value == "Need" or value == "Want"
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
  def __init__(self, ID, Date, Amount, Description, Category, ImportanceLevel,NeedWant):
    super().__init__(ID, Date, Amount, Description)
    self.Category = Category
    self.ImportanceLevel = ImportanceLevel
    self.NeedWant=NeedWant
  
  #only in for debugging, can be removed at end, just shows values without using database   
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Expense, Category: {self.Category}, ImportanceLevel: {self.ImportanceLevel},NeedWant:{self.NeedWant}"
  #converts the data into a dictionary to be added to json database
  def to_database(self):
      data = super().to_database()
      data["Type"] = "Expense"
      data["Category"] = self.Category
      data["ImportanceLevel"] = self.ImportanceLevel
      data["NeedWant"] = self.NeedWant
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
    self.category_budgets = {}
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
                  item["ImportanceLevel"],
                  item.get("NeedWant", "Want")
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
        return (data)
    except FileNotFoundError:
        print("file doesnt exist already, creating database now")
        self.save_transactions( filename)
    except json.JSONDecodeError:
        print("save file is corrupted! Starting fresh")
        self.save_transactions(filename)
    
    #this will allow the user to set a budget 
  def set_category_budget(self, category, budget_amount):
        self.category_budgets[category] = float(budget_amount)
    #this would calculate how much has lalready been used 
  def get_category_spending(self, category):
        total = 0
        #loop thorugh every transaction
        for t in self.transactions:
            #checks if the transaction is an expense and if it matches the catagory  that is getting checked 
            if isinstance(t, Expense) and t.Category == category:
                total += float(t.Amount)
        return total
  #this will check if it pushes the budget over the limit 
  def check_cat_bud(self, category, new_amount):
    #not set a budget for this catagory then it won't be checked 
    if category not in self.category_budgets:
        return None
    #get how much has already been spent 
    current_spending = self.get_category_spending(category)
    budget_limit = self.category_budgets[category]
    predicted_total = current_spending + float(new_amount)
    #warn the user if it is over the price limit or if they are still in budget they will tell them 
    if predicted_total > budget_limit:
        return f"Warning: This expense will push {category} over budget. Limit: £{budget_limit:.2f}, New total: £{predicted_total:.2f}"
    return f"{category} is still within budget. Limit: £{budget_limit:.2f}, New total: £{predicted_total:.2f}"

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
      self.total_balance_after = float(0)

      self.current_date = datetime.now()
      self.future_date = self.current_date + timedelta(days=30)

  # Returns all recurring bills stored in the transaction list.
  def forecast_recurring_bills(self):
      self.transactionsrecurring = [t for t in self.manager.transactions if isinstance(t, RecurringBill)]
      return self.transactionsrecurring
  # Returns total amount of recuring bills due in 30 days
  def forecast_recurring_bills_30days(self):
      self.transactionsrecurring = self.forecast_recurring_bills()
      for bill in self.transactionsrecurring:
        # convert NextDueDate to datetime
        try:
          due_date = datetime.strptime(bill.NextDueDate, "%Y-%m-%d")
        except ValueError:
          continue

        #Checks if its within the next 30 days
        if self.current_date <= due_date <= self.future_date:
          self.transactionsrecurring30day.append(bill)

      self.transactionsrecurringamount = [t.Amount for t in self.transactionsrecurring30day]
      return self.transactionsrecurringamount
  
  # Returns a total amount for recurring bills
  def forecast_recurring_amount(self):
      self.transactionsrecurringamount = self.forecast_recurring_bills_30days()
      print(self.transactionsrecurringamount)
      self.total_recurring = sum(float(x) for x in self.transactionsrecurringamount)
      return self.total_recurring
  
  # Calculates the expense amount.
  def forecast_monthly_expenses(self):
      self.transactionsexpense = [t.Amount for t in self.manager.transactions if isinstance(t, Expense)]
      self.total_expense = sum(float(x) for x in self.transactionsexpense)
      return self.total_expense

  # Calculates the income amount
  def forecast_income_amount(self):
      self.transactionsincome = [t.Amount for t in self.manager.transactions if isinstance(t, Income)]
      self.total_income = sum(float(x) for x in self.transactionsincome)
      return self.total_income
  
  # Calculates the total balance
  def forecast_balance(self):
      self.total_balance = float(self.total_income - self.total_expense)
      return self.total_balance
  
  # Calculates balance after recurring bills are taken off
  def forecast_balance_recurring(self):
     self.total_balance_after = float(self.total_balance - self.total_recurring)
     return self.total_balance_after


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
#For the need want feature 
    def need_want(self):
       needs_tot=0
       wants_tot=0
       #loop thrugh all the transactiosn 
       for t in self.manager.transactions:
          if isinstance(t,Expense):
             #check if the expense is a need 
             if t.NeedWant == "Need":
                needs_tot += t.Amount
             #check if it is wants expense
             elif t.NeedWant =="Want":
                wants_tot += t.Amount
       total=needs_tot +wants_tot
       #prevent divideby zero so no crash
       if total ==0:
          return{"needs":0,"wants":0,"needs %":"0%","wants %":"0%"}
       #results sreturned as dictionary.round them up percentage of them by 2 decimal points an din calulations all numbers rounded 
       return {"Needs": round(needs_tot, 2), "Wants": round(wants_tot, 2),"Needs %": f"{(needs_tot/total)*100:.2f}%","Wants %": f"{(wants_tot/total)*100:.2f}%"}
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
import tkinter as tk
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Transaction Manager")
        self.geometry("400x500")
        self.configure(bg="#1e1e2f")

        self.transaction_manager = TransactionManager()
        self.budget = None  

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        self.create_frames()
        self.show_frame("main")

    # ------------------ FRAME SETUP ------------------

    def create_frames(self):
        self.create_main_menu()
        self.create_add_transaction()
        self.create_view_transactions()
        self.create_report()
        self.create_forecast()
        self.create_budget()

        for frame in self.frames.values():
            frame.place(relwidth=1, relheight=1)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

        if name == "view":
            self.refresh_transactions()
        elif name == "report":
            self.refresh_report()
        elif name == "forecast":
            self.refresh_forecast()

    # ------------------ MAIN MENU ------------------

    def create_main_menu(self):
        frame = tk.Frame(self.container, bg="#1e1e2f")
        self.frames["main"] = frame
    # - Title
        tk.Label(frame, text="Main Menu", width=20, font=("Arial", 16)).pack(pady=20)
    # - Transactions-
        tk.Button(frame, text="Add Transaction", width=20, command=lambda: self.show_frame("add")).pack(pady=10) 
        tk.Button(frame, text="View Transactions", width=20, command=lambda: self.show_frame("view")).pack(pady=10)
    # - Reports - 
        tk.Button(frame, text="Generate Report", width=20, command=lambda: self.show_frame("report")).pack(pady=10)
        tk.Button(frame, text="Generate Forecast", width=20, command=lambda: self.show_frame("forecast")).pack(pady=10)
    # - Budgets - 
        tk.Button(frame, text="Budget Manager", width=20, command=lambda: self.show_frame("budget")).pack(pady=10)
    # - Exit -
        tk.Button(frame, text="Exit", width=20, command=lambda: self.exit()).pack(pady=10)

    # ------------------ EXIT ------------------    
    
    def exit(self):
       self.destroy()

    # ------------------ TRANSACTION ------------------

    def create_add_transaction(self):
        frame = tk.Frame(self.container, bg="#1e1e2f")
        self.frames["add"] = frame

        # Title
        tk.Label(frame, text="Add Transaction", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # ID
        tk.Label(frame, text="ID:").grid(row=1, column=0, sticky="w", padx=10)
        self.id_entry = tk.Entry(frame)
        self.id_entry.grid(row=1, column=1, padx=10)

        # Date
        tk.Label(frame, text="Date (yyyy-mm-dd):").grid(row=2, column=0, sticky="w", padx=10)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=2, column=1, padx=10)

        # Amount
        tk.Label(frame, text="Amount:").grid(row=3, column=0, sticky="w", padx=10)
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=3, column=1, padx=10)

        # Description
        tk.Label(frame, text="Description:").grid(row=4, column=0, sticky="w", padx=10)
        self.desc_entry = tk.Entry(frame)
        self.desc_entry.grid(row=4, column=1, padx=10)

        # Type
        tk.Label(frame, text="Type:").grid(row=5, column=0, sticky="w", padx=10)
        # Dropdown Box
        self.type_var = tk.StringVar()
        self.type_var.set("Income")
        # Adds dropdown box adding buttons based on the different selection
        self.type_var.trace_add("write", self.update_fields)
        #this is for the dropdown menu 
        self.type_dropdown = tk.OptionMenu(frame, self.type_var, "Income", "Expense", "RecurringBill")
        self.type_dropdown.grid(row=5, column=1, padx=10)
        #This is the label and field for need want 
        self.needwant_label = tk.Label(frame, text="Need or Want:")
        self.needwant_entry = tk.Entry(frame)
        # Submit
        tk.Button(frame, text="Submit", command=self.handle_add).grid(row=10, column=0, columnspan=2, pady=10)

        # Back button
        tk.Button(frame, text="Back", command=lambda: self.show_frame("main")).grid(row=11, column=0, columnspan=2)

    # - EXTRA FIELDS -

        # Income fields
        self.source_label = tk.Label(frame, text="Source:")
        self.source_entry = tk.Entry(frame)

        self.tax_label = tk.Label(frame, text="Taxable (T/F):")
        self.tax_entry = tk.Entry(frame)

        # Expense fields
        self.category_label = tk.Label(frame, text="Category:")
        self.category_entry = tk.Entry(frame)

        self.importance_label = tk.Label(frame, text="Importance (1-10):")
        self.importance_entry = tk.Entry(frame)

        # Recurring fields
        self.freq_label = tk.Label(frame, text="Frequency (days):")
        self.freq_entry = tk.Entry(frame)

        self.nextdue_label = tk.Label(frame, text="Next Due Date:")
        self.nextdue_entry = tk.Entry(frame)

        self.update_fields()

    def update_fields(self, *args):
        # Hides everything first
        for widget in [
            self.source_label, self.source_entry,
            self.tax_label, self.tax_entry,
            self.category_label, self.category_entry,
            self.importance_label, self.importance_entry,
            self.freq_label, self.freq_entry,
            self.nextdue_label, self.nextdue_entry,
            self.needwant_label, self.needwant_entry
        ]:
            widget.grid_forget()

        type_ = self.type_var.get()

        # Show only relevant fields
        if type_ == "Income":
            self.source_label.grid(row=6, column=0, sticky="w", padx=10)
            self.source_entry.grid(row=6, column=1, padx=10)

            self.tax_label.grid(row=7, column=0, sticky="w", padx=10)
            self.tax_entry.grid(row=7, column=1, padx=10)

        elif type_ == "Expense":
            self.category_label.grid(row=6, column=0, sticky="w", padx=10)
            self.category_entry.grid(row=6, column=1, padx=10)

            self.importance_label.grid(row=7, column=0, sticky="w", padx=10)
            self.importance_entry.grid(row=7, column=1, padx=10)

            #need and want label 
            self.needwant_label.grid(row=8, column=0, sticky="w", padx=10)
            self.needwant_entry.grid(row=8, column=1, padx=10)

        elif type_ == "RecurringBill":
            self.freq_label.grid(row=6, column=0, sticky="w", padx=10)
            self.freq_entry.grid(row=6, column=1, padx=10)

            self.nextdue_label.grid(row=7, column=0, sticky="w", padx=10)
            self.nextdue_entry.grid(row=7, column=1, padx=10)

    def handle_add(self):
        id = self.id_entry.get()
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        desc = self.desc_entry.get()
        type_ = self.type_var.get()

        # ID validation
        if not is_valid_integer(id):
            messagebox.showerror("Error", "ID must be an integer above 0")
            return

        # loop through transactions and compare the id with other ids in the tranaction file ensuring it is not a duplicate 
        for t in self.transaction_manager.transactions:
            if str(t.ID) == str(id):
                messagebox.showerror("Error", "ID already exists")
                return

        # date validation
        if not is_valid_date(date):
            messagebox.showerror("Error", "Date must be in format yyyy-mm-dd")
            return

        # amount validation
        if not is_valid_amount(amount):
            messagebox.showerror("Error", "Amount must be a number above 0")
            return

        amount = float(amount)

        # type validation
        if not is_valid_type(type_):
            messagebox.showerror("Error", "Type must be Income, Expense, or RecurringBill")
            return

        # Shows only boxes related to the type of entry
        if type_ == "Income":
            source = self.source_entry.get()
            taxable = self.tax_entry.get()

            #income validation
            if not source.strip():
                messagebox.showerror("Error", "Source cannot be empty")
                return

            if not is_valid_bool(taxable):
                messagebox.showerror("Error", "Taxable must be T or F")
                return

            transaction = Income(id, date, amount, desc, source, taxable)

        elif type_ == "Expense":
            category = self.category_entry.get()
            importance = self.importance_entry.get()
            needwant = self.needwant_entry.get().strip().capitalize()

            #expense validation
            if not category.strip():
                messagebox.showerror("Error", "Category cannot be empty")
                return

            if not valid_importance_level(importance):
                messagebox.showerror("Error", "Importance Level must be an integer between 1 and 10")
                return

            if not is_valid_need_want(needwant):
                messagebox.showerror("Error", "Enter either Need or Want")
                return
            #call the budget checking passes in category and amount fromt he user 
            bud_message = self.transaction_manager.check_cat_bud(category, amount)
            #check if the budget message exist wheathe it should warn the user 
            if bud_message is not None and bud_message.startswith("Warning"):
                messagebox.showwarning("Budget Alert", bud_message)
            #if theydon't it would sow a normal poopup about them beingwithin budget 
            elif bud_message is not None:
                messagebox.showinfo("Budget Status", bud_message)
            transaction = Expense(id, date, amount, desc, category, int(importance), needwant)

        elif type_ == "RecurringBill":
            freq = self.freq_entry.get()
            nextdue = self.nextdue_entry.get()

            #recurring bill validation 
            if not is_valid_integer(freq):
                messagebox.showerror("Error", "Frequency must be an integer above 0")
                return

            if not is_valid_date(nextdue):
                messagebox.showerror("Error", "Next Due Date must be in format yyyy-mm-dd")
                return

            transaction = RecurringBill(id, date, amount, desc, int(freq), nextdue)

        else:
            messagebox.showerror("Error", "Invalid type")
            return

        self.transaction_manager.add_transaction(transaction)
        messagebox.showinfo("Success", "Transaction added successfully")
        #clear all input fields after successful submission
        self.id_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

        #clear extra fields
        self.source_entry.delete(0, tk.END)
        self.tax_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.importance_entry.delete(0, tk.END)
        self.freq_entry.delete(0, tk.END)
        self.nextdue_entry.delete(0, tk.END)
        self.needwant_entry.delete(0, tk.END)



    def create_view_transactions(self):
        frame = tk.Frame(self.container, bg="#1e1e2f")
        self.frames["view"] = frame

        # Title
        tk.Label(frame, text="Transactions", font=("Arial", 14)).pack(pady=10)

        # Table container
        self.table_frame = tk.Frame(frame)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Make columns expand evenly
        for col in range(5):
            self.table_frame.grid_columnconfigure(col, weight=1)

        # Back button
        tk.Button(frame, text="Back", command=lambda: self.show_frame("main")).pack(pady=10)


    def refresh_transactions(self):
        # Clear old table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Table headers
        headers = ["ID", "Date", "Amount", "Type", "Description"]

        for col, header in enumerate(headers):
            tk.Label(
                self.table_frame,
                text=header,
                borderwidth=1,
                relief="solid",
                bg="lightgray"
            ).grid(row=0, column=col, sticky="nsew")

        # Get transactions
        transactions = self.transaction_manager.view_transactions("transactions")

        # Fill table rows
        for row, t in enumerate(transactions, start=1):
            bg_color = "#f0f0f0" if row % 2 == 0 else "white"

            tk.Label(
                self.table_frame,
                text=t.get("ID"),
                borderwidth=1,
                relief="solid",
                bg=bg_color
            ).grid(row=row, column=0, sticky="nsew")

            tk.Label(
                self.table_frame,
                text=t.get("Date"),
                borderwidth=1,
                relief="solid",
                bg=bg_color
            ).grid(row=row, column=1, sticky="nsew")

            tk.Label(
                self.table_frame,
                text=t.get("Amount"),
                borderwidth=1,
                relief="solid",
                bg=bg_color
            ).grid(row=row, column=2, sticky="nsew")

            tk.Label(
                self.table_frame,
                text=t.get("Type"),
                borderwidth=1,
                relief="solid",
                bg=bg_color
            ).grid(row=row, column=3, sticky="nsew")

            tk.Label(
                self.table_frame,
                text=t.get("Description"),
                borderwidth=1,
                relief="solid",
                bg=bg_color
            ).grid(row=row, column=4, sticky="nsew")
       

    # ------------------ REPORT ------------------

    def create_report(self):
        frame = tk.Frame(self.container, bg="#1e1e2f")
        self.frames["report"] = frame
        # Title
        self.report_title = tk.Label(frame, text="Summary", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
        # Text output box
        self.report_text = tk.Text(frame, height=20, width=40)
        self.report_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        # Back button
        tk.Button(frame, text="Back", command=lambda: self.show_frame("main")).grid(row=2, column=0, columnspan=2, pady=10)

    def refresh_report(self):
        # Sets state to normal to start in order to allow editing
        self.report_text.config(state="normal")
        self.report_text.delete("1.0", tk.END)

        report = ReportGenerator(self.transaction_manager)
        summary = report.summary_report()
        breakdown = report.category_breakdown()

        self.report_text.insert(tk.END, "\n")
        for k, v in summary.items():
            self.report_text.insert(tk.END, f"{k}: {v}\n")

        self.report_text.insert(tk.END, "\nBreakdown:\n")
        for k, v in breakdown.items():
            self.report_text.insert(tk.END, f"{k}: {v}\n")
        # Locks text box to disable typing
        # call functions
        need_want = report.need_want()
        # heading for it in the report 
        self.report_text.insert(tk.END, "\nNeeds vs Wants:\n")
        # loops through dictionary and prints all the values 
        for k, v in need_want.items():
            self.report_text.insert(tk.END, f"{k}: {v}\n")
        #prevents anyone from typing in text box
        self.report_text.config(state="disabled")
    # ------------------ FORECAST ------------------
    def create_forecast(self):
        frame = tk.Frame(self.container, bg="#1e1e2f")
        self.frames["forecast"] = frame

        # Title
        tk.Label(frame, text="Forecast Report", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)
        # Text output box
        self.forecast_text = tk.Text(frame, height=15, width=40)
        self.forecast_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Back button
        tk.Button(frame, text="Back", command=lambda: self.show_frame("main")).grid(row=2, column=0, columnspan=2, pady=10)
    
    def refresh_forecast(self):
        # Opens text box to allow editing
        self.forecast_text.config(state="normal")
        self.forecast_text.delete("1.0", tk.END)

        forecast = ForecastService(self.transaction_manager)

        text = (
            "Forecasted Report:\n\n"
            f"Average Monthly expense: £{forecast.forecast_monthly_expenses()}\n"
            f"Average Income: £{forecast.forecast_income_amount()}\n"
            f"Current Balance: £{forecast.forecast_balance()}\n"
            f"Recurring bills (30 days): £{forecast.forecast_recurring_amount()}\n"
            f"Balance after recurring bills: £{forecast.forecast_balance_recurring()}\n"
        )

        self.forecast_text.insert(tk.END, text)

        # Locks text to disable editing
        self.forecast_text.config(state="disabled")
    # ------------------ BUDGET ------------------

    def create_budget(self):
        frame = tk.Frame(self.container, bg="#1e1e2f")
        self.frames["budget"] = frame

        tk.Label(frame, text="Budget Manager").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Enter the monthly budget:").grid(row=1, column=0, sticky="w", padx=10)

        self.budget_entry = tk.Entry(frame)
        self.budget_entry.grid(row=1, column=1, padx=10)

        tk.Button(frame, text="Calculate", command=self.handle_budget).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="Back", command=lambda: self.show_frame("main")).grid(row=10, column=0, columnspan=2)

        # Budget output hidden until used
        self.budget_output = tk.Label(frame, text="", justify="left", anchor="w")

        # Progress bar (canvas version)
        self.canvas = tk.Canvas(frame, width=250, height=25, bg="white", highlightthickness=1)
        self.canvas_bar = self.canvas.create_rectangle(0, 0, 0, 25, fill="green")
        self.canvas_text = self.canvas.create_text(125, 12, text="")

        #label for the category name the user wants to set a budget for
        tk.Label(frame, text="Category name:").grid(row=6, column=0, sticky="w", padx=10)

        #entry box for the category name
        self.category_budget_entry = tk.Entry(frame)
        self.category_budget_entry.grid(row=6, column=1, padx=10)
        #label for the category budget amount
        tk.Label(frame, text="Category budget:").grid(row=7, column=0, sticky="w", padx=10)
        #entry box for the budget amount
        self.category_budget_amount_entry = tk.Entry(frame)
        self.category_budget_amount_entry.grid(row=7, column=1, padx=10)
        #button that saves the category budget when clicked
        tk.Button( frame, text="Set Category Budget", command=self.handle_category_budget).grid(row=8, column=0, columnspan=2, pady=10)


    def handle_budget(self):
        self.cal_bud(self.budget_entry.get())


    def cal_bud(self, monthly_budget):
        # hide UI until valid input is confirmed
        self.budget_output.grid_forget()
        self.canvas.grid_forget()
        # validation to ensure input is correct
        if not is_valid_amount(monthly_budget):
            messagebox.showerror("Error", "Budget must be a number above 0")
            return
        # checks if there are no transactions to prevent errors
        if not self.transaction_manager.transactions:
            messagebox.showerror("Error", "No transactions found")
            return
        monthly_budget = float(monthly_budget)
        # stores the budget so it can be reused
        self.budget = BudgetManager(monthly_budget)
        
        # calculates values using budget manager
        total = self.budget.calculate_total_expenses(self.transaction_manager)
        remaining = self.budget.remaining_budget(self.transaction_manager)
        status = self.budget.budget_status(self.transaction_manager)
        
        # calculates percentage of budget used
        percentage = (total / monthly_budget) * 100
        percentage = max(0, min(percentage, 100))

        # update progress bar width
        bar_width = (percentage / 100) * 250
        self.canvas.coords(self.canvas_bar, 0, 0, bar_width, 25)

        # update progress bar colour
        if percentage < 70:
            color = "green"
        elif percentage < 100:
            color = "orange"
        else:
            color = "red"

        self.canvas.itemconfig(self.canvas_bar, fill=color)

        # update text
        self.canvas.itemconfig(self.canvas_text, text=f"{percentage:.2f}%")

        # show widgets only after valid budget
        self.budget_output.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        self.canvas.grid(row=5, column=0, columnspan=2, pady=10)
        # display result
        self.budget_output.config(text=f"Budget available\n" f"Total expenses:{total}\n"f"Remaining budget:{remaining}\n"f"Used:{percentage:.2f}%\n"f"{status}" )
       
       #gets the users category budget from the GUI and saves it
    def handle_category_budget(self):
        #gets the category entered by the user and removes extra spaces
        category = self.category_budget_entry.get().strip()
        #gets the budget amount entered by the user and removes extra spaces
        budget_amount = self.category_budget_amount_entry.get().strip()
        #checks that the category is not empty
        if not category:
            messagebox.showerror("Error", "Category cannot be empty")
            return
        #checks that the budget amount is a number above 0
        if not is_valid_amount(budget_amount):
            messagebox.showerror("Error", "Budget must be a number above 0")
            return
        #saves the category and budget amount into the transaction manager
        self.transaction_manager.set_category_budget(category, float(budget_amount))
        #shows the user that the budget has been set successfully
        messagebox.showinfo( "Budget Set", f"Budget set for {category}: £{float(budget_amount):.2f}"
    )   
          
if __name__ == "__main__":
  gui_cli = input("Enter 1 for CLI or 2 for GUI: ")
  if gui_cli == "2":
      app = App()
      app.mainloop()    
  else:
     manager = TransactionManager()
     menu = """
Welcome to the transaction manager
Enter 1 to add to the database
Enter 2 to view the database
Enter 3 to use the forecast service
Enter 4 to set a budget
Enter 5 for a report
Enter 6 to set a category budget  
Enter 0 to exit the program
"""
     while True:
        print(menu)
        try:
            choice = int(input("Enter your choice: "))
      
            if 0 <= choice <=6:
                if choice == 0:
                    print("closing program")
                    break

                elif choice == 1:
                    print("\n--- ADD TRANSACTION MODE ---")

                    while True:
                        ID = check_input_is_valid(
                            "Enter the ID of the transaction: ",
                            is_valid_integer,
                            "Enter an integer above 0"
                        )
                        ID = ID.strip()

                        exists = False
                        for t in manager.transactions:
                            if t.ID == ID:
                                exists = True

                        if not exists:
                            break
                        else:
                            print("This Id already exists")

                    Date = check_input_is_valid("Enter date (yyyy-mm-dd): ", is_valid_date, "Invalid date")
                    Amount = float(check_input_is_valid("Enter amount: ", is_valid_amount, "Invalid amount"))
                    Description = input("Enter Description: ")
                    type = check_input_is_valid(
                        "Type (Income, Expense, RecurringBill): ",
                        is_valid_type,
                        "Invalid type"
                    )
                    print("Creating transaction...")
                    if type == "Income":
                        Source = input("Enter Source: ")
                        isTaxable = check_input_is_valid("T or F: ", is_valid_bool, "Enter T or F")
                        T = Income(ID, Date, Amount, Description, Source, isTaxable)
                    elif type == "RecurringBill":
                        Frequency = check_input_is_valid("Frequency: ", is_valid_integer, "Invalid")
                        NextDueDate = check_input_is_valid("Next due date: ", is_valid_date, "Invalid date")
                        T = RecurringBill(ID, Date, Amount, Description, Frequency, NextDueDate)
                    elif type == "Expense":
                        Category = input("Enter Category: ")
                        ImportanceLevel = check_input_is_valid("1-10: ", valid_importance_level, "Invalid")
                        #ask user for the nput,lambda becomes the validate function 
                        NeedWant = check_input_is_valid( "Is this expense a Need or Want: ", lambda value: value.strip().capitalize() in ["Need", "Want"],  "Enter Need or Want" ).strip().capitalize()
                        bud_message=manager.check_cat_bud(Category,Amount)
                        if bud_message is not None:
                            print(bud_message)
                        T = Expense(ID, Date, Amount, Description, Category, ImportanceLevel,NeedWant)

                    manager.add_transaction(T)
                    print("Transaction successfully added!\n")             
                elif choice == 2:
                    data=manager.view_transactions("transactions")
                    print(data)
                #choice 3 
                elif choice == 3:
                    forecast=ForecastService(manager)
                    #call the alll the forcat methods from the class 
                    total_expense=forecast.forecast_monthly_expenses()
                    total_income=forecast.forecast_income_amount()
                    recurring_bills=forecast.forecast_recurring_amount()
                    total_balance=forecast.forecast_balance()
                    # These will print the visual message 
                    print(f"The average monly expense is £{total_expense}.")
                    print(f"the average income {total_income}.")
                    print(f"The current amount balance is £{total_balance}.")
                    print(f"The recurring bill amount due within 30 days  is £{recurring_bills}")
                #choice 4 
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
                #choice 6
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
                elif choice == 6:
                    category =input("Enter category name:").strip()
                    budget_amount=check_input_is_valid("Enter the amount:",is_valid_amount,"Enter a number above 0")
                    manager.set_category_budget(category, float(budget_amount))
            else:
             print("Number is out of range, Enter a number between 0 and 6")
        except ValueError:
            print("please enter an integer between 0 and 6")
