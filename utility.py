import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_estimated_price(Location,Area,New_or_Resale,Gymnasium,Lift_Available,Car_Parking,Clubhouse,Gas_Connection,Jogging_Track,Swimming_Pool,bhk):
    try:
        loc_index = __data_columns.index(Location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = Area
    x[1] = New_or_Resale
    x[2] = Gymnasium
    x[3] = Lift_Available
    x[4] = Car_Parking
    x[5] = Clubhouse
    x[6] = Gas_Connection
    x[7] = Jogging_Track
    x[8] = Swimming_Pool
    x[9] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations

    with open("Model/locations.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[10:]  # first 9 columns are stuff

    global __model
    if __model is None:
        with open('Model/realestate_price_model_mumbai.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

# if __name__ == '__main__':
#     load_saved_artifacts()
#     print(get_location_names())
#     print(get_estimated_price('Vashi',10000,0,1,0,1,1,0,1,1,2))
