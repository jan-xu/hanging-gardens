'''

University of California, Berkeley
CE 186 Design of Cyber-Physical Systems (Fall Term 2018)
LAB4 - Exercise 7: A Simple Web App
Python code NameServer.py
Jan Xu
SID 3034407224

'''

# Import Flask, request and jsonify from flask module

from flask import Flask, request, jsonify

# Import sqlite3 Python module, connect NameServer database and create table

import sqlite3
conn = sqlite3.connect('NameServer.sqlite') # connects to the database - if .sqlite file does not exist, it will be created
c = conn.cursor()                           # create a cursor object to used call SQL commands

# Create a table if it does not already exist
c.execute('''CREATE TABLE IF NOT EXISTS names (firstname TEXT, lastname TEXT)''')
conn.commit() # save, or 'commit' the changes
conn.close()  # close the connection after the commit

# Create app object

app = Flask(__name__)

# Route all HTTP requests to the base URL to the root() function, which returns
# the string "Hello"

@app.route('/')
def root():
  return "Hello"

# Route with URL variable first_name
  
@app.route('/firstname/<first_name>', methods=['GET'])
def firstname(first_name):
    return "Hello " + first_name

# Route with URL variables first_name and last_name and a query string with
# query parameters mi and yr

@app.route('/firstname/<first_name>/lastname/<last_name>', methods=['GET'])
def firstlastname(first_name, last_name):
    mi = request.args.get('mi', None) # gets middle initial
    if mi is None:
        return "Hello " + first_name + " " + last_name
    
    yr = request.args.get('yr', None) # gets class year
    if yr is None:
        return "Hello " + first_name + " " + mi + ". " + last_name
    
    return "Hello " + first_name + " " + mi + ". " + last_name + ", Hogwarts Class of " + yr

# Route for storing a name in the database

@app.route('/storename', methods=['POST'])
def storefirstlastname():
    try:
        # Parse the JSON payload/body/data
        payload = request.get_json()
        first = payload['firstname']
        last = payload['lastname']
        
        # Connect to database, add a row to the table with new names, commit
        # and close
        conn = sqlite3.connect('NameServer.sqlite')
        c = conn.cursor()
        c.execute('''INSERT INTO names VALUES (?, ?)''', (first, last))
        conn.commit()
        conn.close()
        
        return jsonify({"code":200})
    
    except:
        
        return jsonify({"code":500})

# Route for retrieving names from the database

@app.route('/retrievename', methods=['GET'])
def retrievefirstlastname():
    # Connect to database, get the five most recently added names from the
    # table, commit and close
    conn = sqlite3.connect('NameServer.sqlite')
    c = conn.cursor()
    c.execute('''SELECT * FROM names ORDER BY ROWID DESC LIMIT 5''')
    query_results = c.fetchall() # results are stored in tuples
    conn.commit()
    conn.close()
    
    # Convert tuples to lists in a dictionary, as the value to the key 'names'
    results = {'names':[list(i) for i in query_results]}
    return jsonify(results)
    
# Start the app, making it available on a local network
    
if __name__ == '__main__':
    import socket # import socket module to find IP address
    my_ip = str(socket.gethostbyname(socket.gethostname()))
    print("\n* Running on the local network at http://" + my_ip + ":5000/")
    app.run(host='0.0.0.0') # runs app and sets host to 0.0.0.0