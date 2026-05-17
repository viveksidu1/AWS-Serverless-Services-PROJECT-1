import json
import boto3
import urllib.parse # This helps clean up weird form characters!

def lambda_handler(event, context):
    try:
        http_method = event['httpMethod']
        
        # 1. Handle the GET request (showing the form)
        if http_method == 'GET':
            html_file = open('contactus.html', 'r')
            html_content = html_file.read()
            html_file.close()
            
            return {
                'statusCode': 200,
                'headers': {"Content-Type": "text/html"},
                'body': html_content
            }
            
        # 2. Handle the POST request (submitting the form)
        elif http_method == 'POST':
            
            # unquote_plus cleans up the text (turns %40 into @, and + into spaces)
            form_body = urllib.parse.unquote_plus(event['body'])
            
            # Find the email
            pieces = form_body.split('&')
            user_email = ""
            for piece in pieces:
                if piece.startswith("email="):
                    user_email = piece.replace("email=", "")
            
            # Connect to DynamoDB
            client = boto3.client('dynamodb')
            
            # --- CHECK IF EMAIL ALREADY EXISTS ---
            # Added double quotes around table name, just in case!
            check_query = "SELECT * FROM \"vivektable\" WHERE email = '" + user_email + "'"
            check_response = client.execute_statement(Statement=check_query)
            
            # Using .get('Items', []) is a safer way to check if it found anything
            if len(check_response.get('Items', [])) > 0:
                return {
                    'statusCode': 200,
                    'headers': {"Content-Type": "text/html"},
                    'body': "<h2>Email ID is already registered! Please go back and try another.</h2>"
                }
            
            # --- IF EMAIL IS NEW, SAVE IT ---
            json_body = form_body.replace("=", "' : '")
            json_body = json_body.replace("&", "', '")
            sql_query = "INSERT INTO \"vivektable\" value {'" + json_body + "'}"
            
            client.execute_statement(Statement=sql_query)
            
            # Open the success page and return it
            success_file = open('success.html', 'r')
            success_content = success_file.read()
            success_file.close()
            
            return {
                'statusCode': 200,
                'headers': {"Content-Type": "text/html"},
                'body': success_content
            }

    # --- NEWBIE ERROR CATCHER ---
    # If ANYTHING goes wrong, it will print the error on the webpage!
    except Exception as e:
        return {
            'statusCode': 200, 
            'headers': {"Content-Type": "text/html"},
            'body': f"<h2>Oops! An error happened:</h2><p>{str(e)}</p>"
        }