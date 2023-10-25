from flask import Flask, render_template, request, redirect, url_for, jsonify   
import openai
import json
import os
import pandas as pd
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Configuration for uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# OpenAI Configuration
openai.api_key = "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"
# Hardcoded file path for uploads
# HARDCODED_FILE_PATH = "/Users/abhi/Desktop/Smartvoy Restaurant/sample.csv"

def get_menu_information(menu_name):
    # Try to form a file path based on menu_name
    menu_file_path = "/Users/abhi/Desktop/Smartvoy_R/uploads/sample.csv"
    menu_df =  pd.read_csv(menu_file_path)

    return menu_df.to_json(orient='records')

cart = []

def add_to_cart(item_name, quantity=1, special_request=None, follow_up_responses=None):
    cart_item = {"item_name": item_name, "quantity": quantity}
    if special_request:
        cart_item["special_request"] = special_request
    if follow_up_responses:
        cart_item["follow_up_responses"] = follow_up_responses
    cart.append(cart_item)
    return json.dumps({"success": f"Added {item_name} to the cart", "cart_item": cart_item})


def view_cart():
    return json.dumps(cart)

# def place_order():
#     order_details = cart.copy()
#     cart.clear()
#     return json.dumps({"success": "Order placed", "order_details": order_details})

# def provide_suggestions(category=None):
#     # Example best_sellers data - replace with actual data if available
#     best_sellers = {
#         "appetizers": ["Chicken Wings", "Mozzarella Sticks"],
#         "main_courses": ["Grilled Salmon", "Filet Mignon"],
#         "desserts": ["Chocolate Cake", "Cheesecake"],
#     }

#     if category and category in best_sellers:
#         suggestions = best_sellers[category]
#     else:
#         suggestions = [item for sublist in best_sellers.values() for item in sublist]

#     return json.dumps({"suggestions": suggestions})

# def ask_follow_up(item_name):
#     follow_up_questions = {
#         "burger": "How would you like your burger cooked?",
#         "coffee": "Would you like sugar or milk with your coffee?"
#         # Add more follow-up questions for other items here
#     }

#     question = follow_up_questions.get(item_name, "")
#     return json.dumps({"question": question})

# def calculate_total(menu_data):
#     total_price = 0
#     item_prices = {item['item_name']: item['price'] for item in menu_data}
    
#     for item in cart:
#         item_name = item["item_name"]
#         quantity = item["quantity"]
#         price = item_prices.get(item_name, 0) * quantity
#         total_price += price
        
#     return json.dumps({"total_price": total_price})

# reservations = [] 
# def make_reservation(date, time, number_of_guests, last_name):
#     reservation_details = {
#         "date": date,
#         "time": time,
#         "number_of_guests": number_of_guests,
#         "last_name": last_name,
#     }

#     # You can add code here to save or process the reservation details
#     # as required by your application.

#     return json.dumps({"success": "Reservation made", "reservation_details": reservation_details})

# def check_reservation_status(last_name="LUIS", reservation_id=None):
#     # function code here
#     for reservation in reservations:
#         if reservation['last_name'] == last_name or reservation['id'] == reservation_id:
#             return json.dumps(reservation)
#     return json.dumps({"error": "Reservation not found"})

# def cancel_reservation(reservation_id):
#     global reservations
#     reservations = [res for res in reservations if res['id'] != reservation_id]
#     return json.dumps({"success": "Reservation canceled"})


# def update_order(order_id, changes):
#     print(f"Debug: Incoming order_id = {order_id}, cart = {cart}")  # Debug statement
#     for item in cart:
#         if 'order_id' in item and item['order_id'] == order_id:
#             item.update(changes)
#             return json.dumps({"success": "Order updated", "order_details": item})
#     return json.dumps({"error": "Order not found"})



# special_offers = ["Special Menu", "10% Discount on Weekdays"]  # Sample data

# def get_special_offers():
#     return json.dumps({"special_offers": special_offers})


# allergy_information = {"gluten-free": ["Salad", "Grilled Chicken"]}  # Sample data

# def get_allergy_information(allergy_type):
#     return json.dumps({"allergy_information": allergy_information.get(allergy_type, [])})


# order_history = {}  # Sample data

# def review_order_history(user_id):
#     return json.dumps({"order_history": order_history.get(user_id, [])})


# restaurant_details = {"location": "123 Main St", "phone": "123-456-7890"}  # Sample data

# def get_restaurant_details():
#     return json.dumps({"restaurant_details": restaurant_details})


# feedbacks = []  # Sample data

# def leave_feedback(user_id, feedback):
#     feedbacks.append({"user_id": user_id, "feedback": feedback})
#     return json.dumps({"success": "Feedback submitted"})


# waiting_list = []  # Sample data

# def join_waiting_list(name, contact):
#     waiting_list.append({"name": name, "contact": contact})
#     return json.dumps({"success": "Added to waiting list"})


# loyalty_points = {}  # Sample data

# def check_loyalty_points(user_id):
#     return json.dumps({"points": loyalty_points.get(user_id, 0)})


# events = []  # Sample data

# def book_event(event_type, date, number_of_guests):
#     event = {"type": event_type, "date": date, "guests": number_of_guests}
#     events.append(event)
#     return json.dumps({"success": "Event booked", "event_details": event})


def run_conversation(user_input, file_name=None):
    messages = [{"role": "user", "content": user_input}]
    functions = [
        {
            "name": "get_menu_information",
            "description": "Get information about a menu", 
            "parameters": {
                "type": "object",
                "properties": {
                    "menu_name": {
                        "type": "string",
                        "description": "The information of the menu "
                    }
                },
                "required": ["menu_name"]
            }
        },
        {
            "name": "add_to_cart",
            "description": "Add an item to the cart",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "special_request": {"type": "string"},
                    "follow_up_responses": {"type": "object", "description": "Follow-up responses related to the item"}
                },
                "required": ["item_name"]
            },
        },
        {
            "name": "view_cart",
            "description": "View the items in the cart",
            "parameters": {
                "type": "object",  # Specify object type
                "properties": {}   # No required properties
            }
        },
        # {
        #     "name": "place_order",
        #     "description": "Place an order with the items in the cart",
        #     "parameters": {
        #         "type": "object",  # Specify object type
        #         "properties": {}   # No required properties
        #     }
        # },
        # {
        #     "name": "provide_suggestions",
        #     "description": "Provide suggestions for menu items",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "category": {"type": "string", "description": "Category of the menu to provide suggestions"}
        #         },
        #         "required": []
        #     },
        # },
        # {
        #     "name": "ask_follow_up",
        #     "description": "Ask follow-up questions based on the ordered item",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "item_name": {"type": "string", "description": "Item name to ask follow-up questions about"}
        #         },
        #         "required": ["item_name"]
        #     },
        # },
        # {
        #     "name": "calculate_total",
        #     "description": "Calculate the total price of the items in the cart",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "menu_data": {
        #                 "type": "array",
        #                 "items": {
        #                     "type": "object",
        #                     "properties": {
        #                         "item_name": {"type": "string"},
        #                         "price": {"type": "number"}
        #                     },
        #                     "required": ["item_name", "price"]
        #                 },
        #                 "description": "Menu data loaded from the uploaded file"
        #             }
        #         },
        #         "required": ["menu_data"]
        #     }
        # },
        # {
        #     "name": "make_reservation",
        #     "description": "Make a restaurant reservation",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "date": {"type": "string", "description": "Reservation date"},
        #             "time": {"type": "string", "description": "Reservation time"},
        #             "number_of_guests": {"type": "integer", "description": "Number of guests"},
        #             "last_name": {"type": "string", "description": "Last name of the person making the reservation"},
        #         },
        #         "required": ["date", "time", "number_of_guests", "last_name"],
        #     },
        # },
        # {
        #     "name": "check_reservation_status",
        #     "description": "Check the status of a reservation",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "last_name": {"type": "string"},
        #             "reservation_id": {"type": "integer", "description": "Optional"}
        #         },
        #         "required": ["last_name"]
        #     }
        # },

        # {
        #     "name": "cancel_reservation",
        #     "description": "Cancel a reservation",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "reservation_id": {"type": "integer"}
        #         },
        #         "required": ["reservation_id"]
        #     }
        # },
        # {
        #     "name": "update_order",
        #     "description": "Update an existing order",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "order_id": {"type": "integer"},
        #             "changes": {"type": "object"}
        #         },
        #         "required": ["order_id"]
        #     }
        # },
        # {
        #     "name": "get_special_offers",
        #     "description": "Retrieve special offers and promotions",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {}
        #     }
        # },
        # {
        #     "name": "get_allergy_information",
        #     "description": "Retrieve information related to specific allergy types",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "allergy_type": {"type": "string"}
        #         },
        #         "required": ["allergy_type"]
        #     }
        # },
        # {
        #     "name": "review_order_history",
        #     "description": "Retrieve the order history for a specific user",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "user_id": {"type": "integer"}
        #         },
        #         "required": ["user_id"]
        #     }
        # },
        # {
        #     "name": "get_restaurant_details",
        #     "description": "Retrieve details about the restaurant's location, contact, etc.",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {}
        #     }
        # },
        # {
        #     "name": "leave_feedback",
        #     "description": "Submit feedback for a dining experience",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "user_id": {"type": "integer"},
        #             "feedback": {"type": "string"}
        #         },
        #         "required": ["user_id", "feedback"]
        #     }
        # },
        # {
        #     "name": "join_waiting_list",
        #     "description": "Join the waiting list for a table",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "name": {"type": "string"},
        #             "contact": {"type": "string"}
        #         },
        #         "required": ["name", "contact"]
        #     }
        # },
        # {
        #     "name": "check_loyalty_points",
        #     "description": "Check the loyalty points for a specific user",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "user_id": {"type": "integer"}
        #         },
        #         "required": ["user_id"]
        #     }
        # },
        # {
        #     "name": "book_event",
        #     "description": "Book an event such as private dining or special occasions",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "event_type": {"type": "string"},
        #             "date": {"type": "string"},
        #             "number_of_guests": {"type": "integer"}
        #         },
        #         "required": ["event_type", "date", "number_of_guests"]
        #     }
        # },
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
            functions=functions,
            function_call="auto",
        )
    except openai.error.InvalidRequestError as e:
        print(f"Error: {e}")
    #print(f"First Response{response}")
    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):
        available_functions = {
            "get_menu_information": get_menu_information,
            "add_to_cart": add_to_cart,
            "view_cart": view_cart,
            # "place_order": place_order,
            # "provide_suggestions":provide_suggestions,
            # "ask_follow_up": ask_follow_up,
            # "calculate_total": calculate_total,
            # "make_reservation": make_reservation,
            # "check_reservation_status": check_reservation_status,
            # "cancel_reservation": cancel_reservation,
            # "update_order": update_order,
            # "get_special_offers": get_special_offers,
            # "get_allergy_information": get_allergy_information,
            # "review_order_history": review_order_history,
            # "get_restaurant_details": get_restaurant_details,
            # "leave_feedback": leave_feedback,
            # "join_waiting_list": join_waiting_list,
            # "check_loyalty_points": check_loyalty_points,
            # "book_event": book_event,
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        # Hypothetical debug logging
        # print(f"Function args before calling: {function_args}")

        # # Hypothetical function call
        # if function_name == "get_menu_information":
        #     try:
        #         function_response = function_to_call(**function_args)
        #     except TypeError as e:
        #         print(f"TypeError occurred: {e}")
        # elif function_name == "update_order":
        #     # Hard-coded changes for simulation
        #     hard_coded_changes = {'quantity': 2, 'special_request': 'No onions'}
        #     function_args['changes'] = hard_coded_changes
        #     function_response = function_to_call(**function_args)
        # else:
        function_response = function_to_call(**function_args)


        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
        ) # get a new response from GPT where it can see the function response
        #print(f"Second Response{response}") 
        # Extract the message text from the OpenAI response
        response_text = second_response["choices"][0]["message"]["content"]
        return response_text



# @app.route('/')
# def upload_page():
#     return render_template('upload.html')  # HTML for upload page

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     uploaded_file = request.files['file']
#     if uploaded_file.filename != '':
#         # Check if the upload folder exists; if not, create it
#         if not os.path.exists(app.config['UPLOAD_FOLDER']):
#             os.makedirs(app.config['UPLOAD_FOLDER'])
        
#         # Save the uploaded file
#         uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
#     return redirect(url_for('chatbot_page'))


# # @app.route('/chatbot')
# # def chatbot_page():
# #     return render_template('chatbot.html')  # HTML for chatbot page


# @app.route('/conversation', methods=['POST'])
# def conversation():
#     user_input = request.form['user_input']
    
#     # Get the latest uploaded file name
#     uploaded_file_name = os.listdir(app.config['UPLOAD_FOLDER'])[-1].split('.')[0] if os.listdir(app.config['UPLOAD_FOLDER']) else None
    
#     response = run_conversation(user_input, file_name=uploaded_file_name)
#     return render_template('chatbot.html', response=response)

# import logging

# logging.basicConfig(level=logging.DEBUG)

def run_bulk_conversations(user_inputs, file_name=None):
    bulk_responses = []
    try:
        for user_input in user_inputs:
            response = run_conversation(user_input)
            bulk_responses.append(response)
        return bulk_responses
    except Exception as e:
        # logging.error(f"Error in run_bulk_conversations: {e}")
        return {"error": "An error occurred"}

@app.route('/', methods=['GET'])
def bulk_conversation_form():
    return render_template('bulk_conversation_interface.html')  # Render the HTML template

@app.route('/bulk_conversation', methods=['POST'])
def bulk_conversation():
    try:
        data = request.json  # Parse JSON data from the request

        # Extract user_inputs and file_name from the JSON data
        user_inputs = data.get('user_inputs', [])
        file_name = data.get('file_name', None)

        # Run the bulk conversations function
        bulk_responses = run_bulk_conversations(user_inputs, file_name)

        return jsonify({'responses': bulk_responses})  # Return responses as JSON
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=False)
