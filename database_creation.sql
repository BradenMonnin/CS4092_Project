CREATE TABLE Book (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    publication_year INTEGER NOT NULL,
    genre TEXT,
    total_copies INTEGER NOT NULL CHECK (total_copies > 0),
    available_copies INTEGER NOT NULL CHECK (available_copies >= 0),
    CONSTRAINT check_available_copies CHECK (available_copies <= total_copies)
);

CREATE TABLE Member (
    member_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE Staff (
    staff_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE Loan (
    loan_id INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    status TEXT NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Returned', 'Overdue')),
    FOREIGN KEY (member_id) REFERENCES Member(member_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id)
);