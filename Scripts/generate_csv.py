import os
import pandas as pd
import sqlite3

# Root directory containing "chunk8_*" directories
root_directory = '/home/dmercado/calibration_local_lakes/files_ok'  # Replace with the appropriate path

# Create an empty list to store the results
results_data = []

# Iterate through directories in search of "calibration.db" files
for dir_lake in os.listdir(root_directory):
            lake = dir_lake  # Lake name is the directory name
            db_file = os.path.join(root_directory, dir_lake, 'calibration.db')

            # Check if the database file exists and is not empty
            #if os.path.isfile(db_file) and os.path.getsize(db_file) > 0:
            if os.path.isfile(db_file):
                # Connect to the SQLite database
                connection = sqlite3.connect(db_file)

                # Use Pandas to read the SQLite table into a DataFrame
                table_name = 'results'  # Replace with the name of the table you want to read
                query = f'SELECT * FROM {table_name}'
                df = pd.read_sql_query(query, connection)

                # Get the values of interest (e.g., the last values from columns 1 to 7)
                values_list = df.iloc[-1, 3]
                values = values_list.split(";")
                
		# Close the database connection
                connection.close()
            #else:
                # If the database file is empty, set all parameter values to blank
            #    values = [""] * 7

                # Append the results to the list of dictionaries
                results_data.append({'Lake': lake, 'Parameter1': values[0], 'Parameter2': values[1], 'Parameter3': values[2], 'Parameter4': values[3], 'Parameter5': values[4], 'Parameter6': values[5], 'Parameter7': values[6]})

# Create a DataFrame from the list of dictionaries
results_df = pd.DataFrame(results_data)

# Save the results DataFrame to a CSV file
results_df.to_csv('/home/dmercado/calibration_local_lakes/parameters_results.csv', index=False)  # Replace with the appropriate path

