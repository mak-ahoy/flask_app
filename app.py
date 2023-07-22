from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
db= SQLAlchemy(app)

# adding a schema for the alchemy databse
class Info(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(20), nullable=False)
    datecreated= db.Column(db.DateTime, default=datetime.utcnow)

def __repr__self():
    return '<Task %r>' % self.id



# Define a route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle the form submission
@app.route('/submit', methods=['GET' ,'POST'])
def submit():
    # Get the data from the submitted form
    code = request.form.get('code') 

    # Process the code, perform necessary computations, etc.
    result = process_code(code)

    # Pass the result back to the HTML template
    return render_template('result.html', result=result, code=code)

# route for login page
@app.route('/login')
def login():
    return render_template('login.html')

#gives new route of welcome  after validation. 
@app.route('/welcome' , methods=['GET', 'POST'])
def changed():
    email = str(request.form.get('email'))
    passw = str(request.form.get('password'))

    if (validatePass(passw) and validateEmail(email)):
        return render_template('welcome.html', email = email , passw = passw)
    
#this requires moroe testing and debugging for the smae the same type of code    
    # elif (validateEmail(email)==False):
    #     return render_template('index.html', email = "Please write correct email address!")
    # elif (validatePass(passw)==False):
    #     return render_template('index.html', passw = "Password should greater than 8 character and not guessable!")
    elif (validatePass(passw) == True and validateEmail(email) == True):
        return render_template('login.html', email = email, passw = passw)
    elif (validatePass(passw) == False and validateEmail(email) == True):
        return render_template('login.html', email = email, passw = "Wrong")
    else:
        return render_template('login.html', email = "", passw = "")


# Function to process the code
def process_code(code):
    try:
        # Try to compile the code
        compiled_code = compile(code, '<string>', 'exec')
        return 'Code is valid and makes sense'
    except SyntaxError as e:
        return f'Code has syntax errors: {str(e)}'  + ' Failed Processed Result'
    except Exception as e: 
        return f'An error occurred: {str(e)}' + 'Failed Processed Result'
    
# validates login email for the page
def validateEmail(email):
    count=0
    if (email[-4:]==".com" and len(email)>7):
        for i in email:
            print(i)
            if (i=="@"):
                count+=1
        if count==1:
            return True
    else:
        return False
        
#validates login password for the page
def validatePass(password):
    if (len(password)>8 and password != "Password123"):
        return True
    else:
        return False

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
