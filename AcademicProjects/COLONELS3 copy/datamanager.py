import torch
from torch.utils.data import DataLoader
from torch.utils.data.sampler import RandomSampler, SequentialSampler
from torch.utils.data import Dataset
import json
import os
import cv2
from skimage import transform
import warnings

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def retrieve_image(filename, W=64):
    """
    Loads an image, resizes it to WxW pixels, and then converts it into a
    Torch tensor of shape (3, W, W). The "3" dimension corresponds to 
    the blue, green, and red channels of the input image.

    """
    image = cv2.imread(filename)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        image = transform.resize(image, (W,W))
    image = torch.from_numpy(rgb2gray(image)).unsqueeze(0)
    #image = torch.from_numpy(image.transpose((2, 0, 1)))
    return image
 

class DataPartition(Dataset):

    def __init__(self, json_file, data_dir, partition, resize_width=64):  
        """
        Creates a DataPartition from a JSON configuration file.
        
        - json_file is the filename of the JSON config file.
        - data_dir is the directory where the images are stored.
        - partition is a string indicating which partition this object
                    represents, i.e. "train" or "test"
        - resize_width indicates the dimensions to which each image will
                    be resized (the images are resized to a square WxW
                    image)
        
        """
        with open(json_file) as f:
            data = json.load(f)
        self.data = [datum for datum in data 
                     if datum['partition'] == partition]
        self.root_dir = data_dir
        categories_ = set()
        for datum in self.data:
            categories_.add(datum['category'])
        self.categories_ = sorted(list(categories_))
        self.resize_width = resize_width

    def __len__(self):
        """
        Returns the number of data (datums) in this DataPartition.
        
        """
        return len(self.data)

    def __getitem__(self, i):
        """
        Converts the ith datum into the following dictionary and then
        returns it:
            
            {'image': retrieve_image(img_filename), 
             'category': datum['category'], 
             'filename': datum['filename'] }
        
        """      
        datum = self.data[i]
        img_filename = os.path.join(self.root_dir, datum['filename'])
        sample = {'image': retrieve_image(img_filename, self.resize_width), 
                  'category': datum['category'], 
                  'filename': datum['filename']}
        return sample
   
    def categories(self):
        """
        Returns an alphabetically sorted list of categories in this
        DataPartition. The categories are all distinct values
        associated with the key "category" in any datum.
        
        """
        return self.categories_
    
   
class DataManager:
    
    def __init__(self, train_partition, test_partition, 
                 evidence_key = 'image', response_key='category'):
        """
        Creates a DataManager from a JSON configuration file. The job
        of a DataManager is to manage the data needed to train and
        evaluate a neural network.
        
        - train_partition is the DataPartition for the training data.
        - test_partition is the DataPartition for the test data.
        - evidence_key is the key associated with the evidence in each
          datum of the data partitions, i.e. train_partition[i][evidence_key]
          should be the ith evidence tensor in the training partition.
        - response_key is the key associated with the response in each
          datum of the data partitions, i.e. train_partition[i][response_key]
          should be the ith response tensor in the training partition.
        
        """
        self.train_set = train_partition
        self.test_set = test_partition
        self.evidence_key = evidence_key
        self.response_key = response_key
        try:
            self.categories = sorted(list(set(train_partition.categories()) |
                                          set(test_partition.categories())))
        except AttributeError:
            pass
    
    def train(self, batch_size):
        """
        Returns a torch.DataLoader for the training examples. The returned
        DataLoader can be used as follows:
            
            for batch in data_loader:
                # do something with the batch
        
        - batch_size is the number of desired training examples per batch
        
        """
        train_loader = DataLoader(self.train_set, batch_size=batch_size,
                                  sampler=RandomSampler(self.train_set), 
                                  num_workers=2)
        return(train_loader)
    
    def test(self):
        """
        Returns a torch.DataLoader for the test examples. The returned
        DataLoader can be used as follows:
            
            for batch in data_loader:
                # do something with the batch
                
        """
        return DataLoader(self.test_set, batch_size=4, 
                          sampler=SequentialSampler(self.test_set), 
                          num_workers=2)

    
    def evidence_and_response(self, batch):
        """
        Converts a batch obtained from either the train or test DataLoader
        into an evidence tensor and a response tensor.
        
        The evidence tensor returned is just batch[self.evidence_key].
        
        To build the response tensor, one starts with batch[self.response_key],
        where each element is a "response value". Each of these response
        values is then mapped to the index of that response in the sorted set of
        all possible response values. The resulting tensor should be
        a LongTensor.

        The return value of this function is:
            evidence_tensor, response_tensor
        
        See the unit tests in test.py for example usages.
        
        """
        def category_index(category):
            return self.categories.index(category)
        inputs = batch[self.evidence_key].float()
        labels = torch.Tensor([category_index(c) for c 
                               in batch[self.response_key]]).long()
        return inputs, labels

    def evaluate(self, classifier, partition):
        """
        Given a classifier that maps an evidence tensor to a response
        tensor, this evaluates the classifier on the specified data
        partition ("train" or "test") by computing the percentage of
        correct responses.
        
        See the unit test ```test_evaluate``` in test.py for expected usage.
        
        """
        def loader(partition):
            if partition == 'train':
                return self.train(40)
            else:
                return self.test()
    
        def accuracy(outputs, labels):
            correct = 0
            total = 0
            for (output, label) in zip(outputs, labels):
                total += 1
                if label == output.argmax():
                    correct += 1
            return correct, total
        correct = 0
        total = 0       
        for data in loader(partition):
            inputs, labels = self.evidence_and_response(data)
            outputs = classifier(inputs) 
            correct_inc, total_inc = accuracy(outputs, labels)
            correct += correct_inc
            total += total_inc
        return correct / total

