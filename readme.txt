Instructions on how to run the Dash Application:

1. Create a Virtual Environment


Setup and Run Instructions for the Dash Application

Prerequisites:
- Python 3 installed on your system
- Terminal access (Command Prompt on Windows, Terminal on macOS and Linux)

Step-by-step instructions:

1. Setup Python Environment:
   Ensure Python 3 is installed on your machine. You can verify this by running:

   python --version 
   
   or

   python3 --version

   You should see a version number of Python 3.x.x.

2. Navigate to the project directory

3. Create a Virtual Environment. To create a virtual environment, run:
   python -m venv venv

   or on some systems:

   python3 -m venv venv

   Then activate the virtual environment:
   On Windows:

   venv\Scripts\activate

   on MacOS or Linux:

   source venv/bin/activate

4. Install required packages. Install all dependencies listed
   in the requirements.txt file by running:

   pip install -r requirements.txt

   or 

   pip3 install -r requirements.txt

5. Run the Application. Once all packages are installed, run the application with:

   python app.py 

   or 

   python3 app.py

   After running this command, the Dash application will start and you should see 
   output in the terminal indicating that the server is running. It will typically 
   tell you the local address where the app is being served, usually something like http://127.0.0.1:8050/.

6. Access the Application:
Open a web browser and enter the local server address (http://127.0.0.1:8050/ or whatever address is indicated in the terminal). You should now be able to interact with the application.

Please ensure to keep the terminal open while you are using the application. To stop the server, go back to your terminal and press CTRL+C.

For futher contact or support, contact me through this email: anthony.uy@student.ateneo.edu






