# DSCI_510_Final_Project

Project Name: Adult Diabetes in the United States
Team Member: Pei-Jou Liu, ID: 7384221314, email: peijoul@usc.edu

Create a virtual environment to run the project this keeps the project’s libraries separate from other projects.

pip install -r requirements.txt

python get_data.py

python clean_data.py

python run_analysis.py

python visualize_results.py

To get data, run get_data.py. It downloads adult diabetes data from the CDC and saves it as CSV files. Since the API does not work, I use the CSV files that are already in the data/raw/ folder.

To clean data, run clean_data.py. It reads all the CSV files in data/raw/, finds the year and type of each file, and then cleans and merges all the information into the data/processed/ folder.

To run analysis, run run_analysis.py. It loads the clean_data from data/processed/, keeps only the rows about diabetes, and creates summary tables that are saved in the results/ folder.

To produce the visualizations, run visualize_results.py. It reads the summary tables from the results folder, creates the graphs, and saves the image files in the results/ folder.
