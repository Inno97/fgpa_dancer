# import the data from csv
import numpy as np
import pandas as pd
import os
import torch
from torch.utils.data import TensorDataset, DataLoader

class Dataset():
    def __init__(self):
        self.df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/dataset/dataset_3classes_2_16.csv')
        self.train_loader, self.test_loader = load_datasets(self.df)
        
    # get the next input from the either DataLoader (datasets are random)    
    def get_next_train_data(self):
        test_input, test_output = next(iter(self.train_loader))
        #test_output = test_output[0]

        #print("input: {}, output: {}".format(test_input[0], test_output))
        return test_input, test_output
        
    def get_next_train_data(self):
        test_input, test_output = next(iter(self.test_loader))
        #test_output = test_output[0]

        #print("input: {}, output: {}".format(test_input[0], test_output))
        return test_input, test_output

    def get_train_loader(self):
        return self.train_loader

    def get_test_loader(self):
        return self.test_loader    
    
# helper functions
def parse_input(df, starting_index):
    data = np.array(((df.iloc[starting_index, 0],df.iloc[starting_index + 1,0],df.iloc[starting_index + 2,0],df.iloc[starting_index + 3,0],df.iloc[starting_index + 4,0],df.iloc[starting_index + 5,0],df.iloc[starting_index + 6,0],df.iloc[starting_index + 7,0],
                  df.iloc[starting_index + 8, 0], df.iloc[starting_index + 9, 0], df.iloc[starting_index + 10, 0], df.iloc[starting_index + 11, 0], df.iloc[starting_index + 12, 0], df.iloc[starting_index + 13, 0], df.iloc[starting_index + 14, 0], df.iloc[starting_index + 15, 0]),
                 (df.iloc[starting_index, 1],df.iloc[starting_index + 1, 1],df.iloc[starting_index + 2, 1],df.iloc[starting_index + 3, 1],df.iloc[starting_index + 4, 1],df.iloc[starting_index + 5, 1],df.iloc[starting_index + 6, 1],df.iloc[starting_index + 7, 1], 
                  df.iloc[starting_index + 8, 1], df.iloc[starting_index + 9, 1], df.iloc[starting_index + 10, 1], df.iloc[starting_index + 11, 1], df.iloc[starting_index + 12, 1], df.iloc[starting_index + 13, 1], df.iloc[starting_index + 14, 1], df.iloc[starting_index + 15, 1])))
    return data

def load_datasets(df):
    print("loading dataset")
    # 20% set aside for testing
    num_items = (df.shape[0]) // 8
    max_data = 900
    batch_size = 2

    x_train_list = []
    y_train_list = []
    x_test_list = []
    y_test_list = []

    for i in range(num_items):
        if i == max_data:
            break
        starting_index = i * 8 * (num_items // max_data)
        
        # 16 inputs
        data = parse_input(df, starting_index)
        
        # do encoding, go by index as shown below
        if 'shrug' in df.iloc[starting_index, 2]:
            value = (0)
        elif 'zigzag' in df.iloc[starting_index, 2]:
            value = (1)
        elif 'windows' in df.iloc[starting_index, 2]:
            value = (2)
        else:
            continue
        
        if i % 5 != 4: # training
            x_train_list.append(data)
            y_train_list.append(value) 
        else: # testing
            x_test_list.append(data)
            y_test_list.append(value)
            
    # remove extra inputs that cannot fit in batch_size
    while len(x_train_list) % batch_size != 0:
        x_train_list.pop()
        y_train_list.pop()
        
    while len(x_test_list) % batch_size != 0:
        x_test_list.pop()
        y_test_list.pop()
    
    print("parsed data, loading into DataLoaders for training and testing")
    
    # transform to PyTorch DataLoader
    tensor_x_train = torch.Tensor(x_train_list) # transform to torch tensor
    tensor_y_train = torch.Tensor(y_train_list)
        
    print("loaded training data into DataLoader:", tensor_x_train.size())

    dataset_train = TensorDataset(tensor_x_train,tensor_y_train)
    train_loader = DataLoader(dataset_train, batch_size = batch_size, shuffle = True, num_workers = 1)

    tensor_x_test = torch.Tensor(x_test_list) # transform to torch tensor
    tensor_y_test = torch.Tensor(y_test_list)
        
    print("loaded training data into DataLoader:", tensor_x_test.size())

    dataset_test = TensorDataset(tensor_x_test,tensor_y_test)
    test_loader = DataLoader(dataset_test, batch_size = batch_size, shuffle = True, num_workers = 1)
    
    return train_loader, test_loader
