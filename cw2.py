
import json
import datetime

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
              item["Amount"],
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
                  item["Amount"],
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
                  item["Amount"],
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
    self.save_transactions("transactions")
    print("transaction added successfully")

  #prints database, may only need 218 - 221, if someone wants to test then you can
  def view_transactions(self, filename):
    try:
        with open(f"{filename}.json", "r") as f:
            print(json.load(f))
            return json.load(f)
    except FileNotFoundError:
        print("file doesnt exist already, creating database now")
        self.save_transactions(self, filename)
    except json.JSONDecodeError:
        print("save file is corrupted! Starting fresh")
        self.save_transactions(filename)

#  Simple forecasting calculations using transaction data.
class ForecastService:
  def __init__(self, transaction_manager):
      # Uses the same TransactionManager object so it can access stored transactions.
      self.manager = transaction_manager

  # Calculates the average expense amount.
  def forecast_monthly_expenses(self):
      expenses = [t.Amount for t in self.manager.transactions if isinstance(t, Expense)]
      if not expenses:
          return 0
      return sum(expenses) / len(expenses)

  # Calculates the average income amount and rounds it to 4 decimal places.
  def forecast_income_amount(self):
      incomes = [t.Amount for t in self.manager.transactions if isinstance(t, Income)]
      if not incomes:
          return 0
      return round(sum(incomes) / len(incomes), 2)

  # Returns all recurring bills stored in the transaction list.
  def forecast_recurring_bills(self):
      return [t for t in self.manager.transactions if isinstance(t, RecurringBill)]


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


if __name__ == "__main__":
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
        elif choice == 1:
          #need to check if id exists inside of the database already
          while user_error == 0:
            ID = check_input_is_valid("Enter the ID of the transaction: ", is_valid_integer, "Enter an integer above 0 that isnt in the database")  
            Date = check_input_is_valid("Enter the date of the expense: ", is_valid_date, "Enter date in format yyyy-mm-dd")
            Amount = check_input_is_valid("Insert the amount: ", is_valid_amount, "Enter a float above 0")
            Description = input("Enter Description: ")
            type = check_input_is_valid("enter the type of transaction: ", is_valid_type, "Enter a valid type of transaction")
            
            if type == "Income":
              Source = input("Enter the Source: ")
              isTaxable = check_input_is_valid("is it taxable T or F: ", is_valid_bool, "Enter T or F")
              
              T = Income(ID, Date, Amount, Description, Source, isTaxable)
              
            elif type == "Expense":
              Category = input("Enter the Category of expense: ")
              ImportanceLevel = check_input_is_valid("Enter Importance Level 1-10: ", is_valid_integer, "Enter an integer 0-10")
              T = Expense(ID, Date, Amount, Description, Category, ImportanceLevel)
              
            elif type == "Recurringbill":
              Frequency = check_input_is_valid("Enter the Frequency of expense: ", is_valid_integer, "Enter an integer above 0 that isnt in the database")
              NextDueDate = check_input_is_valid("When is the next due date: ", is_valid_date, "Enter date in format yyyy-mm-dd")
              T = RecurringBill(ID, Date, Amount, Description, Frequency, NextDueDate)
            else:
              print("wrong input")
              
            manager.add_transaction(T)
            break
          
        elif choice == 2:
          manager.view_transactions("transactions")
        elif choice == 3:
          pass
        elif choice == 4:
          pass
        elif choice == 5:
          pass
        else:
          print("Number is out of range, Enter a number between 0 and 5")
    except ValueError:
      print("please enter an integer between 0 and 5")
