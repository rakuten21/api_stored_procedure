-- Procedure for updating/editing employee details
CREATE PROCEDURE UpdateEmployee
    @EmployeeID INT,
    @FirstName NVARCHAR(50) = NULL,
    @LastName NVARCHAR(50) = NULL,
    @Position NVARCHAR(50) = NULL,
    @Department NVARCHAR(50) = NULL,
    @HireDate DATE = NULL,
    @Salary DECIMAL(10, 2) = NULL,
    @Email NVARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -- Update the employee's information
        UPDATE Employees
        SET 
            FirstName = COALESCE(@FirstName, FirstName),
            LastName = COALESCE(@LastName, LastName),
            Position = COALESCE(@Position, Position),
            Department = COALESCE(@Department, Department),
            HireDate = COALESCE(@HireDate, HireDate),
            Salary = COALESCE(@Salary, Salary),
            Email = COALESCE(@Email, Email)
        WHERE EmployeeID = @EmployeeID;

        -- Check if any rows were affected
        IF @@ROWCOUNT = 0
        BEGIN
            THROW 51000, 'No employee found with the given EmployeeID.', 1;
        END
    END TRY
    BEGIN CATCH
        -- Handle potential errors
        DECLARE @ErrorMessage NVARCHAR(4000);
        SET @ErrorMessage = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH;
END;
GO
