
# Yext Coding Challenge

The Yext coding challenge consists of a simple Flask API that receives a list of contacts and sorting instructions. The endpoint sorts the list of contacts based on the provided instructions.



## Authors

- Roberto Requejo Fernández


## Run Guide

Requirements

```bash
    pip install Flask==3.1.0
```
    
Now we need to start the service with the following:
```bash
    python app.py
```

The app will listen in port 5000
## API Reference

#### Sort Contacts

```http
  POST /sort
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `sort_order` | `dictionary` | **Required**. A dictionary of the sorting specifications |
| `contacts` | `array` | **Required**. A list of contacts to sort |

It will return a list of dictionaries that contain the sorted contacts based on requirements

 ### Example Request

 ```bash
  curl -X POST http://127.0.0.1:5000/sort \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "sort_order": {
      "last_contacted": "desc",
      "last_name": "asc",
      "first_name": "asc"
    },
    "contacts": [
      {
        "first_name": "Alice",
        "last_name": "Smith",
        "zip_code": "12345",
        "phone_number": "555-0101",
        "last_contacted": "2024-04-10T14:33:20Z"
      },
      {
        "first_name": "Bob",
        "last_name": "Smith",
        "zip_code": "54321",
        "phone_number": "555-0102",
        "last_contacted": "2024-04-12T09:15:00Z"
      },
      {
        "first_name": "Charlie",
        "last_name": "Brown",
        "zip_code": "67890",
        "phone_number": "555-0103",
        "last_contacted": "2024-04-09T22:45:10Z"
      }
    ]
  }

```

### Expected Output

 ```bash

 {
  "contacts": [
    {
      "first_name": "Bob",
      "last_name": "Smith",
      "zip_code": "54321",
      "phone_number": "555-0102",
      "last_contacted": "2024-04-12T09:15:00Z"
    },
    {
      "first_name": "Alice",
      "last_name": "Smith",
      "zip_code": "12345",
      "phone_number": "555-0101",
      "last_contacted": "2024-04-10T14:33:20Z"
    },
    {
      "first_name": "Charlie",
      "last_name": "Brown",
      "zip_code": "67890",
      "phone_number": "555-0103",
      "last_contacted": "2024-04-09T22:45:10Z"
    }
  ]
}

```


## Extra

I created three classes that I worked with: Contacts, SortingOrder, and Request. This approach makes the code easier to scale and maintain.

Using classes also simplifies validation and helps inform the user when they’ve made a mistake or if the JSON data is not formatted correctly as required.