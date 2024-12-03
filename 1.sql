-- Step 1: Create the Database
CREATE DATABASE CompanyDB;
GO

-- Step 2: Use the Database
USE CompanyDB;
GO

-- Step 3: Create the Employees Table
CREATE TABLE Employees (
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing Employee ID
    FirstName NVARCHAR(50) NOT NULL,          -- Employee's First Name
    LastName NVARCHAR(50) NOT NULL,           -- Employee's Last Name
    Position NVARCHAR(50) NOT NULL,           -- Job Position
    Department NVARCHAR(50) NOT NULL,         -- Department Name
    HireDate DATE NOT NULL,                   -- Date of Hiring
    Salary DECIMAL(10, 2) NOT NULL CHECK (Salary > 0), -- Monthly Salary must be positive
    Email NVARCHAR(100) UNIQUE NOT NULL       -- Email Address
);
GO

-- Step 2: Insert 100 Rows of Realistic Data
DECLARE @Counter INT = 1;

WHILE @Counter <= 100
BEGIN
    INSERT INTO Employees (FirstName, LastName, Position, Department, HireDate, Salary, Email)
    VALUES (
        CONCAT('Employee', @Counter),               -- Generate unique first names
        CONCAT('Last', @Counter),                   -- Generate unique last names
        CASE                                        -- Assign more diverse job titles
            WHEN @Counter % 10 = 1 THEN 'Software Engineer'
            WHEN @Counter % 10 = 2 THEN 'Project Manager'
            WHEN @Counter % 10 = 3 THEN 'HR Specialist'
            WHEN @Counter % 10 = 4 THEN 'Sales Executive'
            WHEN @Counter % 10 = 5 THEN 'Accountant'
            WHEN @Counter % 10 = 6 THEN 'Customer Support'
            WHEN @Counter % 10 = 7 THEN 'Marketing Manager'
            WHEN @Counter % 10 = 8 THEN 'Data Analyst'
            WHEN @Counter % 10 = 9 THEN 'DevOps Engineer'
            ELSE 'Product Manager'
        END,
        CASE                                        -- Assign realistic departments
            WHEN @Counter % 8 = 1 THEN 'IT'
            WHEN @Counter % 8 = 2 THEN 'HR'
            WHEN @Counter % 8 = 3 THEN 'Sales'
            WHEN @Counter % 8 = 4 THEN 'Finance'
            WHEN @Counter % 8 = 5 THEN 'Support'
            WHEN @Counter % 8 = 6 THEN 'Marketing'
            WHEN @Counter % 8 = 7 THEN 'Operations'
            ELSE 'R&D'
        END,
        DATEADD(DAY, -(@Counter * 5), GETDATE()),   -- Spread hire dates over time
        ROUND((RAND() * 40000) + 40000, 2),         -- Randomize salaries between 40,000 and 80,000
        CONCAT('employee', @Counter, '@company.com') -- Generate unique email addresses
    );

    SET @Counter = @Counter + 1;
END; 
