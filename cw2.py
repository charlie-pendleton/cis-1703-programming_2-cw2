import json
import datetime

#add all user inputs to a list, they dont need uniform attributes meaning expenses and incomes can have differnt end attributes.
#filter by the attributes youy want
#when making table get the type of transaction, then filter by just that so then its organised

class Transaction:
  def __init__(self, ID, Date, Amount, Description):
    self.ID = ID
    self.Date = Date
    self.Amount = Amount
    self.Description = Description
    
  def to_database(self):
    return {
        "ID": self.ID,
        "Date": self.Date,
        "Amount": self.Amount,
        "Description": self.Description
    }
    
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}"
    
class Income(Transaction):
  def __init__(self, ID, Date, Amount, Description, Source, isTaxable):
    super().__init__(ID, Date, Amount, Description)
    self.Source = Source
    self.isTaxable = isTaxable
    
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Income, Source: {self.Source}, isTaxable: {self.isTaxable}"
    
  def to_database(self):
    data = super().to_database()
    data["Type"] = "Income"
    data["Source"] = self.Source
    data["IsTaxable"] = self.isTaxable
    return data


class Expense(Transaction):
  def __init__(self, ID, Date, Amount, Description, Category, ImportanceLevel):
    super().__init__(ID, Date, Amount, Description)
    self.Category = Category
    self.ImportanceLevel = ImportanceLevel
    
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Expense, Category: {self.Category}, ImportanceLevel: {self.ImportanceLevel}"
    
class RecurringBill(Transaction):
  def __init__(self, ID, Date, Amount, Description, Frequency, NextDueDate):
    super().__init__(ID, Date, Amount, Description)
    self.Frequency = Frequency
    self.NextDueDate = NextDueDate
    
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Recurring, Frequency: {self.Frequency}, NextDueDate: {self.NextDueDate}"
    
class TransactionManager:
  def __init__(self):
    self.transactions = []
    
  # def save_inventory(filename, expenses):
  #   with open(f"{filename}.json", "w") as f:
  #       json.dump(expenses, f, indent=4)
    
  def add_transaction(self, transaction):
    self.transactions.append(transaction)

  
  def view_transactions(self):
    for t in self.transactions:
      print(t)
  
  def categorise_expense(self):
    pass
  
  # def __str__(self):
  #   return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}"
  
  
class ForecastService:
  pass

class BudgetManager:
  pass

class ReportGenerator:
  pass

if __name__ == "__main__":
  manager = TransactionManager()
  while True:
    
    ID = input("Enter ID: ")
    Date = input("Enter Date")
    Amount = float(input("Insert the amount: "))
    Description = input("Enter Description: ")
    type = input("enter the type: ")
    
    if type == "income":
      Source = input("Enter the Source: ")
      isTaxable = input("is it taxable True or False")
      T = Income(ID, Date, Amount, Description, Source, isTaxable)
      
    elif type == "expense":
      Category = input("Enter the Category of expense: ")
      ImportanceLevel = input("Enter Importnce Level")
      T = Expense(ID, Date, Amount, Description, Category, ImportanceLevel)
      
    elif type == "recurringbill":
      Frequency = input("Enter the Frequency of expense: ")
      NextDueDate = input("When is the next due date: ")
      T = RecurringBill(ID, Date, Amount, Description, Frequency, NextDueDate)
    else:
      print("worng input")
    # T = Transaction(ID, Date, Amount, Description)
    # print(T)
    
    manager.add_transaction(T)
    manager.view_transactions()
  

    
    
    