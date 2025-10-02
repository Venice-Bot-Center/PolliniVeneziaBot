import os

import pyrebase

API_KEY = os.environ["FBKEY"]
AUTHDOMAIN = os.environ["FBAUTH"]
DATABASEURL = os.environ["FBDATABASE"]
STORAGEBUCKET = os.environ["FBSTORAGE"]


class FirebaseDB:
    config = {
        "apiKey": API_KEY,
        "authDomain": AUTHDOMAIN,
        "databaseURL": DATABASEURL,
        "storageBucket": STORAGEBUCKET,
    }

    db = pyrebase.initialize_app(config).database()


class DBIstance:
    def __init__(self):
        self.firebase_istance = FirebaseDB().db

    @property
    def pollini_hash(self):
        return self.pollini_hash.get()

    @pollini_hash.getter
    def pollini_hash(self):
        return self.firebase_istance.child("pollini").child("hash").get().val()

    @pollini_hash.setter
    def pollini_hash(self, last):
        self.firebase_istance.child("pollini").update({"hash": str(last)})

    @property
    def pollini_mex(self):
        return self.pollini_mex.get()

    @pollini_mex.getter
    def pollini_mex(self):
        return self.firebase_istance.child("pollini").child("mex").get().val()

    @pollini_mex.setter
    def pollini_mex(self, last):
        self.firebase_istance.child("pollini").update({"mex": str(last)})
