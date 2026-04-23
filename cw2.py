import json
from datetime import datetime, timedelta
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

#class to manage transactions
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
  

  
  # def __str__(self):
  #   return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}"
  
  
class ForecastService:
    def __init__(self, filename="transactions"):
      self.current_date = datetime.now()
      self.future_date = self.current_date + timedelta(days=30)
      self.filename = filename
      #Lists of all database inputs
      self.transactionsexpense = []
      self.transactionsincome = []
      self.transactionsrecurring = []
      self.transactionsrecurring_filtered = []
      #Floats used for calculating forecast
      self.total_balance = float(0)
      self.total_income = float(0)
      self.total_expense = float(0)
      self.total_recurring = float(0)
      
      #opens database and stores it inside of data
      try: 
        with open(f"{filename}.json", "r") as f:
          data =json.load(f)
        #loops through data and then gets the type and adds them to the dictionary inside each type
        for item in data:
          tx_type = item.get("Type")

          if tx_type == "Income":
            self.transactionsincome.append(
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
            self.transactionsexpense.append(
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
            self.transactionsrecurring.append(
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

    #Works out all recurring bills and filters them for only ones due in the next 30 days
    def recurringbills(self):
      self.transactionsrecurring_filtered.clear()
       
      for bill in self.transactionsrecurring:
        # convert NextDueDate to datetime
        due_date = datetime.strptime(bill.NextDueDate, "%Y-%m-%d")

        #Checks if its within the next 30 days
        if self.current_date <= due_date <= self.future_date:
          self.transactionsrecurring_filtered.append(bill)
      return self.transactionsrecurring_filtered

    #Works out all income added to the database to store it in a value
    def totalincome(self):
      totalincomes = float(sum(tx.Amount for tx in self.transactionsincome))
      self.total_income = totalincomes
      return self.total_income
  
    #Works out all expenses added to the database to store it in a value
    def totalexpense(self):
      totalexpenses = float(sum(tx.Amount for tx in self.transactionsexpense)) 
      self.total_expense = totalexpenses
      return self.total_expense

    #Works out all recurring expenses in the next 30 days and stores it in a value 
    def totalrecurring(self):
      self.transactionsrecurring_filtered = self.recurringbills()
      self.total_recurring =  float(sum(tx.Amount for tx in self.transactionsrecurring_filtered)) 
      return self.total_recurring
    
    #Works out the total balance before recurring bills are taken away
    def totalbalance(self):
      income = self.totalincome()
      expense = self.totalexpense()
      self.total_balance = float(income)-float(expense)
      return self.total_balance

    def forecast(self):
      balance = self.totalbalance()
      recurring = self.totalrecurring()

      total_balance = float(balance)-float(recurring)
      if balance < 0:
        print(f"""Balance is in the Negatives.
Your current balance is £{balance}
Please add more money before your reccuring bills come out to get out of your overdraft.
After recurring payments are taken out you will have £{total_balance}.""")
        
      elif balance == 0:
        print(f"""Balance is £0.
Please add more money before your recurring bills come out to get out of your overdraft.
After recurring bills come out you will have £{total_balance}.""")
        
      elif balance > 0 and recurring > balance:
       print(f"""Balance is in the Positives.
Your current balance is £{balance}
Please add more money before your recurring bills come out to get out of your overdraft.
After they are taken out you will have £{total_balance}.""") 
      
      elif balance > 0 and recurring == balance:
        print(f"""Balance is in the Positives.
Your current balance is £{balance}
Please add more money before your recurring bills come out to stay above £0
After they are taken out you will have £{total_balance}.""") 
      else:
        print(f"""Balance is in the Positives.
              Your current balance is £{balance}.
              After recurring payments are taken out you will have £{total_balance} left.""")

      

      




       

    


class BudgetManager:
  pass

class ReportGenerator:
  pass


if __name__ == "__main__":
  manager = TransactionManager()
  forecastservice = ForecastService()
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
          forecastservice.forecast()
        elif choice == 4:
          pass
        elif choice == 5:
          pass
        else:
          print("Number is out of range, Enter a number between 0 and 5")
    except ValueError:
      print("please enter an integer between 0 and 5")
    
    
    
    # T = Transaction(ID, Date, Amount, Description)
    # print(T)
    
    
    
  

    
    
    
