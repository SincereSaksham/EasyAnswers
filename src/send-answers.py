import requests
from bs4 import BeautifulSoup
import json

def extract_form_details(form_url):
    response = requests.get(form_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the form action URL
    form = soup.find('form')
    action_url = form['action'] if form else None

    # Extract fbzx hidden input field
    fbzx_input = soup.find('input', {'name': 'fbzx'})
    fbzx_value = fbzx_input['value'] if fbzx_input else None

    # Extract field entry IDs and option values for multiple choice/checkbox questions
    form_fields = {}
    options_map = {}  # Store options for each question
    
    questions = soup.find_all('div', class_='Qr7Oae')  # Adjust class name as needed
    for question in questions:
        question_text = question.find(class_='M7eMe').text.strip()
        
        # For text fields or text areas
        input_field = question.find('input') or question.find('textarea')
        if input_field:
            entry_id = input_field['name']
            form_fields[question_text] = entry_id

        # Extract options for radio buttons or checkboxes
        options = question.find_all('div', {'data-value': True})  # Use generic attribute filter
        if options:
            options_map[question_text] = {opt.get_text(strip=True): opt.get('data-value', '') for opt in options}

    return action_url, form_fields, fbzx_value, options_map

def submit_form(action_url, form_fields, answers, fbzx_value, options_map):
    form_data = {}

    # Map the answers to their corresponding entry IDs and option values
    for question, entry_id in form_fields.items():
        if question in answers:
            answer = answers[question]
            
            # If the question has predefined options (multiple choice/checkbox), use the value attribute
            if question in options_map and answer in options_map[question]:
                form_data[entry_id] = options_map[question][answer]  # Use the option's value
            else:
                form_data[entry_id] = answer  # Use the text answer for regular questions
        else:
            form_data[entry_id] = ''  # Empty string if no answer is available

    # Include additional required parameters for form submission
    form_data['draftResponse'] = []
    form_data['pageHistory'] = 0
    if fbzx_value:
        form_data['fbzx'] = fbzx_value  # Add the fbzx token

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': action_url
    }

    # Send POST request to submit the form
    response = requests.post(action_url, data=form_data, headers=headers)

    if response.status_code == 200:
        print('Form submitted successfully.')
    else:
        print(f'Failed to submit the form. Status code: {response.status_code}')

# Main execution
form_url = '<LINK-TO-GOOGLE-FORM>'

# Step 3: Extract form details (action URL, field entry IDs, fbzx token, options)
action_url, form_fields, fbzx_value, options_map = extract_form_details(form_url)

# Load answers from the JSON file
with open('answers.json', 'r') as f:
    answers = json.load(f)

# Step 4: Submit the form with the extracted details and answers
if action_url:
    submit_form(action_url, form_fields, answers, fbzx_value, options_map)
else:
    print('Failed to extract form action URL.')
