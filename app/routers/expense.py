from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.schema.expense import ExpenseCreate, ExpenseRead
from app.service.expenseService import ExpenseService
from app.util.protectRoute import get_current_user_id  # make sure this returns int
from typing import List

expenseRouter = APIRouter(prefix="/expenses", tags=["Expenses"])

@expenseRouter.post("/", response_model=ExpenseRead, status_code=201)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user_id)  # <- must be int user_id
):
    service = ExpenseService(db)

    full_expense = {
        "user_id": current_user,
        "expense_name": expense.expense_name,
        "amount": expense.amount,
        "expense_type": expense.expense_type
    }

    return service.add_expense(expense_details=full_expense)


@expenseRouter.get("/user/{user_id}", response_model=List[ExpenseRead])
def get_user_expenses(user_id: int, db: Session = Depends(get_db)):
    service = ExpenseService(db)
    return service.get_all_expense_for_specific_user(user_id)

@expenseRouter.get("/user/{user_id}/type/{expense_type}", response_model=List[ExpenseRead])
def get_user_expenses_by_type(user_id: int, expense_type: str, db: Session = Depends(get_db)):
    service = ExpenseService(db)
    return service.get_all_expense_for_specific_type(expense_type, user_id)
