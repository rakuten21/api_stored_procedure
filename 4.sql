-- Procedure for getting all of the employee details
CREATE PROCEDURE GetAllEmployees
AS
BEGIN
    SELECT EmployeeID, FirstName, LastName, Position, Department, HireDate, Salary, Email
    FROM Employees;
END;