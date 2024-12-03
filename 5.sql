-- Procedure for adding employee details
-- Create the AddEmployee procedure
CREATE PROCEDURE AddEmployee
    @FirstName NVARCHAR(50),
    @LastName NVARCHAR(50),
    @Position NVARCHAR(50),
    @Department NVARCHAR(50),
    @HireDate DATE,
    @Salary DECIMAL(10, 2),
    @Email NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Insert the new employee
    BEGIN TRY
        INSERT INTO Employees (FirstName, LastName, Position, Department, HireDate, Salary, Email)
        VALUES (@FirstName, @LastName, @Position, @Department, @HireDate, @Salary, @Email);
        
        SELECT SCOPE_IDENTITY() AS NewEmployeeID; -- Return the new EmployeeID
    END TRY
    BEGIN CATCH
        -- Handle potential errors
        DECLARE @ErrorMessage NVARCHAR(4000);
        SET @ErrorMessage = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH;
END;
GO
