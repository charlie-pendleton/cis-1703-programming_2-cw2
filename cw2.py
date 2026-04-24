import json
import datetime

# Base class used for all transaction types.
# Income, Expense and RecurringBill inherit shared attributes from this class.
class Transaction:
  def __init__(self, ID, Date, Amount, Description):
    # Stores the basic details that every transaction needs
    self.ID = ID
    self.Date = Date
    self.Amount = Amount
    self.Description = Description

  # Converts the transaction  into a dictionary.
  def to_database(self):
    return {
        "ID": self.ID,
        "Date": self.Date,
        "Amount": self.Amount,
        "Description": self.Description
    }

  # Returnsthe transaction 
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}"



# It adds income-specific details such as source and tax status.
class Income(Transaction):
  def __init__(self, ID, Date, Amount, Description, Source, isTaxable):
    # Calls the parent Transaction constructor to reuse shared attributes
    super().__init__(ID, Date, Amount, Description)
    self.Source = Source
    self.isTaxable = isTaxable

  # Displays income details 
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Income, Source: {self.Source}, isTaxable: {self.isTaxable}"

  # Adds income specific fields before saving to JSON.
  def to_database(self):
    data = super().to_database()
    data["Type"] = "Income"
    data["Source"] = self.Source
    data["IsTaxable"] = self.isTaxable
    return data



# It adds category and importance level.
class Expense(Transaction):
  def __init__(self, ID, Date, Amount, Description, Category, ImportanceLevel):
    super().__init__(ID, Date, Amount, Description)
    self.Category = Category
    self.ImportanceLevel = ImportanceLevel

  # Displays expense details 
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Expense, Category: {self.Category}, ImportanceLevel: {self.ImportanceLevel}"


# RecurringBill is used for regular payments such as rent, subscriptions or bills.
class RecurringBill(Transaction):
  def __init__(self, ID, Date, Amount, Description, Frequency, NextDueDate):
    super().__init__(ID, Date, Amount, Description)
    self.Frequency = Frequency
    self.NextDueDate = NextDueDate

  # Displays recurring bill details 
  def __str__(self):
    return f"ID: {self.ID}, Date: {self.Date}, Amount: {self.Amount}, Description: {self.Description}, Type: Recurring, Frequency: {self.Frequency}, NextDueDate: {self.NextDueDate}"


# Manages the list of transactions in the program.
class TransactionManager:
  def __init__(self):
    # Stores all transaction in one list.
    self.transactions = []

  # Adds a new transaction  to the list.
  def add_transaction(self, transaction):
    self.transactions.append(transaction)

  # Prints all transactions currently stored.
  def view_transactions(self):
    for t in self.transactions:
      print(t)

  # Intended to group expenses by category.
  def categorise_expense(self):
    pass


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

  # Ask the user to enter a value until they close the program 
  while True:

    # Gets the shared transaction information from the user.
    ID = input("Enter ID: ")
    Date = input("Enter Date")
    Amount = float(input("Insert the amount: "))
    Description = input("Enter Description: ")
    type = input("enter the type: ")

    # Creates an Income object if the user enters income.
    if type == "income":
      Source = input("Enter the Source: ")
      isTaxable = input("is it taxable True or False")
      T = Income(ID, Date, Amount, Description, Source, isTaxable)

    # Creates an Expense object if the user enters expense.
    elif type == "expense":
      Category = input("Enter the Category of expense: ")
      ImportanceLevel = input("Enter Importnce Level")
      T = Expense(ID, Date, Amount, Description, Category, ImportanceLevel)

    # Creates a RecurringBill object if the user enters recurringbill.
    elif type == "recurringbill":
      Frequency = input("Enter the Frequency of expense: ")
      NextDueDate = input("When is the next due date: ")
      T = RecurringBill(ID, Date, Amount, Description, Frequency, NextDueDate)

    # Handles invalid transaction 
    else:
      print("worng input")

    # Adds the created transaction object to the manager.
    manager.add_transaction(T)

    # Displays all stored transactions after each new entry.
    manager.view_transactions()
    
    
    
