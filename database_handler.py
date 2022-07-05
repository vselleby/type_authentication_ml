import pickle
import numpy as np
# from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
import os.path
from globals import NUMBER_SAMPLES


class DbSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DbSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseHandler(metaclass=DbSingleton):

    def __init__(self):
        self.features = []
        self.previous_feature_length = 0
        # self.model = EllipticEnvelope()
        self.model = IsolationForest()
        self.username = ""
        self.file_path = "models/"

    def authenticate(self, pressed, released):
        model = pickle.load(open(self.file_path + self.username + ".sav", 'rb'))
        temp_features = pressed + released
        temp_features = np.array(temp_features)
        temp_features = [temp_features]
        try:
            authenticated = model.predict(temp_features)[0] == 1
        except ValueError:
            authenticated = False

        if authenticated:
            print("-------------Authenticated---------------")
        else:
            print("------------Not Authenticated------------")
        return True

    def register(self, pressed, released):
        temp_features = pressed + released
        if len(temp_features) == 0:
            print("You have to enter a password\n")
            return False
        elif self.previous_feature_length == 0:
            self.features.insert(len(self.features), temp_features)
        else:
            if self.previous_feature_length != len(temp_features):
                print("Password has different length\n")
                return False
            else:
                self.features.insert(len(self.features), temp_features)
        self.previous_feature_length = len(temp_features)
        if len(self.features) == NUMBER_SAMPLES:
            self.train_model()
        return True

    def check_available(self, username):
        self.previous_feature_length = 0
        self.username = username
        if os.path.exists(self.file_path + username + ".sav"):
            # print("Username not available\n")
            return False
        return True

    def train_model(self):
        np_features = np.array(self.features)
        self.model.fit(np_features)
        pickle.dump(self.model, open(self.file_path + self.username + ".sav", 'wb'))
        print("User created, you can now try authenticating\n")
