import os
import pandas as pd
import sqlite3

# Root directory containing lakes directories
root_directory = '/home/dmercado/calibration_local_lakes/files_ok/'  # Replace with the appropriate path

# Create an empty list to store the results
results_data = []

# Iterate through directories in search of "calibration.db" files
for dir_lake in os.listdir(root_directory):
            print(dir_lake)
            lake = dir_lake  # Lake name is the directory name
            db_file = os.path.join(root_directory, dir_lake, 'calibration.db')

            # Check if the database file exists and is not empty
            #if os.path.isfile(db_file) and os.path.getsize(db_file) > 0:
            if os.path.isfile(db_file):
                print(lake)
                # Connect to the SQLite database
                connection = sqlite3.connect(db_file)

                # Use Pandas to read the SQLite table into a DataFrame
                table_name = 'results'  # Replace with the name of the table you want to read
                query = f'SELECT * FROM {table_name}'
                df = pd.read_sql_query(query, connection)

                # Get the values of interest (e.g., the last values from columns 1 to 7)
                values = df.iloc[-1, 5]
                
		# Close the database connection
                connection.close()
            #else:
            #    # If the database file is empty, set all parameter values to blank
            #    values = ""

                # Append the results to the list of dictionaries
                results_data.append({'Lake': lake, 'Parameter': values})

# Create a DataFrame from the list of dictionaries
results_df = pd.DataFrame(results_data)

# Save the results DataFrame to a CSV file
results_df.to_csv('/home/dmercado/calibration_local_lakes/parameters_metrics.csv', index=False)  # Replace with the appropriate path
