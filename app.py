# from flask import Flask

# # __name__ tells Flask: “Use the current file as the main program.”
# app= Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello Lily, your backend is running!"

# # Python files can be used in two ways:
# # Executed directly — you run the file like: python app.py
# # Imported as a module — another Python file uses it like: import app
# # When Python imports a file, it runs all the code at the top level
# # Sometimes, you don’t want certain code to run when importing.
# # You only want it to run when the file is the “main program” you are executing.
# # 🔑 How Python knows? 
# # Python has a built-in variable:  __name__
# # If you run a file directly → __name__ is "__main__"
# # If you import a file → __name__ is the filename (like "app")
# if __name__== "__main__":
#     # .run() = method that starts the server
#     # app.run() does 3 main things
#     # 1. Opens a port (default is 5000)
#     # Your computer listens on 127.0.0.1:5000 (localhost)
#     # Only your computer can access it for now

#     # 2. Starts a loop that waits for HTTP requests
#     # When your browser visits /, Flask checks your routes
#     # Then runs the corresponding function and sends the response

#     # 3. Runs a development server
#     # This is only for testing and learning
#     # Not meant for real production (later you use something like Gunicorn or NGINX)
#     app.run(debug=True)
#     # debug=True does two things:
#     # Auto-reload on file changes
#     # Debug mode / interactive debugger



from flask import Flask, jsonify

app= Flask(__name__)

@app.route("/")
def home():
    # most APIs communicate using JSON, which is structured data
    # jsonify is a function that converts Python dictionaries to JSON automatically
    # JSON is a key-value structured format
    return jsonify({
        "message": "Hello Lily, your backend is running!",
        "status": "success"
    })

@app.route("/create-customer")
def create_customer():
    return jsonify({
        "customer_id": "cust_001",
        "name": "Test User",
        "email": "lily@example.com"
    })

@app.route("/charge-customer")
def charge_customer():
    return jsonify({
        "customer_id": "cust_001",
        "amount": 50,
        "status": "charged"
    })

if __name__== "__main__":
    app.run(debug=True)

