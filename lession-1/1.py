import requests
import json
username = input("Enter the github username:")
request = requests.get('https://api.github.com/users/'+username+'/repos')
result = request.json()
status_code = request.status_code

if request.ok:
    with open("result.json", "w", encoding="utf-8") as write_f:
        json.dump(result, write_f, indent=4)
    print("Результат запроса сохранен в файле result.json")
else:
    print('Ошибка')

