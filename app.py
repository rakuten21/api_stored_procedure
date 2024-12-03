from flask import Flask, request, jsonify  # Flask for creating the API, request for parsing input, jsonify for sending JSON responses
import pyodbc  # Library for connecting to the SQL Server
from config import get_db_connection  # Custom configuration for getting a database connection
from flask_cors import CORS  # Enables Cross-Origin Resource Sharing

app = Flask(__name__)
CORS(app)  # Allows the API to be accessed from different origins (e.g., web browsers)

# -------------------------------
# Route: /get-employee?EmployeeID=[id]
# Purpose: Fetch details of a specific employee using their EmployeeID
# -------------------------------
@app.route('/get-employee', methods=['GET'])
def get_employee_details():
    # Extract EmployeeID from query parameters
    employee_id = request.args.get('EmployeeID')

    # If no EmployeeID is provided, return an error
    if not employee_id:
        return jsonify({'error': 'Please provide EmployeeID'}), 400

    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Call the stored procedure with the provided EmployeeID
        cursor.execute("EXEC GetEmployeeDetails ?", (employee_id,))
        result = cursor.fetchall()

        # If no employee is found, return a 404 error
        if not result:
            return jsonify({'error': 'No employee found with the given EmployeeID'}), 404

        # Format the result into a list of dictionaries
        employees = []
        for row in result:
            employees.append({
                'EmployeeID': row.EmployeeID,
                'FirstName': row.FirstName,
                'LastName': row.LastName,
                'Position': row.Position,
                'Department': row.Department,
                'HireDate': row.HireDate.strftime('%Y-%m-%d'),
                'Salary': float(row.Salary),
                'Email': row.Email
            })

        # Return the employee details as JSON
        return jsonify(employees)

    except Exception as e:
        # Return a 500 error if something goes wrong
        return jsonify({'error': str(e)}), 500

    finally:
        # Ensure the database connection is closed
        cursor.close()
        conn.close()

# -------------------------------
# Route: /get-employees
# Purpose: Fetch details of all employees
# -------------------------------
@app.route('/get-employees', methods=['GET'])
def get_all_employees():
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Call the stored procedure to fetch all employees
        cursor.execute("EXEC GetAllEmployees")
        result = cursor.fetchall()

        # If no employees are found, return a 404 message
        if not result:
            return jsonify({'message': 'No employees found'}), 404

        # Format the result into a list of dictionaries
        employees = []
        for row in result:
            employees.append({
                'EmployeeID': row.EmployeeID,
                'FirstName': row.FirstName,
                'LastName': row.LastName,
                'Position': row.Position,
                'Department': row.Department,
                'HireDate': row.HireDate.strftime('%Y-%m-%d') if row.HireDate else None,
                'Salary': float(row.Salary) if row.Salary else 0.0,
                'Email': row.Email
            })

        # Return the list of employees as JSON
        return jsonify(employees)

    except Exception as e:
        # Return a 500 error if something goes wrong
        return jsonify({'error': str(e)}), 500

    finally:
        # Ensure the database connection is closed
        cursor.close()
        conn.close()

# -------------------------------
# Route: /add-employee
# Purpose: Add a new employee
# -------------------------------
@app.route('/add-employee', methods=['POST'])
def add_employee():
    try:
        # Parse the JSON request body
        data = request.get_json()
        
        # Ensure all required fields are provided
        required_fields = ['FirstName', 'LastName', 'Position', 'Department', 'HireDate', 'Salary', 'Email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Call the stored procedure to add the employee
        cursor.execute(
            "EXEC AddEmployee ?, ?, ?, ?, ?, ?, ?",
            (
                data['FirstName'],
                data['LastName'],
                data['Position'],
                data['Department'],
                data['HireDate'],
                data['Salary'],
                data['Email']
            )
        )
        
        # Fetch the newly created EmployeeID
        result = cursor.fetchone()
        new_employee_id = result.NewEmployeeID if result else None

        # Commit the transaction
        conn.commit()

        # Return a success message with the new EmployeeID
        return jsonify({'message': 'Employee added successfully', 'EmployeeID': new_employee_id}), 201

    except Exception as e:
        # Return a 500 error if something goes wrong
        return jsonify({'error': str(e)}), 500

    finally:
        # Ensure the database connection is closed
        cursor.close()
        conn.close()

# -------------------------------
# Route: /edit-employee/<EmployeeID>
# Purpose: Edit an existing employee's details
# -------------------------------
@app.route('/edit-employee/<int:EmployeeID>', methods=['PUT'])
def edit_employee(EmployeeID):
    try:
        # Parse the JSON request body
        data = request.get_json()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Call the stored procedure to update the employee
        cursor.execute(
            "EXEC UpdateEmployee ?, ?, ?, ?, ?, ?, ?, ?",
            (
                EmployeeID,  # Use EmployeeID from the URL
                data.get('FirstName'),
                data.get('LastName'),
                data.get('Position'),
                data.get('Department'),
                data.get('HireDate'),
                data.get('Salary'),
                data.get('Email')
            )
        )

        # Commit the transaction
        conn.commit()

        # Return a success message
        return jsonify({'message': 'Employee details updated successfully'}), 200

    except Exception as e:
        # Return a 500 error if something goes wrong
        return jsonify({'error': str(e)}), 500

    finally:
        # Ensure the database connection is closed
        cursor.close()
        conn.close()

# -------------------------------
# Route: /delete-employee/<EmployeeID>
# Purpose: Delete an employee
# -------------------------------
@app.route('/delete-employee/<int:EmployeeID>', methods=['DELETE'])
def delete_employee(EmployeeID):
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Call the stored procedure to delete the employee
        cursor.execute("EXEC DeleteEmployee ?", (EmployeeID,))
        
        # Commit the transaction
        conn.commit()

        # Return a success message
        return jsonify({'message': 'Employee deleted successfully'}), 200

    except Exception as e:
        # Return a 500 error if something goes wrong
        return jsonify({'error': str(e)}), 500

    finally:
        # Ensure the database connection is closed
        cursor.close()
        conn.close()

# -------------------------------
# Entry Point
# Purpose: Run the Flask app in debug mode
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
