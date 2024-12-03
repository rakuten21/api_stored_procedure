-- Procedure for getting specific employee detail using employee id
CREATE PROCEDURE GetEmployeeDetails
    @EmployeeID INT
AS
BEGIN
    SELECT EmployeeID, FirstName, LastName, Position, Department, HireDate, Salary, Email
    FROM Employees
    WHERE EmployeeID = @EmployeeID;
END;