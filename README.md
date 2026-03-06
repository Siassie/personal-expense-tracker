# Personal Expense Tracker

    A FastAPI backend API with a Python CLI client to manage personal expenses. Users can sign up, log in, add expenses, view them, and filter by type.


    The system allows users to:

        - Create an account
        - Authenticate with JWT tokens
        - Add expenses
        - View all their expenses
        - Filter expenses by type

    
    Expense types supported:
     
        Code  |  Meaning 
        d	  |  Daily   
        m	  |  Monthly 
        y	  |  Yearly  



Architecture Overview

    The project follows a layered architecture commonly used in backend applications.

    CLI Client
    │
    ▼
    FastAPI Routers
    │
    ▼
    Services (Business Logic)
    │
    ▼
    Repositories (Database Access)
    │
    ▼
    SQLAlchemy Models
    │
    ▼
    PostgreSQL Database


    Each layer has a specific responsibility.

    Layer         |   Responsibility
    CLI           |   User interaction
    Routers       |   API endpoints
    Services      |   Business logic
    Repositories  |   Database queries
    Models	      |   Database structure
    Schemas	      |   Data validation



Project Structure

    personal-expense-tracker
    │
    ├── cli.py
    ├── main.py
    ├── .env
    │
    ├── app
    │   ├── core
    │   │   ├── database.py
    │   │   └── security
    │   │        ├── authHandler.py
    │   │        └── hashHelper.py
    │   │
    │   ├── db
    │   │   ├── models
    │   │   │    ├── user.py
    │   │   │    └── expense.py
    │   │   │
    │   │   ├── repository
    │   │   │    ├── base.py
    │   │   │    ├── userRepo.py
    │   │   │    └── expenseRepo.py
    │   │
    │   ├── schema
    │   │   ├── user.py
    │   │   └── expense.py
    │   │
    │   ├── routers
    │   │   ├── auth.py
    │   │   └── expense.py
    │   │
    │   ├── service
    │   │   ├── userService.py
    │   │   └── expenseService.py
    │   │
    │   └── util
    │        ├── init_db.py
    │        └── protectRoute.py



Dependencies

    Required Python packages:

        - fastapi
        - uvicorn
        - sqlalchemy
        - psycopg2
        - bcrypt
        - python-decouple
        - PyJWT
        - requests
        - pydantic


    Install them:

        command:
            pip install fastapi uvicorn sqlalchemy psycopg2-binary bcrypt python-decouple pyjwt requests pydantic



Environment Configuration

    .env:

        JWT_SECRET=j8MNO8ytRj5oXMh4cELPMQEhj145ZvR0BBAXeKAZyiz
        JWT_ALGORITHM=HS256


    Used by:

        - AuthHandler
        - protectRoute
        - CLI token decoding

    

Database Configuration

    File:

        app/core/database.py


    Connection string:

        postgresql://user:password@localhost:5432/postgres


    Meaning:

        Part       |   Description
        user       |   PostgreSQL username
        password   |   PostgreSQL password
        localhost  |   Database host
        5432       |   Default PostgreSQL port
        postgres   |   Database name

    The project uses SQLAlchemy ORM.

    
    Session creation

        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )


    Each request receives its own session using:

        - get_db()



Database Schema

    - Two tables exist.



User Table

    Model:

        app/db/models/user.py:

            Column        Type          Description

            id            Integer       Primary key
            first_name    String(50)    User first name
            last_name     String(100)   User last name
            email         String(70)    Unique login email
            password      String(250)   Hashed password
            

    Relationship:

        expenses = relationship("Expenses", back_populates="user", cascade="all, delete")

        This means:

            - One user can have many expenses
            - Deleting a user deletes all their expenses



Expenses Table

    Model:

        app/db/models/expense.py:

            Column          Type          Description

            id              Integer       Primary key
            user_id         Integer       Foreign key
            expense_name    String(50)    Name of expense
            amount          Float         Expense amount
            expense_type    String(1)     d, m, or y

    
    Relationship:

        user = relationship("User", back_populates="expenses")



Authentication System

    The system uses JWT tokens.


    Implementation:

        app/core/security/authHandler.py:

            Token payload
            payload = {
                "user_id": user_id,
                "expires": time.time() + 900
            }


    Token lifetime:

        - 900 seconds = 15 minutes

    
    Token algorithm:

        - HS256


    JWT library used:

        - PyJWT



Password Security

    Passwords are hashed using bcrypt.


    File:

        - app/core/security/hashHelper.py


    Hashing:

        - hashpw(password, gensalt())


    Verification:

        - checkpw(plain, hashed)


    bcrypt is widely used for password hashing because it is designed to be computationally slow, making brute-force attacks harder.



Database Initialization

    Tables are created automatically when the server starts.

    
    File:

        - app/util/init_db.py
        - Base.metadata.create_all(bind=engine)


    Called in main.py lifespan event.



API Endpoints

    Root Endpoint:

        GET /

    
    Response:

        {
        "message": "API is running"
        }



Signup

    POST /auth/signup


    Request body:

        {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@email.com",
        "password": "123456"
        }


    Response:

        {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@email.com"
        }



Login

    POST /auth/login


    Request:

        {
        "email": "john@email.com",
        "password": "123456"
        }


    Response:

        {
        "token": "JWT_TOKEN"
        }



Add Expense

    POST /expenses/


    Requires:

        Authorization: 
            
            Bearer <token>


    Request:

        {
        "expense_name": "Rent",
        "amount": 5000,
        "expense_type": "m"
        }


    Response:

        {
        "id": 1,
        "user_id": 1,
        "expense_name": "Rent",
        "amount": 5000,
        "expense_type": "m"
        }



Get User Expenses

    GET /expenses/user/{user_id}


    Example:

        GET /expenses/user/1


    Returns:

        [
        {
            "id": 1,
            "user_id": 1,
            "expense_name": "Rent",
            "amount": 5000,
            "expense_type": "m"
        }
        ]



Get Expenses by Type

    GET /expenses/user/{user_id}/type/{expense_type}


    Example:

        GET /expenses/user/1/type/m


    Protected Route Example
        
        GET /protected

    Requires token.
    

    Returns:

        {
        "data": 1
        }

    Where 1 is the authenticated user id.



CLI Application

    File:

        cli.py

    The CLI communicates with the API using the requests library.

    
    Base URL:

        http://127.0.0.1:8000



CLI Menu

    When started:

        === Expense Tracker CLI ===

        1 Login
        2 Signup
        3 Add Expense
        4 View My Expenses
        5 View Expenses by Type
        6 Exit



CLI Flow

    Login


    Requests:

        POST /auth/login


    Stores token globally:

        TOKEN



Add Expense

    Steps:

        1 Validate user logged in
        2 Decode token
        3 Send POST request



View Expenses

    Steps:

        1 Call /protected
        2 Extract user id
        3 Request /expenses/user/{id}



Running the Project

    1. Install dependencies
        pip install fastapi uvicorn sqlalchemy psycopg2-binary bcrypt python-decouple pyjwt requests pydantic


    2. Start PostgreSQL
        Ensure PostgreSQL is running and matches:

            postgresql://user:password@localhost:5432/postgres


    3. Run API
        uvicorn main:app --reload


        Server runs at:

            http://127.0.0.1:8000

        
        Swagger docs:

            http://127.0.0.1:8000/docs


    4. Run CLI
        Open another terminal:

            python cli.py
        
        
        Example Usage Flow:

            Signup
            ↓
            Login
            ↓
            Add expense
            ↓
            View expenses
            ↓
            Filter by type


    
Security Notes

    Current security implementation:

        Feature	             |  Status

        Password hashing     |  bcrypt
        Authentication       |  JWT
        Token expiry         |  15 minutes
        Protected endpoints  |  Yes



Known Limitations
    - Expenses endpoint allows requesting another user's expenses if their ID is known.
    - ExpenseService duplicates repository logic instead of using create_expense.
    - Token expiration is handled manually rather than using JWT exp claim.
    - No refresh tokens implemented.



Possible Improvements

    - Pagination for expenses
    - Expense categories
    - Expense deletion
    - Expense updates
    - Token refresh system
    - Rate limiting
    - Docker deployment
