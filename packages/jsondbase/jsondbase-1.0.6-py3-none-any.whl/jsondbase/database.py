import json, os

class LocalDatabase:
    def __init__(self, dbname="default.json"):
        """
        :dbname --> name of the json file, if not enter the default json file as `default.json`
        """

        self.dbname = dbname

        if not os.path.exists(self.dbname):
            open(self.dbname, "w+").write("[]")

    def openjson(self):
        return json.loads(open(self.dbname).read())

    def writejson(self, data):
        try:
            with open(self.dbname, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as E:
            return False, E

        return True, None
    
    def isRecordExist(self, value, *keys):
        """
        :value --> value to find the entire record\n
        :keys --> multiple keys\n
        example isRecordExist("abc@gmail.com", "person", "email") if json["person"]["email] == "abc@gmail.com" will be return True or False
        """
        result = self.openjson()

        try:
            for items in result:
                output = items
                for key in keys:
                    output = output[key]
                if output == value: return True, None
        except Exception as E:
            return False, E
        
        return False, "Unknown Error"

    def addRecord(self, record):
        try:
            data = self.openjson()
            data.append(record)
            self.writejson(data)
            return True, None
        except Exception as E:
            return False, E

    def deleteRecord(self, value, *keys):
        """
        :value --> value to delete the entire record\n
        :keys --> multiple keys\n
        example getRecord("abc@gmail.com", "person", "email") if json["person"]["email] == "abc@gmail.com" will be delete that record
        """
        result = self.openjson()

        try:
            for items in result:
                output = items
                for key in keys:
                    output = output[key]
                if output == value:
                    data = [record for record in result if record != items]
                    self.writejson(data)
                    return True, None
        except Exception as E:
            return None, E

        return None, "value not found"

    def getRecord(self, value, *keys):
        """
        :value --> value to find the entire record\n
        :keys --> multiple keys\n
        example isRecordExist("abc@gmail.com", "person", "email") if json["person"]["email] == "abc@gmail.com" will be return entire record
        """
        result = self.openjson()

        try:
            for items in result:
                output = items
                for key in keys:
                    output = output[key]
                if output == value: return items
        except:
            return None

        return None
