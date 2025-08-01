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

-- Insert sample books
INSERT INTO Book (title, author, isbn, publication_year, genre, total_copies, available_copies) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 1925, 'Fiction', 3, 2),
('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 1960, 'Fiction', 2, 1),
('1984', 'George Orwell', '978-0-452-28423-4', 1949, 'Dystopian Fiction', 4, 3),
('Pride and Prejudice', 'Jane Austen', '978-0-14-143951-8', 1813, 'Romance', 2, 2),
('The Catcher in the Rye', 'J.D. Salinger', '978-0-316-76948-0', 1951, 'Fiction', 3, 1),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', '978-0-439-70818-8', 1997, 'Fantasy', 5, 4),
('The Lord of the Rings', 'J.R.R. Tolkien', '978-0-544-00341-5', 1954, 'Fantasy', 3, 2),
('Database System Concepts', 'Abraham Silberschatz', '978-0-07-352332-3', 2019, 'Computer Science', 2, 2),
('Introduction to Algorithms', 'Thomas H. Cormen', '978-0-262-03384-8', 2009, 'Computer Science', 3, 3),
('Clean Code', 'Robert C. Martin', '978-0-13-235088-4', 2008, 'Computer Science', 2, 1);

-- Insert sample members
INSERT INTO Member (first_name, last_name, email, phone, street, city, state, zip_code, join_date) VALUES
('John', 'Smith', 'john.smith@email.com', '513-555-0101', '123 Main St', 'Cincinnati', 'OH', '45202', '2024-01-15'),
('Emily', 'Johnson', 'emily.johnson@email.com', '513-555-0102', '456 Oak Ave', 'Cincinnati', 'OH', '45203', '2024-02-20'),
('Michael', 'Brown', 'michael.brown@email.com', '513-555-0103', '789 Pine Rd', 'Cincinnati', 'OH', '45204', '2024-03-10'),
('Sarah', 'Davis', 'sarah.davis@email.com', '513-555-0104', '321 Elm St', 'Cincinnati', 'OH', '45205', '2024-04-05'),
('David', 'Wilson', 'david.wilson@email.com', '513-555-0105', '654 Maple Dr', 'Cincinnati', 'OH', '45206', '2024-05-12'),
('Lisa', 'Anderson', 'lisa.anderson@email.com', '513-555-0106', '987 Cedar Ln', 'Cincinnati', 'OH', '45207', '2024-06-18'),
('James', 'Taylor', 'james.taylor@email.com', '513-555-0107', '147 Birch St', 'Cincinnati', 'OH', '45208', '2024-07-01'),
('Jennifer', 'Martinez', 'jennifer.martinez@email.com', '513-555-0108', '258 Walnut Ave', 'Cincinnati', 'OH', '45209', '2024-07-15');

-- Insert sample staff
INSERT INTO Staff (first_name, last_name, role, email, phone, hire_date) VALUES
('Alice', 'Cooper', 'Head Librarian', 'alice.cooper@library.org', '513-555-0201', '2020-08-15'),
('Bob', 'Richards', 'Assistant Librarian', 'bob.richards@library.org', '513-555-0202', '2021-06-01'),
('Carol', 'Thompson', 'Library Clerk', 'carol.thompson@library.org', '513-555-0203', '2022-09-12'),
('Daniel', 'Garcia', 'Library Assistant', 'daniel.garcia@library.org', '513-555-0204', '2023-03-20');

-- Insert sample loans
INSERT INTO Loan (member_id, book_id, loan_date, due_date, return_date, status) VALUES
-- Active loans
(1, 1, '2025-07-20', '2025-08-03', NULL, 'Active'),
(2, 5, '2025-07-25', '2025-08-08', NULL, 'Active'),
(3, 7, '2025-07-28', '2025-08-11', NULL, 'Active'),
(4, 10, '2025-07-29', '2025-08-12', NULL, 'Active'),

-- Overdue loans
(5, 2, '2025-07-10', '2025-07-24', NULL, 'Overdue'),
(6, 5, '2025-07-05', '2025-07-19', NULL, 'Overdue'),

-- Returned loans
(1, 3, '2025-07-01', '2025-07-15', '2025-07-14', 'Returned'),
(2, 6, '2025-07-05', '2025-07-19', '2025-07-18', 'Returned'),
(3, 8, '2025-07-10', '2025-07-24', '2025-07-22', 'Returned'),
(7, 9, '2025-07-15', '2025-07-29', '2025-07-28', 'Returned');