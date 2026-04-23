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
  def __init__(self, transaction_manager):
      self.manager = transaction_manager

  def forecast_monthly_expenses(self):
      expenses = [t.Amount for t in self.manager.transactions if isinstance(t, Expense)]
      if not expenses:
          return 0
      return sum(expenses) / len(expenses)

  def forecast_monthly_income(self):
      incomes = [t.Amount for t in self.manager.transactions if isinstance(t, Income)]
      if not incomes:
          return 0
      return sum(incomes) / len(incomes)

  def forecast_recurring_bills(self):
      return [t for t in self.manager.transactions if isinstance(t, RecurringBill)]

class BudgetManager:
  def __init__(self, monthly_budget):
      self.monthly_budget = monthly_budget

  def calculate_total_expenses(self, transaction_manager):
      return sum(t.Amount for t in transaction_manager.transactions if isinstance(t, Expense))

  def remaining_budget(self, transaction_manager):
      spent = self.calculate_total_expenses(transaction_manager)
      return self.monthly_budget - spent

  def is_over_budget(self, transaction_manager):
      return self.remaining_budget(transaction_manager) < 0

  def budget_status(self, transaction_manager):
      remaining = self.remaining_budget(transaction_manager)

      if remaining < 0:
          return f" You are over budget by {abs(remaining)}"
      elif remaining < self.monthly_budget * 0.2:
          return f" Warning: Only {remaining} left in your budget"
      else:
          return f" You have {remaining} remaining"

class ReportGenerator:
    def __init__(self, transaction_manager):
        self.manager = transaction_manager

    def summary_report(self):
        incomes = [t.Amount for t in self.manager.transactions if isinstance(t, Income)]
        expenses = [t.Amount for t in self.manager.transactions if isinstance(t, Expense)]
        recurring = [t.Amount for t in self.manager.transactions if isinstance(t, RecurringBill)]

        return {
            "Total Income": sum(incomes),
            "Total Expenses": sum(expenses),
            "Total Recurring Bills": sum(recurring),
            "Net Balance": sum(incomes) - (sum(expenses) + sum(recurring))
        }

    def category_breakdown(self):
        breakdown = {}
        for t in self.manager.transactions:
            if isinstance(t, Expense):
                breakdown.setdefault(t.Category, 0)
                breakdown[t.Category] += t.Amount
        return breakdown

    def export_to_json(self, filename="transactions_export"):
        data = [
            t.to_database() if hasattr(t, "to_database") else t.__dict__
            for t in self.manager.transactions
        ]

        with open(f"{filename}.json", "w") as f:
            json.dump(data, f, indent=4)

        return f"{filename} saved successfully"

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
  

    
    
    
