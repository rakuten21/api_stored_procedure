-- Procedure for deleting employee detail
CREATE PROCEDURE DeleteEmployee
    @EmployeeID INT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -- Attempt to delete the employee
        DELETE FROM Employees
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