CREATE TABLE [dbo].[ExpensesByMonthByItems]
(
  ExpensesItemName VARCHAR(100),
  FactValue DECIMAL(20,2),
  PlanValue DECIMAL(20,2),
  [Period] DATE, 
  CONSTRAINT [PK_ExpensesByMonthByItems] PRIMARY KEY (ExpensesItemName,[Period])
)

GO
GRANT SELECT, INSERT,UPDATE, DELETE ON ExpensesByMonthByItems TO Python