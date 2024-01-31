A small project for parsing and importing data in JSON and then retrieving the information

Order of installation:
1) After cloning the repository write this command in the terminal in 'eshop' directory: pip install -r requirements.txt.
2) If this does not work, run the following commands in the same directory:
   python -m pip install Django (possibly python3)
   pip install djangorestframework

How to run the project:
1) After the installation you will need to initialize the database. Run these commands in the terminal in the same directory:
   python manage.py makemigrations (This command is not necessary as long as you do not change anything in models.py)
   python manage.py migrate (possibly python3)
2) Then after checking that the database was created, run this command in the terminal:
   python manage.py runserver

Click on the link in the terminal and you will see a hint where to go.
Enjoy!
      
