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



# from flask import Flask, jsonify

# app= Flask(__name__)

# @app.route("/")
# def home():
#     # most APIs communicate using JSON, which is structured data
#     # jsonify is a function that converts Python dictionaries to JSON automatically
#     # JSON is a key-value structured format
#     return jsonify({
#         "message": "Hello Lily, your backend is running!",
#         "status": "success"
#     })

# @app.route("/create-customer")
# def create_customer():
#     return jsonify({
#         "customer_id": "cust_001",
#         "name": "Test User",
#         "email": "lily@example.com"
#     })

# @app.route("/charge-customer")
# def charge_customer():
#     return jsonify({
#         "customer_id": "cust_001",
#         "amount": 50,
#         "status": "charged"
#     })

# if __name__== "__main__":
#     app.run(debug=True)

# -----------------------------------------------Dynamic version
# print("THIS FILE IS RUNNING")
# from flask import Flask, jsonify

# app= Flask(__name__)

# @app.route("/")
# def home():
#     # most APIs communicate using JSON, which is structured data
#     # jsonify is a function that converts Python dictionaries to JSON automatically
#     # JSON is a key-value structured format
#     return jsonify({
#         "message": "Hello Lily, your backend is running!",
#         "status": "success!!!!!"
#     })

# @app.route("/create-customer/<name>/<email>")
# def create_customer(name, email):
#     return jsonify({
#         "customer_id": "cust_001",
#         "name": name,
#         "email": email
#     })

# @app.route("/charge-customer/<customer_id>/<int:amount>")
# def charge_customer(customer_id, amount):
#     return jsonify({
#         "customer_id": customer_id,
#         "amount": amount,
#         "status": "charged"
#     })

# @app.route("/status/<system>/<users>/<errors>")
# def status(system, users, errors):
#     return jsonify({
#         "system": system,
#         "users": users,
#         "errors": errors
#     })

# @app.route("/multiply/<int:x>/<int:y>")
# def multiply(x, y):
#     return jsonify({"result": x*y})
# # Summary: Always return a string, dict, or Response object from Flask route. Integers/floats alone are not valid HTTP responses.
# # return x*y is an integer. Flask cannot automatically convert a raw int to a response
# # What Flask accepts as a return:
# # str → Flask wraps it in a response with text/html
# # dict → Flask 2.0+ automatically converts to JSON, or you can use jsonify(dict)
# # Response object → fully custom response


# @app.route("/test")
# def test():
#     return "Test route works"



# if __name__== "__main__":
#     app.run(debug=True, use_reloader=False)


# ----------------------------POST requests & in-memory storage
from flask import Flask, jsonify, request

app= Flask(__name__)
# {} -> create dictionary customers
customers= {}
next_customer_id= 1

# --------------------------------charging system
invoices= {}
next_invoice_id= 1

@app.route("/create-customers", methods=["POST"])
def create_customer():
    # You want to get JSON data sent by the client
    data= request.get_json()
    # data is a Python dictionary, syntax data["key"]
    # Extract name/email
    name= data["name"]
    email= data["email"]

    # since you're modifying a global variable inside a function, Python needs: global
    #  Create a customer_id
    global next_customer_id

    customer_id= f"cust_{next_customer_id}"
    next_customer_id +=1

    # [] are how you access or assign a key inside a dictionary.
    # my_dict = {}
    # my_dict["apple"] = 5
    # dictionary becomes {"apple": 5}
    # Store in dictionary
    # Store the name/email in the customers dictionary using customer_id as key
    customers[customer_id]= {"name": name, "email": email}
    
    # return response
    return jsonify({
        "customer_id": customer_id,
        "name": name,
        "email": email
    })

@app.route("/")
def home():
    # most APIs communicate using JSON, which is structured data
    # jsonify is a function that converts Python dictionaries to JSON automatically
    # JSON is a key-value structured format
    return jsonify({
        "message": "Hello Lily, your backend is running!",
        "status": "success!!!!!"
    })

@app.route("/test")
def test():
    return "Test route works"


@app.route("/get-customer/<customer_id>")
def get_customer(customer_id):
    # Always check existence BEFORE accessing dictionary key.
    # Wrong order:
    # Access
    # Then check
    # Correct order:
    # Check
    # Then access
    
    if customer_id in customers:

        customer_data= customers[customer_id]
        name= customer_data["name"]
        email= customer_data["email"]

        return jsonify({
            "customer_id": customer_id,
            "name": name,
            "email": email
        })
    else: 
        return jsonify({"error": "Customer not found"})


# charging system
@app.route("/charge-customer", methods=["POST"])
def charge_customer():
    
    data= request.get_json()
    customer_id= data["customer_id"]
    
    if customer_id in customers:
        
        amount= data["amount"]

        global next_invoice_id
        invoice_id= f"inv_{next_invoice_id}"
        next_invoice_id +=1

        invoices[invoice_id]={
            "customer_id": customer_id,
            "amount": amount, 
            "status": "charged"
        }

        return jsonify({
            "invoice_id": invoice_id,
            "customer_id": customer_id,
            "amount": amount, 
            "status": "charged"
        })

    else:
        return jsonify({"error": "The customer doesnt exist." })
    

#  retrieve an invoice after it’s created
@app.route("/get-invoice/<invoice_id>")
def get_invoice(invoice_id):
    if invoice_id in invoices:
        invoice_data= invoices[invoice_id]

        return jsonify({
            "invoice_id": invoice_id,
            "customer_id": invoice_data["customer_id"],
            "amount": invoice_data["amount"],
            "status": "charged"
        })
    
    else: 
        return jsonify({
            "error": "It doesnt exist!"
        })


# Filtering and listing multiple items
# Right now your invoices structure looks like this in memory:
# invoices = {
#   "inv_1": {"customer_id": "cust_1", "amount": 50, "status": "charged"},
#   "inv_2": {"customer_id": "cust_1", "amount": 20, "status": "charged"},
#   "inv_3": {"customer_id": "cust_2", "amount": 70, "status": "charged"}
# }

# your job is to turn that dictionary into a list of JSON objects
# like this
# [
#   {"invoice_id": "inv_1", "customer_id": "cust_1", "amount": 50},
#   {"invoice_id": "inv_2", "customer_id": "cust_1", "amount": 20},
#   {"invoice_id": "inv_3", "customer_id": "cust_2", "amount": 70}
# ]

# Why return a list instead of a dictionary?
# most APIs prefer a list of objects:
# Reason 1 — predictable structure
# Frontends expect collections to be arrays/lists.
# Reason 2 — easier filtering & sorting later
# Lists are much easier for that.
# Reason 3 — real APIs do this

@app.route("/all-invoices")
def all_invoices():
    all_invoices= []

    for i in invoices:
        invoices_id= i
        invoices_data= invoices[i]

        invoices_obj= {
            "invoice_id": invoices_id,
            "customer_id": invoices_data["customer_id"],
            "amount": invoices_data["amount"],
            "status": invoices_data["status"]
        }
        
        all_invoices.append(invoices_obj)

    return jsonify({
        "invoices": all_invoices
    })



if __name__== "__main__":
    app.run(debug=True, use_reloader=False)