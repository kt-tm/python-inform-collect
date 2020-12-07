import requests
api_key = '685mxu**********************************'
sender_email = 'tokarevak85@gmail.com'
sender_name = 'katya'
format = 'json'
email = input("Введите email для отправки электронного письма:")
subject = input("Введите тему электронного письма:")
body = input("Введите текст электронного письма:")
params = {'format': format,
          'api_key': api_key,
          'email': email,
          'sender_email': sender_email,
          'sender_name': sender_name,
          'subject': subject,
          'body': body,
          'list_id': 1}
request = requests.get('https://api.unisender.com/ru/api/sendEmail', params)
result = request.json()
status_code = request.status_code
print(status_code)
print(result)
