# Process-Review-Tool/ Sankey Diagram Generator (work in progress)

Visualize your excelsheet with the following requirements here: http://process-review-tool.eu-north-1.elasticbeanstalk.com/

Requirements:
1. suffix is xlsx
2. excelfile contains only one sheet
3. line 1 and column 1 are not empty
4. there are no joined cells in the sheet
   
A detailed introduction to the usecase the prorcess review tool was created for can be found here: https://drive.google.com/file/d/11xXN_69VGJmS-o0dwA8FyAWD1GqJYQW2/view?usp=drivesdk

This interactive Sankey diagram generator is a Dash-based Python application that allows users to visualize relationships between columns in their dataset. The application reads Excel files and presents an interactive interface for selecting columns, filtering data, and generating the Sankey diagram.
![image](https://user-images.githubusercontent.com/81876912/236634270-c1420de9-796c-4c06-9996-45e9544c6695.png)
![image](https://user-images.githubusercontent.com/81876912/236634251-590d0881-873a-403d-a45f-60fbab678f02.png)


# Features
Upload data files in Excel format.
Select multiple columns to visualize in the Sankey diagram.
Filter data by the values of the last selected column.
Generated Sankey diagram updates based on user interactions.
Dependencies
The application requires the following libraries:

dash
pandas
base64
io
Please make sure to install these libraries before running the application.

# How to Use
Clone the repository or download the source code.
Install the required libraries.
Run the main.py file to start the application. This will start a local web server and display the URL to access the app.
Open the URL in your web browser to access the Sankey diagram generator.
Upload an Excel file using the "Drag and Drop or Select Files" uploader.
Once the file is uploaded, choose the columns you want to visualize in the Sankey diagram from the dropdown menu.
Based on the selected columns, choose the filter values for the last selected column using the second dropdown menu.
The Sankey diagram will be generated and displayed on the screen, showing the flow between the selected columns and filtered based on the chosen values.

# Files
main.py: This is the main file containing the Dash application, layout definition, and callback functions.
create_sankey_diagram.py: This file contains the gen_sankey() function responsible for generating the Sankey diagram using Plotly.
Customization
You can customize the appearance of the Sankey diagram and the app layout by modifying the gen_sankey() function in create_sankey_diagram.py and the app.layout in main.py respectively. Please refer to the Dash documentation and Plotly documentation for more information on customization options.

# License
This project is licensed under the MIT License. See the LICENSE file for more details.
