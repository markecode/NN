import numpy as np
from sklearn import preprocessing


def load_snp_returns():
    f = open('YESBANK.csv', 'rb').readlines()[1:]
    raw_data = []
    for line in f:
        try:
            open_price = float(line.decode("utf-8").split(',')[1])
            close_price = float(line.decode("utf-8").split(',')[4])
            high_price = float(line.decode("utf-8").split(',')[2])
            Low_price = float(line.decode("utf-8").split(',')[2])
            vol = float(line.decode("utf-8").split(',')[5])
            raw_data.append(close_price-open_price)
        except:
            continue

    return raw_data[::-1]



def split_into_chunks(data, train, predict, step):
    X= []
    Y = []
    for i in range(0, len(data), step):
        try:
            x_i = data[i+train+predict]
            
            series = np.array(data[i:i+train+predict]) 
            series = preprocessing.scale(series)
            
            x_i = series[:-1]
            y_i = series[-1]
           
        except Exception as err:
            print(err,i)
            break
        X.append(x_i)
        Y.append(y_i)

    return X, Y

def shuffle_in_unison(a, b):

    assert len(a) == len(b)
    shuffled_a = np.empty(a.shape, dtype=a.dtype)
    shuffled_b = np.empty(b.shape, dtype=b.dtype)
    permutation = np.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
    return shuffled_a, shuffled_b


def create_Xt_Yt(X, y,l):

    X_train = X[0:l]
    Y_train = y[0:l]
    
    X_test = X[l:]
    Y_test = y[l:]
    return X_train, X_test, Y_train, Y_test


def createnumpyarray(X,Y,trainsize):
    X_data = np.zeros((len(X),3))
    Y_data = np.zeros((len(Y),1))
    for i in range(len(X)):
        X_data[i]= X[i]
        Y_data[i]=Y[i]
    
    return  X_data , Y_data

def Normalize(data):
    norm = []
    max_val = max(data)
    min_val = min(data)
    for i in range(len(data)):
        newval = (data[i])/(max_val-min_val) 
        norm.append(newval)
    return norm