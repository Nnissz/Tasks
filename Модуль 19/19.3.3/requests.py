import requests

def Print(m):
    print(m)
    print(res.text)
    print(res.status_code)

body = {
    "id": "10001",
    "category": {
        "id": 0,
        "name": "string"
    },
    "name": "pussycat",
    "status": "available"
}
res = requests.post(url="https://petstore.swagger.io/v2/pet",
                    headers={},#{"content-type": "application/json", "accept": "application/json"},
                    #data=body,
                    json=body)
Print('---POST---')

res = requests.get(url="https://petstore.swagger.io/v2/pet/10001",
                   params={'status': 'available'},
                   headers={'accept': 'application/json'})
Print('---GET---')

body = {
  "id": 0,
  "category": {
    "id": 1,
    "name": "string"
  },
  "name": "doggie123",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}
res = requests.put(url="https://petstore.swagger.io/v2/pet",
                   json=body)
Print('---PUT---')

res = requests.delete(url="https://petstore.swagger.io/v2/pet/10001")
Print('---DELETE---')

