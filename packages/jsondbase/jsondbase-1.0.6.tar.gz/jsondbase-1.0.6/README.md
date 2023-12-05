# JsonDBase

Use the json file as a local database and do not need to install anything else

feature add, delete, exist, find in any level nested json tree

# Install

```
pip3 install jsondbase
```

# Usage

### isRecordExist
```
from jsondbase import LocalDatabase

db = LocalDatabase(dbname="session.json")

"""
example of session.json
[{
    "company": "ABC"  
    "employee": {  
        "name":       "sonoo",   
        "salary":      56000,   
        "married":     true  
    }  
}]  
"""
#                 value  key
db.isRecordExist("ABC", "comapny")
# find in other level
db.isRecordExist("sonoo", "employee", "name")
```

### addRecord
```
from jsondbase import LocalDatabase

db = LocalDatabase(dbname="session.json")

json = {
    "company": "ABC"  
    "employee": {  
        "name":       "sonoo",   
        "salary":      56000,   
        "married":     true  
    }  
}  

db.addRecord(json)
```

### deleteRecord

```
from jsondbase import LocalDatabase

db = LocalDatabase(dbname="session.json")

"""
example of session.json
[{
    "company": "ABC"  
    "employee": {  
        "name":       "sonoo",   
        "salary":      56000,   
        "married":     true  
    }  
}]  
"""
#                 value  key
db.deleteRecord("ABC", "comapny")
# delete in other level
db.deleteRecord("sonoo", "employee", "name")
```

### getRecord
```
from jsondbase import LocalDatabase

db = LocalDatabase(dbname="session.json")

"""
example of session.json
[{
    "company": "ABC"  
    "employee": {  
        "name":       "sonoo",   
        "salary":      56000,   
        "married":     true  
    }  
}]  
"""
#                 value  key
db.getRecord("ABC", "comapny")
# get record in other level
db.getRecord("sonoo", "employee", "name")
```