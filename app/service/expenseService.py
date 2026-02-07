# app/service/expenseService.py
from app.db.repository.expenseRepo import ExpenseRepository
from app.db.schema.expense import ExpenseCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

class ExpenseService:
    def __init__(self, session: Session):
        self.__expenseRepository = ExpenseRepository(session=session)

    def add_expense(self, expense_details: dict):
        from app.db.models.expenses import Expenses

        new_expense = Expenses(**expense_details)
        self.__expenseRepository.session.add(new_expense)
        self.__expenseRepository.session.commit()
        self.__expenseRepository.session.refresh(new_expense)
        return new_expense
    

    def get_all_expense_for_specific_user(self, user_id: int) -> List[ExpenseCreate]:
        expenses = self.__expenseRepository.get_expense_by_user_id(user_id=user_id)
        if not expenses:
            raise HTTPException(status_code=400, detail=f"No expenses found for user {user_id}.")
        return expenses

    def get_all_expense_for_specific_type(self, expense_type: str, user_id: int) -> List[ExpenseCreate]:
        expenses = self.__expenseRepository.get_expense_by_expense_type(expense_type=expense_type, user_id=user_id)
        if not expenses:
            raise HTTPException(status_code=400, detail=f"No expenses of type {expense_type} for user {user_id}.")
        return expenses
