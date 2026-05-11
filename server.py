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

# --------------------------------input validation
ALLOWED_STATUS= {"charged", "paid", "failed"}
# Use UPPERCASE for constants:
# This tells other developers: “This value should NOT change”

# --------------------------------Building contracts layer
# billing logic architecture
# creating source of truth for billing rules
# Invoices are temporary financial records.
# Contracts are the permanent agreement.

# The contract stores BILLING RULES.
# Invoices are only generated FROM the rules.
contracts= {}
next_contract_id= 1

@app.route("/create-contract", methods=["POST"])
def create_contract():
    data= request.get_json()

    customer_id= data["customer_id"]
    start_date= data["start_date"]
    monthly_amount= data["monthly_amount"]
    annual_inspection_fee= data["annual_inspection_fee"]

    if customer_id not in customers:
        return "Customer doesn't exist. "
    
    global next_contract_id
    contract_id= f"contract_{next_contract_id}"
    next_contract_id= next_contract_id +1

    end_date= "2076-01-01"

    contracts[contract_id]= {
        "customer_id": customer_id,
        "start_date": start_date,
        "end_date": end_date,
        "monthly_amount": monthly_amount,
        "annual_inspection_fee": annual_inspection_fee
    }

    return jsonify(contracts[contract_id])


# Customer Balance
# building a rule:
# “Show how much the customer owes in total, including unpaid past invoices.”
@app.route("/customer-balance/<customer_id>")
def customer_balance(customer_id):
    total_due= 0

    for i in invoices:
        invoice= invoices[i]

        if invoice["customer_id"] == customer_id and invoice["status"] !="paid":
            total_due= total_due+invoice["amount"]
        
    return jsonify({"customer_id": customer_id, 
                   "total_due":total_due})



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
            "status": invoice_data["status"]
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


# Filtering invoice of a specific customer 
@app.route("/customer-invoices/<customer_id>")
def customer_invoices(customer_id):
    # Pre-check for customer existence
    if customer_id not in customers:
        return {
            "Error": "404 Not found. "
        }

    customer_invoices= []

    for i in invoices:
        invoice_id= i
        invoice_data= invoices[i]

        if invoice_data["customer_id"] == customer_id:
           invoice_obj={
               "invoice_id": invoice_id,
               "customer_id": invoice_data["customer_id"],
               "amount": invoice_data["amount"],
               "status": invoice_data["status"]
           }

           customer_invoices.append(invoice_obj) 

    return jsonify({
        "invoices": customer_invoices
    })


# Helper functions
# def get_invoices(customer_id=None):
# meaning: The function can receive a customer_id, but it is optional.
# Case A — no parameter passed: format_invoices()
# Case B — parameter passed: format_invoices("cust_1")
def format_invoices(customer_id=None):
    # Create empty list
    formatted_invoices= []
    
    # A dictionary has pairs:key, value
    # .items() returns both the key and the value together
    # Conceptually it becomes:
    # (inv_1 , {customer_id: cust_1, amount: 50})
    # (inv_2 , {customer_id: cust_2, amount: 70})

    # Python can automatically split that pair into two variables
    # for invoice_id, invoice_data in invoices.items():
    # first loop:
    # invoice_id = "inv_1"
    # invoice_data = {"customer_id": "cust_1", "amount": 50}

    # dictionary loop cheat sheet
    # for key in dict
    # → loops keys
    # for value in dict.values()
    # → loops values
    # for key, value in dict.items()
    # → loops both
    for invoice_id, invoice_data in invoices.items():
        # usually order conditions like: general condition→ specific condition

        # guard clause: it keeps code flatter and easier to read
        # Developers often prefer guard clause:
        # if bad_condition:
        #     continue

        # because it keeps the main logic outside the if.
        # Instead of:
        # if condition:
        #     do 10 lines

        # we write:
        # if bad_condition:
        #     continue

        # do 10 lines

        # A guard clause means:
        # Exit early if something is invalid.
        # This prevents deep nesting.

        # if wrong_customer:
        # continue
        # This protects the main logic.

        # Why developers like guard clauses
        # Because the main logic stays clean:
        # for invoice in invoices
        #     guard 1
        #     guard 2
        #     guard 3

        #     build invoice object

        # Instead of messy nesting like:
        # if customer matches
        #     if status is paid
        #         if something else
        #             build object

        # Guard clauses flatten the code.
        if customer_id is not None and invoice_data["customer_id"] != customer_id:
            # is not None instead of != None because None is a special object, not a normal value. but both work. 

            # continue: Ignore the rest of this loop iteration and jump to the next invoice.
            # So inside a loop:
            # for item in something:
            #     if condition:
            #         continue

            # means:
            # if condition is true
            #     ignore everything below
            #     go to next loop iteration
            continue
        # Example:
        # invoice_id = "inv_1"
        # invoice_data = {
        #     "customer_id": "cust_1",
        #     "amount": 50
        # }

        # Now suppose your endpoint asked for:
        # customer_id = "cust_2"

        # So we check:
        # invoice_data["customer_id"] != customer_id

        # which becomes:
        # "cust_1" != "cust_2"

        # That is True.
        # So Python executes:
        # continue

        # Meaning:
        # skip building invoice_obj
        # skip append
        # go to next invoice

        # when it's false -> build invoice_obj

        # bad_case = True
        # → continue
        # → jump to next loop iteration
        # → do_something() skipped

        invoice_obj={
               "invoice_id": invoice_id,
               "customer_id": invoice_data["customer_id"],
               "amount": invoice_data["amount"],
               "status": invoice_data["status"]
           }
        
        formatted_invoices.append(invoice_obj)

    # JSON needs key:value pairs
    # JSON is basically a structured data format
    # example:
    # {
    #   "name": "Alice",
    #   "age": 22
    # }

    # orginally i wrote 
    # return jsonify({
    #     "invoices": formatted_invoices
    # })
    # But since this is a helper, it should just return:
    return formatted_invoices
    # Then the route does: jsonfiy()

    # helper function is not responsible for HTTP, and should return a Python list
      
# Helper function that updates an invoice status. like “mark this invoice as paid or failed.”
def update_invoice_status(invoice_id, new_status):
    # Check existence (guard clause)
    # This is called a guard clause — it stops execution early if a condition is not met.
    if invoice_id not in invoices: 
        return {"error": True,
                "type": "not_found",
                "message": "Invoice not found. "}
    
    # Input validation
    # List []
    # Ordered
    # Slower lookup
    # Set {}
    # Unordered
    # ⚡ Faster lookup (this is why we prefer it)

    # 📦 List ([])
    # ["charged", "paid", "failed"]
    # 👉 Python checks one by one:

    # Is it "charged"? ❌  
    # Is it "paid"? ❌  
    # Is it "failed"? ✅

    # 👉 This is called linear search
    # 👉 Time complexity: O(n) (slower as list grows)
    # 🐢 O(n) — Linear Time
    # 👉 Time grows proportionally with n

    # Time complexity = how fast (or slow) an algorithm grows as input size increases
    # n = number of elements
    # Example:
    # 3 invoices → n = 3
    # 1,000 invoices → n = 1000
    # 1,000,000 invoices → n = 1,000,000

    # ⚡ Set ({})
    # {"charged", "paid", "failed"}
    # 👉 Python uses something called a hash table

    # Instead of checking one by one:
    # → instantly jump to where "paid" should be
    # → check it directly

    # 👉 No looping through everything
    # 👉 Time complexity: O(1) (constant time)
    # Meaning: 👉 No matter how big n is, time stays the same

    # What happens internally?
    # Python uses a hash table:
    # 1.Convert key → hash (a number)
    # 2.Jump directly to memory location
    # 3.Get value
    # 👉 No scanning
    # 👉 No looping

    # 🔥 Simple analogy
    # List:
    # Like checking names on paper:
    # You read line by line until you find it
    # Set:
    # Like a locker system:
    # You go directly to locker #42

    # dictionary and set they’re both {}, Python distinguishes them by structure
    # Dictionary
    # {"key": "value"}
    # 👉 key : value pair
    # Set
    # {"charged", "paid", "failed"}
    # 👉 just values, NO keys

    # To create empty set:
    # set()

    # Dictionary and Set are BOTH hash-based -> O(1)

    if new_status not in ALLOWED_STATUS:
        # 👉 if it's a set → O(1)
        # 👉 if it's a list → O(n)
        return {
            "error": True,
            "type": "invalid_request",
            "message": "Invalid status. "
            }
    
    
    invoice_data= invoices[invoice_id]
    invoice_data["status"]= new_status

    return {
        "error": False,
        "data":{
            "invoice_id": invoice_id,
            "customer_id": invoice_data["customer_id"], 
            "amount": invoice_data["amount"],
            "status": invoice_data["status"]
            }
        
    }

# validator (reusable validation system)
# its only job is: determine whether data is valid
# NOT:
# create responses
# return HTTP codes
# format Flask responses
# That belongs to route.

# validator should return plain Python structure
def validate_update_invoice_request(data):
    if data is None:
        return {
                "error": True,
                "type": "invalid_request",
                "message": "client JSON is missing. "}
        
    if "invoice_id" not in data:
        return {
                "error": True,
                "type": "invalid_request",
                "message": "invoice_id is missing. "}

    if "status" not in data:
        return {
                "error": True,
                "type": "invalid_request",
                "message": "status is missing. "}

    # Type validation
    # this line can still crash:
    # data["status"].strip()

    # Why?
    # Because .strip() only works on strings.

    # so BEFORE .strip(), validate type.
    # Is "status" a string?
    # Syntax: isinstance(value, str)

    # Why this is preferred over type():
    # type(x) == str
    # checks:
    # “Is this EXACTLY a str?”

    # isinstance(x, str)
    # checks:
    # “Can this behave like a str?”
    # returns either true or false

    # Python developers usually prefer isinstance() for validation.
    check_type= data["status"]
    if not isinstance(check_type, str):
        return {
            "error": True,
            "type": "invalid_request", 
            "message": "Status is not string. "
        }
    
    # Case 1 — valid string
    # Suppose:
    # check_type = "paid"
    # Then:
    # isinstance("paid", str)
    # becomes:
    # True
    # Now your condition:
    # if not isinstance(check_type, str):
    # becomes:
    # if not True:
    # which becomes:
    # if False:
    # So:
    # block does NOT run
    # NO error returned
    # validation passes ✔

    # That is correct.

    # Case 2 — invalid type
    # Suppose:
    # check_type = 123
    # Then:
    # isinstance(123, str)
    # becomes:
    # False
    # Now condition becomes:
    # if not False:
    # which becomes:
    # if True:
    # So:
    # error block runs ✔
    # validation fails ✔

    # Also correct.

    # The important mental model
    # You are NOT asking:
    # “Is it true?”
    # You are asking:
    # “Is this INVALID?”

    # Backend validation is usually written as:
    # if invalid:
    #     reject request

    # NOT:
    # if valid:
    #     continue

    # Why?
    # Because guard clauses are cleaner.

    # So this:
    # if not isinstance(check_type, str):

    # means:
    # “If status is INVALID (not string), reject immediately.”

    # That’s the correct backend mindset.


    # You’re thinking:
    # “If they’re separate, how does second validation know first validation already happened?”

    # Answer:
    # Because Python runs code TOP → DOWN line by line.
    # 👉 return immediately STOPS the function

    # This is the key.
    # Your code:
    # if not isinstance(check_type, str):
    #     return error

    # if not data["status"].strip():
    #     return error

    # Execution flow becomes:

    # Step 1:
    # Check type

    # If invalid:
    #     RETURN immediately
    #     function ENDS

    # If valid:
    #     continue downward

    # That means:
    # .strip()
    # ONLY runs if Python survived the first check.

    # Example — invalid type
    # Suppose:
    # status = 123

    # First condition:
    # if not isinstance(123, str):
    # becomes:
    # if True:
    # So:
    # return error
    # Function ENDS immediately.
    # Python NEVER reaches:
    # .strip()
    # That’s the important part.

    # Example — valid string
    # Suppose:
    # status = "paid"
    # First condition:
    # if not isinstance("paid", str):
    # becomes:
    # if False:
    # So Python SKIPS the return.
    # Then continues downward safely to:
    # .strip()

    # Now it’s safe because you already proved it’s a string.

    if not data["status"].strip():
        return {
                "error": True,
                "type": "invalid_request",
                "message": "status is invalid. "}
        
    # explicit success return
    # validator returns None if valid
    return None


@app.route("/update-invoice-status", methods=["POST"])
def route_update_invoice():
    #  1. get JSON from request

    # Property vs Method in Python
    # You wrote: request.json (property) vs request.get_json() (method).
    # Property (request.json)
    # Think of it as a variable attached to the object.
    # No parentheses ().
    # Directly gives the value (parsed JSON if available).
    # Example:
    # data = request.json  # no () needed

    # Method (request.get_json())
    # Think of it as a function attached to the object.
    # You call it with parentheses ().
    # Can accept optional arguments (like force=True, silent=True).
    # Example:
    # data = request.get_json()  # you call it

    # ✅ Bottom line: for simple use, they behave almost the same. Some developers prefer the method because it gives more control.
    # ✅ Both are fine, just pick one
    data= request.get_json()

    # wire validator into route
    validation_error= validate_update_invoice_request(data)

    # i wrote:
    # return jsonify({validation_error})
    # ❌ This is wrong
    # When you wrap something in {} WITHOUT key:value pairs:
    # Python interprets it as a:
    # SET
    # So:
    # {validation_error}
    # means:
    # “create a set containing validation_error”
    # But:
    # dictionaries are unhashable
    # sets cannot contain dictionaries
    # So this breaks.

    # Your validator ALREADY returns a dictionary:
    # {
    #    "error": True,
    #    "message": "..."
    # }
    # So you should pass it DIRECTLY
    if validation_error:
        return jsonify(validation_error), 400


    # Input Validation
    # APIs cannot trust clients.
    # Clients can send:
    # missing fields
    # wrong types
    # empty values
    # garbage data

    # Validate if client send JSON
    # If:
    # data = None
    # then Python crashes immediately.

    #⚡ Important rule
    # Validation belongs BEFORE business logic.
    # Meaning:
    # routes validate request structure
    # helpers perform business operations

    # Layer 1
    # Was JSON sent?
    # Layer 2
    # Does required data exist?

    # receive request
    # ↓
    # is json missing?
    # ↓
    # is invoice_id missing?
    # ↓
    # is status missing?
    # ↓
    # is status empty?
    # ↓
    # is status wrong type?
    # ↓
    # call helper
    # if data is None:
    #     return jsonify({
    #             "error": True,
    #             "type": "invalid_request",
    #             "message": "client JSON is missing. "}), 400
    
    # if "invoice_id" not in data:
    #     return jsonify({
    #             "error": True,
    #             "type": "invalid_request",
    #             "message": "invoice_id is missing. "}), 400
    
    # if "status" not in data:
    #     return jsonify({
    #             "error": True,
    #             "type": "invalid_request",
    #             "message": "status is missing. "}), 400
    
    # You ALREADY validate valid statuses later:
    # if new_status not in ALLOWED_STATUS
    # inside helper.
    # That means:
    # helper validates BUSINESS RULES
    # route validates REQUEST STRUCTURE

    # 🧠 So route should probably focus on:
    # request exists
    # required fields exist
    # values not empty
    # while helper handles:
    # allowed statuses
    # invoice existence
    # business operations

    # Python treats empty strings as:
    # False
    # This is called:
    # falsy values

    # In Python:
    # Value	    Truthy/Falsy
    # ------------------------------
    # "paid"	truthy
    # ""	    falsy
    # None	    falsy
    # 0	        falsy

    # .strip() always returns:
    # another STRING
    # Always.
    # Even if the string becomes empty.

    # 🔥 Empty string is NOT None
    # This is VERY important.
    # Value	Meaning
    # ------------------------------------------------
    # None	absence of value/object
    # ""	string exists, but contains 0 characters

    # Empty string
    # ""
    # is:
    # a string
    # BUT Python treats it as falsy


    # ❌ Problem
    # You wrote:
    # if data["status"].strip() is False:
    # But:
    # data["status"].strip()
    # returns a STRING.
    # Example:
    # "paid" or ""
    # It does NOT return the boolean:
    # False

    # 🧠 Important distinction
    # Empty string ""
    # is:
    # a string
    # BUT Python treats it as falsy

    # Boolean False
    # False
    # is:
    # actual boolean object
    # These are different things.

    # 🔥 Example
    # This is FALSE:
    # "" is False

    # because:
    # empty string ≠ boolean False

    # ⚡ But Python allows this:
    # if "":
    # Python interprets empty string as falsy.
    # That’s the magic.

    # ⚡ Why your version doesn’t work
    # You tried to force a boolean comparison:
    # .strip() not True
    # But .strip() doesn’t produce booleans — it produces strings.
    # So you're comparing:
    # string vs boolean ❌
    # if not data["status"].strip():
    #     return jsonify({
    #             "error": True,
    #             "type": "invalid_request",
    #             "message": "status is invalid. "}), 400

    # 🔥 Your confusion
    # You’re thinking:
    # not False → True
    # so if condition is True → return error???

    # That feels backwards at first.
    # But the key issue is:
    # you’re mixing up the value inside the condition vs the condition itself.

    # 🧠 Step-by-step breakdown
    # Your code:
    # if not data["status"].strip():
    # Let’s simulate it.
    # Case 1: valid input
    # data["status"] = "paid"
    # Then:
    # data["status"].strip() → "paid"
    # Now:
    # not "paid"

    # Python rules:
    # non-empty string → True
    # so:
    # not True → False

    # So condition does NOT run ❌
    # ✔ correct (we do NOT want error)

    # Case 2: invalid input (spaces only)
    # data["status"] = "   "
    # Then:
    # .strip() → ""
    # Now:
    # not ""

    # Python rules:
    # empty string → False
    # So:
    # not False → True

    # So condition runs ✔
    # → return error

    # 🔥 So what is actually happening?
    # You are NOT saying:
    # “if not False then error”
    # You are saying:
    # “if status is empty after cleaning → error”

    # 🧠 The real mental model
    # This line:
    # if not data["status"].strip():
    # means:
    # IF status has NO meaningful value → reject request
    # NOT:
    # IF True → reject request

    # ⚡ Why it feels weird (but is actually correct)
    # Because Python allows “truthy/falsy evaluation”:
    # Value	            Treated as
    # ------------------------------
    # "hello"	        True
    # ""	            False
    # " " → "".strip()	False
    # So Python is doing shorthand logic for you.

    # Instead of reading:
    # if not data["status"].strip()
    # read it like English:
    # “If status is empty after removing spaces”

    # 2. extract invoice_id and new_status
    invoice_id= data["invoice_id"]
    status= data["status"]

    # 3. call helper -> result = update_invoice_status(invoice_id, new_status)
    result= update_invoice_status(invoice_id, status)

    # map types to HTTP codes
    if result["error"]:
        if result["type"] == "not_found":
            return jsonify(result), 404
        elif result["type"] == "invalid_request":
            return jsonify(result), 400
        
    # Flask can accept:
    # Return Type	    Meaning
    # string	        text response
    # dict	            JSON response
    # Response object	advanced/custom
    # tuple	            (response, status_code)
        
    # 4. jsonify(result) and return
    return jsonify(result), 200
        
    # Python Set
    # Set = unordered collection of unique elements
    # Defined using {} with values without key:value pairs

    # Example:
    # my_set = {1, 2, 3}
    # print(my_set)  # output: {1, 2, 3}
    # my_set.add(2)
    # print(my_set)  # still {1, 2, 3} because duplicates are ignored

    # Why your jsonify({result}) is wrong:
    # {result} → Python sees it as a set containing your dict, not a dictionary.
    # Flask jsonify() expects dict or list to convert to JSON properly.

    # ✅ Correct way: just pass the dictionary:
    # return jsonify(result)  # result is already a dict
    


if __name__== "__main__":
    app.run(debug=True, use_reloader=False)