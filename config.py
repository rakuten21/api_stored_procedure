import pyodbc  # Library to connect to SQL Server
import os  # Library for interacting with the operating system, used here to read environment variables
from dotenv import load_dotenv  # Library to load environment variables from a .env file

# Load the environment variables from the .env file
load_dotenv()

def get_db_connection():
    """
    Establishes a connection to the SQL Server database using the credentials
    stored in environment variables.
    """
    # Create a connection string using environment variables
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"  # Specify the ODBC driver for SQL Server
        f"SERVER={os.getenv('DB_SERVER')};"          # Get the server name from the environment
        f"DATABASE={os.getenv('DB_NAME')};"          # Get the database name from the environment
        f"Trusted_Connection=yes;"                   # Use Windows Authentication
    )

    return connection  # Return the active database connection
