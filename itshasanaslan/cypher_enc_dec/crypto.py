# Hasan Aslan 
# www.itshasanaslan.com
# itshasanaslan@gmail.com
from cryptography.fernet import Fernet


class CryptoHandler:
    def __init__(self, **kwargs):
        self.key = kwargs.get("key")
        self.fernet = None
        # very first object
        if self.key == None and kwargs.get("generate_new"): # generate_new = True
            self.key = Fernet.generate_key() #get new key.
            file_location = kwargs.get("key_location") # default = key.key
            if kwargs.get("save"):
                if file_location == None:
                    self.save_key() # to default location.

                else:
                    self.save_key(file_location)

        # import object
        elif self.key == None and kwargs.get("read_key"):
            file_location = kwargs.get("key_location")

            if file_location == None:
                self.get_key()

            else:
                self.get_key(file_location)
        
        # init fernet obj
        self.fernet = Fernet(self.key)
    
    # for future use
    def save_key(self, filename = "key.key"):
        if self.key == None:
            raise Exception("Key is null")

        file = open(filename, 'wb')
        file.write(self.key)
        file.close()

    def get_key(self, filename = "key.key"):
        file = open(filename, 'rb')
        self.key = file.read()
        file.close()
        return self.key

    def encrypt(self, message):
        if type(message) == type(b'a'): return self.fernet.encrypt(message)
        if type(message) == type(""):return self.fernet.encrypt(message.encode())
        return None

    def decrypt(self, message):
        return self.fernet.decrypt(message)
        #if type(message) == type(b'a'): return self.fernet.decrypt(message)
        #if type(message) == type(""): return self.fernet.decrypt(message.decode())
        #return None

    def save_data(self, data, file_location):
        operation = ""
        if type(data) == type(b'a'): operation = 'wb'
        elif type(data) == type(""): operation = 'w'
        
        with open(file_location, operation) as file:
            file.write(data)

    # just reads from file. Does not encrypt or decrypt.
    # Get the data with this and do the operation with other functions.
    def read_data(self, file_location):
        file = open(file_location, 'rb')
        data = file.read()
        file.close()
        return data

def test_this_script():
    # if you have a key saved...
    c = CryptoHandler(read_key = True, key_location = "new.key") 
    #c.save_data(c.encrypt("Hasan Aslan"), "saved.txt")
    print(c.decrypt(c.read_data("saved.txt")))




if __name__ == "__main__":
    test_this_script()