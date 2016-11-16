# Json Schema
For now, all JSON requests will pass through http://example.com:12345/data and the exact url will be determined once the server is running on tux.

The current available strings for category name are as follows:

 * `"ip"`
 * `"disk_usage"`
 
All requests can potentially result in a 500 Server Error response (it shouldn't but it's possible), and your code should be capable of responding accordingly.

All responses from the server should contain a key `"status"` which will have a value of either `"success"` or `"failure"` which can be checked before parsing the rest of the message.

## Failures
All failed messages will occur in parallel with some HTTP code in the 400 or 500 series and take on the following format:
```
{
    "status": "failure",
    "reason": "some explanation of the failure if possible"
}
```

No guarantees will be made about the contents of the message, but it may be useful for debugging purposes.

## Requesting data from the server
The first request to the server from the client must be logging in to receive the user's ID from the server. All subsequent requests require this ID in a key called `"user"`. Responses will be sent with the HTTP code 403 Forbidden if the user does not have access to the requested machine. 

### Logging In
Since there is currently no protocol for maintaining passwords and security, those fields can be ignored, but this message can be used for getting the user id from the server which is necessary for subsequent requests

#### Request
```
{
    "user": "username",
    "password": "password, or blank for now"
}
```

#### Response
```
{
    "status": "success",
    "id": "user id"
}
```

### Getting Machine Information
Machines can have names set by the user and a list of different users who can access it. This is the protocol for retrieving that data. Machines should be displayed using the user's assigned name, so this should be done before displaying any data collected from the server.

#### Request
```
{
    "machine": "uuid",
    "user": "user id"
}
```

#### Response
```
{
    "status": "success",
    "name": "user-assigned name",
    "users": [
        "user id 1",
        "user id 2",
        ...
    ]
}
```


### Getting data for a single machine
This works in a paging format where some number of records can be selected. There is currently no limit on the number of records which can be retrieved at once. Records are sent in order from newest to oldest.

#### Request
```
{
    "machine": "uuid",
    "category": "category name",
    "user": "user id",
    "start": 0, // Record to start counting from
    "count": 1000 // Number of records to retrieve
}
```

#### Response
```
{
    "status": "success",
    "last": 1000, // Number of last record retrieved
    "records": [
    {
        "machine": "uuid",
        "datetime": "ISO 8601: YYYY-MM-DDThh:mm:ss.sss",
        "data": "category dependent data encoding"
    },
    ...
    ]
}
```


### Getting data for multiple machines
This is identical to the protocol for a single machine with the omission of the machine key from the request. Only machines the user is authorized to access will be returned in the response. This may be an empty list if the user does not have authorization to access any machine.

#### Request
```
{
    "category": "category name",
    "user": "user id",
    "start": 0, // Record to start counting from
    "count": 1000 // Number of records to retrieve
}
```

#### Response
```
{
    "status": "success",
    "last": 1000, // Number of last record retrieved
    "records": [
    {
        "machine": "uuid",
        "datetime": "ISO 8601: YYYY-MM-DDThh:mm:ss.sss",
        "data": "category dependent data encoding"
    },
    ...
    ]
}
```

## Saving to the Database
All saving operations will return a 201 Created HTTP response code on success and 400 Bad Request on failure. Additionally, the body of the response will follow this JSON format:
```
{
    "status": "'success' or 'failure'",
    "reason": "some explanation of the failure if possible"
}
```

### Saving Statistic Data
```
{
    "machine": "uuid",
    "datetime": "ISO 8601: YYYY-MM-DDThh:mm:ss.sss",
    "category": "category name",
    "data": "arbitrary category-specific data encoded as string"
}
```

### Saving Machine-User Authorization
```
{
    "action": "'authorize' or 'deauthorize'",
    "user": "user id",
    "machine": "machine uuid"
}
```