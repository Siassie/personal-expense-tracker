# app/db/repository/expenseRepo.py
from .base import BaseRepository
from app.db.models.expenses import Expenses
from app.db.schema.expense import ExpenseCreate
from typing import List, Optional

class ExpenseRepository(BaseRepository):

    def create_expense(self, expense_data: ExpenseCreate):
        new_expense = Expenses(**expense_data.model_dump(exclude_none=True))
        self.session.add(new_expense)
        self.session.commit()
        self.session.refresh(new_expense)
        return new_expense

    def get_expense_by_user_id(self, user_id: int) -> List[Expenses]:
        return self.session.query(Expenses).filter_by(user_id=user_id).all()

    def get_expense_by_expense_type(self, expense_type: str, user_id: int) -> List[Expenses]:
        return self.session.query(Expenses).filter_by(expense_type=expense_type, user_id=user_id).all()
