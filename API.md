## List TODOs

 * URL: /todo/
 * HTTP Method: GET
 
### Example Response

    [
      {
        "id": 1,
        "created": "29.08.2016 11:34",
        "changed": "29.08.2016 11:57",
        "title": "Tenetur Illum Tempora Quisquam Eaque Hic",
        "completed": true
      },
      {
        "id": 2,
        "created": "29.08.2016 11:34",
        "changed": "29.08.2016 11:34",
        "title": "Beatae Consectetur Reiciendis Deserunt Facilis Consequatur",
        "completed": false
      },
      ...
    ]

## Get all active TODOs

 * URL: /todo/active/
 * HTTP Method: GET
 
### Example Response

    [
      {
        "id": 2,
        "created": "29.08.2016 11:34",
        "changed": "29.08.2016 11:34",
        "title": "Beatae Consectetur Reiciendis Deserunt Facilis Consequatur",
        "completed": false
      },
      ...
    ]
    
## Get all completed TODOs

 * URL: /todo/completed/
 * HTTP Method: GET
 
### Example Response

    [
      {
        "id": 1,
        "created": "29.08.2016 11:34",
        "changed": "29.08.2016 11:57",
        "title": "Tenetur Illum Tempora Quisquam Eaque Hic",
        "completed": true
      },
      ...
    ]

## Add a TODO

 * URL: /todo/
 * HTTP Method: POST
 
### Example Request

    {
      "title": "Create Web API for TODO MVC"
    }
    
### Example Response

    HTTP 201 OK
    {
      "id": 8,
      "created": "02.09.2016 17:46",
      "changed": "02.09.2016 17:46",
      "title": "Create Web API for TODO MVC",
      "completed": false
    }
    
## Get a TODO

 * URL: /todo/{id}
 * HTTP Method: GET
 
### Example Request

    {
      "id": 8
    }
    
### Example Response

    HTTP 200 OK
    {
      "id": 8,
      "created": "02.09.2016 17:46",
      "changed": "02.09.2016 17:46",
      "title": "Create Web API for TODO MVC",
      "completed": false
    }
    
## Update a TODO

 * URL: /todo/{id}
 * HTTP Method: PUT
 
### Example Request

    {
      "id": 8,
      "title": "Create Web API for TODO MVC",
      "completed": true
    }
    
### Example Response

    HTTP 200 OK
    {
      "id": 8,
      "created": "02.09.2016 17:46",
      "changed": "02.09.2016 17:48",
      "title": "Create Web API for TODO MVC",
      "completed": true
    }
    
## Delete a TODO

 * URL: /todo/{id}
 * HTTP Method: DELETE
 
### Example Request

    {
      "id": 1
    }
    
### Example Response

    HTTP 204 OK
    no content
