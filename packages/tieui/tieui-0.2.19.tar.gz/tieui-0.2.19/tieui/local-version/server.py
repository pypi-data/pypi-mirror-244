from flask_cors import CORS
from flask_socketio import SocketIO, Namespace
from flask import Flask, request, jsonify
import subprocess
import threading
import json
import os
import openai
import stripe
import signal
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re
import tempfile


stripe.api_key = 'sk_live_V0i7sCCumeu7cM6y2Azt1KFq'
SENDGRID_API_KEY='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'

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
CORS(app)


class CustomNamespace(Namespace):
    def __init__(self, namespace, app_name):
        super().__init__(namespace)
        self.app_name = app_name

    def on_connect(self):
        print('Client connected to {self.app_name}')

    def on_disconnect(self):
        print('Client disconnected from {self.app_name}', self.app_name)
        stop_subprocess(self.app_name)

    def on_message(self, message):
        print('received message on {self.app_name}:', message)

    def on_publish_event(self):
        self.emit('update', {'data': 'New data from {self.app_name}.adk.publish()'})

    def on_executeCallback(self, item):
        socketio.emit('callBack', item)
        self.emit('callBack', item)



@app.route('/send-contact-email', methods=['POST'])
def sendEmailContact():
    toEmail = request.json.get('to')
    phone = request.json.get('phone')
    msg = request.json.get('msg')
    name = request.json.get('name')

    ct = '<strong> email: '+toEmail+'phone: '+phone+'msg: '+msg+'name: '+name+'</strong>'

    message = Mail(
        from_email='jlmontalvof@gmail.com',
        to_emails='jlmontalvof@gmail.com',
        subject='New Contact Request',
        html_content=ct
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        # Return a success response
        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        print(e.message)

        # Return an error response
        return jsonify({"error": "Failed to send email"}), 500


@app.route('/publish/<appName>', methods=['POST'])
def publish(appName):
    print('puto')
    # print(request)
    data = request.json  # Get the entire JSON object
    # print('started publish', data)
    pythonCode = data.get('code')
    components = data.get('components')
    styling = data.get('styling')
    tabStyling = data.get('tab_styling')
    namespace =f'/{appName}'
    socketio.emit('update', {'data': components, 'code': pythonCode, 'styling': styling, 'tab_styling': tabStyling}, namespace=namespace)
    return {'status': 'success'}

@app.route('/test_emit/<appName>')
def test_emit(appName):
    namespace =f'/{appName}'
    socketio.emit('update', {'data': 'Test data from /test_emit'}, namespace=namespace)
    return {'status': 'Test emit success'}

running_subprocesses = {}

@app.route('/execute_python_code/<appName>', methods=['POST'])
def execute_python_code(appName):
    try:
        # Get the Python code from the request
        python_code = request.json.get('pythonCode', '')

        print('the python code')
        print(python_code)
        python_code = re.sub(r'from tieui import TieUi', f'from tieui_module import TieUi', python_code)
        print(python_code)
        # Execute the Python code and capture the output
        def execute_code():
            result = execute_remote_code_async(python_code, appName)
            return result
        
        process = subprocess.Popen(['python3', '-c', python_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp)
        running_subprocesses[appName] = process

        # result = threading.Thread(target=execute_code).start()

        return jsonify({'result': 0})
    except Exception as e:
        print({'error': str(e)})
        return jsonify({'error': str(e)})

def execute_remote_code_async(command, appName):
    try:
        # Create a temporary Python script file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(command)
            temp_file_path = temp_file.name

        # Run the Python script using subprocess, and create a process group
        process = subprocess.Popen(['python3', temp_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp)

        # Store the process object in the dictionary indexed by app name
        running_subprocesses[appName] = process

        # Wait for the subprocess to finish and capture the output
        stdout, stderr = process.communicate()

        # Print and return the result
        result = {'stdout': stdout.decode('utf-8'), 'stderr': stderr.decode('utf-8')}
        return result
    except subprocess.CalledProcessError as e:
        return {'error_code': e.returncode, 'error_output': e.stderr.decode('utf-8')}
    except Exception as e:
        return {'error': str(e)}
    finally:
        # Remove the temporary file after execution
        os.remove(temp_file_path)

@app.route('/run-published-code', methods=['POST'])
def run_code_from_route():
    print('running published code')
    data = request.get_json()
    file_location = data.get('location')
    independent = data.get('isIndependent')
    new_app_name = data.get('newAppName')
    app_n = data.get('appName')
    og_app_n = data.get('ogAppName')

    print(app_n)
    print(og_app_n)

    if file_location is None:
        return jsonify(error="No Location Provided")
    
    try:
        if independent:
            with open(file_location, 'r') as file:
                content = file.read()

            # Use a regular expression to find and replace the app_name value
            print(file_location)
            file_name = file_location.split('/')[-1].rsplit('.', 1)[0]
            print("THIS IS THE NAME: ", file_name)
            # content = re.sub(r'app_name\s*=\s*".*?"', f'app_name="{new_app_name}"', content)

            content = re.sub(r'app_name\s*=\s*".*?"', f'app_name="{new_app_name}", og_app_name="{file_name}"', content)
            print(content)

            # Run the Python script using subprocess and store the process object
            print('the content')
            print(content)
            process = subprocess.Popen(['python3', '-c', content], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp)
            running_subprocesses[new_app_name] = process
        else:
            # Run the Python script using subprocess and store the process object
            process = subprocess.Popen(['python3', file_location], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setpgrp)
            running_subprocesses[new_app_name] = process

        return jsonify(stdout="", stderr=""), 200
    except subprocess.CalledProcessError as e:
        return jsonify(error=str(e), stderr=e.stderr), 400
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/stop_subprocess/<appName>', methods=['POST'])
def stop_subprocess(appName):
    try:
        # Check if the subprocess is running for the given app name
        if appName in running_subprocesses:
            # Terminate the subprocess and its process group
            os.killpg(os.getpgid(running_subprocesses[appName].pid), signal.SIGTERM)
            del running_subprocesses[appName]
            return jsonify(message=f'Subprocess for {appName} stopped successfully')
        else:
            return jsonify(error=f'No subprocess found for {appName}'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500
@app.route('/publish-code/<appName>', methods=['POST'])
def publish_code(appName):
    data = request.get_json()
    code = data.get('code')
    app_name = data.get('app_name')
    layout = data.get('layout')
    tabLayout = data.get('tabLayouts')
    # save_directory = f'./{appName}-'  # Replace with your desired directory
    save_directory = ''  
    # Construct the file path with app_name as the filename
    file_path = save_directory + app_name + '.py'
    layout_file_path = save_directory + app_name + '_layout.json'
    tabLayout_file_path = save_directory + app_name + '_tabLayout.json'
    print("THIS IS THE CODE: ", code)
    try:
        # Open the file for writing and save the code
        with open(file_path, 'w') as file:
            file.write(code)

        with open(layout_file_path, 'w') as layout_file:
            json.dump(layout, layout_file, indent=4)
        
        with open(tabLayout_file_path, 'w') as tabLayout_file:
            json.dump(tabLayout, tabLayout_file, indent=4)
            
        return jsonify({'message': 'Code saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/execute_ai_prompt', methods=['POST'])
def execute_ai_prompt():
    try:
        # Get the prompt from the request
        prompt = request.json.get('prompt', '')
        newAppName = request.json.get('appName', '')

        # Define the system message for OpenAI
        system_message2 = '''from tieui import TieUi

tie = TieUi(app_name="AppName")


text_input_value = 0.0
text_input_value2 = 0
text_input_value3 = 0

def calculate_u(r, p, n):
    u_values = [p]
    
    for i in range (0 , n):
        u_i = r * u_values[i] * (1 - u_values[i]) #Logistic Map formula
        u_values.append(u_i)
        
    return u_values

def custom_button_callback_handler(item):
    print("CUSTOM")
    try:
        r = float(text_input_value)
        p = float(text_input_value2)
        n = int(text_input_value3)
        result = calculate_u(r, p, n)
        tie.components[4]['settings']['label'] = "Result: " + str(result[-1])  # I assume you want the last value, change this as needed
    except ValueError:
        tie.components[4]['settings']['label'] = "Invalid input"
    except TypeError:
        tie.components[4]['settings']['label'] = "Error in calculation"
    tie.update()

def handle_text_input_change(item):
    global text_input_value
    new_value = item.get("value", "")
    text_input_value = new_value

def handle_text_input_change2(item):
    global text_input_value2
    new_value = item.get("value", "")
    text_input_value2 = new_value

def handle_text_input_change3(item):
    global text_input_value3
    new_value = item.get("value", "")
    text_input_value3 = new_value

def handle_checkbox_change(item):
    print(item)
def handle_slider_change(item):
    print(item)
def handle_switch_change(item):
    print(item)
def handle_chip_clicked(item):
    val = item.get("value", "")
    if (val == "delete"):
        print("chip deleted")
    else:
        print("chip Clicked")
def handle_select_change(item):
    print(item)
    tie.components[11]['settings']['value'] = item.get("value", '')
    tie.update()

def handle_update(item):
    print("PUTO")
tie.add(tie.textBox({"id": "unique-id-1","label": "A Float R", "variant": "outlined"},handle_text_input_change))
tie.add(tie.textBox({"id": "unique-id-2","label": "Initial Value P", "variant": "outlined"},handle_text_input_change2))
tie.add(tie.textBox({"id": "unique-id-2","label": "Non Negative Integer", "variant": "outlined"},handle_text_input_change3))

tie.add(tie.button({"id": "unique-id-3", "label": "Add Numbers", "variant": "outlined"}, custom_button_callback_handler))
tie.add(tie.label({"label": "Result: ", "variant": "h6", "color": "black"}))
tie.add(tie.checkbox({"label": "Result: "}, handle_checkbox_change))
tie.add(tie.checkbox({"label": "Result: ", "labelPlacement": "bottom"}, handle_checkbox_change))
tie.add(tie.slider({"min": 5, "max": 30, "step": 1}, handle_slider_change))
tie.add(tie.switch({"label": "Result: "}, handle_switch_change))
tie.add(tie.chip({"label": "Result: "}, handle_chip_clicked))
tie.add(tie.chip({"label": "Result: ", "variant": "outlined"}, handle_chip_clicked))
tie.add(tie.progress({"color": "success"}))
options = [
    {"label": "Option 1", "value": "option1"},
    {"label": "Option 2", "value": "option2"},
    {"label": "Option 3", "value": "option3"},
]
# Add a select component to your TieUi application
tie.add(tie.select({
    "id": "unique-id-3",  # Replace with a unique identifier
    "options": options,  # List of selectable options
    "label": "Select label",
    "variant": "outlined",  # Variant of the select component
    "value": "option1"  # Provide a default value that matches one of the available options
}, handle_select_change))

data_grid_component = tie.dataGrid(
    {
        "rows": [
            {
                "id": 1,
                "column1": "Value 1",
            }
        ],
        "columns": [
            {
                "field": "column1",
                "headerName": "Column 1",
                "width": 150,
            }
        ],
        "options": {},  # Add any options you need for the DataGrid
    }
)
tie.add(data_grid_component)

tab1_components = [
    tie.label({"label": "Content for Tab 1", "variant": "body1"}),
    tie.chip({"label": "Result: "}, handle_chip_clicked),
    tie.select({
        "id": "unique-id-3",  # Replace with a unique identifier
        "options": [
    {"label": "Option 1", "value": "option1"},
    {"label": "Option 2", "value": "option2"},
    {"label": "Option 3", "value": "option3"},
],  # List of selectable options
        "label": "Select label",
        "variant": "outlined",  # Variant of the select component
        "value": "option1"  # Provide a default value that matches one of the available options
    }, handle_select_change)
]

tab2_components = [
    tie.label({"label": "Content for Tab 2", "variant": "body1"}),
    tie.button({"id": "unique-id-qw3", "label": "Add Numbers", "variant": "outlined"}, handle_update)
]

tabs_settings = {
    "value": 0,  # default active tab index
    "tab": [
        {"label": "Tab 1", "value": "tab1", "components": tab1_components},
        {"label": "Tab 2", "value": "tab2", "components": tab2_components},
        # ... more tabs if needed
    ]
}

tie.add(tie.links({"href": "https://tieui.app", "underline":"hover", "label": "underline hover"}))

tie.add(tie.tabs(tabs_settings))
tie.add(tie.alerts({"severity": "error", "label": "This is an error alert — check it out!"}))


tie.publish()
This is my sdk code to create UIs, the following questions in the chat are going to be based on that. Please only respond with code snippets include the whole implementation (meaning add imports and stuff) and NOTHING ELSE. NOT EVEN EXPLANATIONS.
          Make sure that the code will work. The order in which things happen is important. you have to define the Tieui() before any functions, for example...
        '''

        # Combine the system message and user prompt
        full_prompt = system_message2 + ' ' + prompt

        # Set your OpenAI API key
        openai.api_key = "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"
        # PROMPT_TOKENS = len(openai.tokenize(full_prompt))
        # MAX_TOKENS = 2048

        # response_tokens = MAX_TOKENS - PROMPT_TOKENS
        # Generate code using GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": full_prompt
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=0,
            max_tokens=1500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Check if the response is successful
        if response.id:
            code = response.choices[0].message.content
            code = re.sub(r'app_name\s*=\s*".*?"', f'app_name="{newAppName}"', code)
            code = re.sub(r'```python', f'', code)
            code = re.sub(r'```', f'', code)
            return jsonify({'code': code})
        else:
            return jsonify({'error': f'Failed to generate code. OpenAI response: {response}'})
    except Exception as e:
        return jsonify({'error': str(e)})

custom_namespaces = {}

def register_custom_namespace(app_name):
    namespace = f'/{app_name}'
    custom_namespace = CustomNamespace(namespace, app_name)
    socketio.on_namespace(custom_namespace)
    # Store the custom_namespace object itself, not a 'sid'
    custom_namespaces[app_name] = custom_namespace
    print(socketio.server.manager.rooms.keys())
    print(socketio.server.namespace_handlers.keys())

def unregister_all_routes_and_namespaces():
    global custom_namespaces
    namespace_copy = dict(socketio.server.namespace_handlers)
    
    for namespace in namespace_copy.keys():
        # Disconnect clients from the namespace
        socketio.server.namespace_handlers.pop(namespace)
        socketio.server.disconnect(namespace)
    print(socketio.server.namespace_handlers.keys())
    custom_namespaces.clear()  # Clear the dictionary

@app.route('/register-app/<appName>', methods=['POST'])
def register_app(appName):
    print('registering')
    register_custom_namespace(appName)
    return {'status': 'app registered'}

@app.route('/unregister-all', methods=['POST'])
def unregister_all():
    unregister_all_routes_and_namespaces()
    
    return jsonify({'status': 'All routes and namespaces unregistered.'})

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  userId = request.json.get('userId', '')
  price = request.json.get('price', '')
  units = request.json.get('units', '')
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'TieUi Subscription',
        },
        'unit_amount': price,
      },
      'quantity': units,
    }],
    mode='payment',
    success_url='https://tieui-fe-366c37caf130.herokuapp.com/success?userId='+userId+"&numSubs="+str(units),
    cancel_url='https://tieui-fe-366c37caf130.herokuapp.com/cancel',
  )

  return {"url": session.url, "code": 303}

@app.route('/create-subscription', methods=['POST'])
def create_subscription():
    userId = request.json.get('userId', '')
    priceId = request.json.get('priceId', '')  # The ID of the Stripe Price object
    customer_email = request.json.get('customer_email', '')  # The customer's email
    quantity = request.json.get('quantity', 1)  # Default to 1 if quantity is not provided
    new_payment_id = request.json.get('new_payment_id', False)

    otherId = "price_1O3KNSKteYI3s5fN7TCoKFij"
    priceId = "price_1O2WehKteYI3s5fNcmJTOBnH"
    if(new_payment_id == True):
        priceId = otherId
    # Create a customer if it doesn't exist (you can also retrieve an existing customer)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=customer_email,  # Replace with the customer's email
        line_items=[
            {
                'price': priceId,
                'quantity': quantity,
            },
        ],
        mode='subscription',
        success_url='https://tieui-fe-366c37caf130.herokuapp.com/success?userId=' + userId+"&numSubs="+str(quantity),
        cancel_url='https://tieui-fe-366c37caf130.herokuapp.com/cancel',
    )

    return {"url": session.url, "code": 303}

@app.route('/health-check', methods=['GET'])
def health_check():
    print('checking health')
    return {'status': 300}
if __name__ == '__main__':
    print('server started')
    port = int(os.environ.get('PORT', 8080))
    socketio.run(app, host='0.0.0.0', port=port)
