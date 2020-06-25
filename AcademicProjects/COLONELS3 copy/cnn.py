import torch
import torch.optim as optim
import json
from datamanager import retrieve_image, DataPartition, DataManager
from training import Dense, ReLU, nlog_softmax_loss, minibatch_training
import math
import numpy as np

# IMPORTANT: DO NOT IMPORT OR USE ANYTHING FROM torch.nn
# BESIDES THESE THINGS
from torch.nn import Parameter, Conv2d, MaxPool2d, Module, init, Sequential


def create_kernel_row_matrix(kernels):
    """
    Creates a kernel-row matrix (as described in the notes on
    "Computing Convolutions"). See the unit tests for example input
    and output.

    """

    a,b,c,d = kernels.shape
    return kernels.reshape(a,b*c*d)

    raise NotImplementedError("Question 8.")

def create_window_column_matrix(images, window_width, stride):
    """
    Creates a window-column matrix (as described in the notes on
    "Computing Convolutions"). See the unit tests for example input
    and output.

    """

    #Approach 2
    num_images, num_channels, height, width = images.shape
    windows = []
    ctr = 0
    outer = torch.tensor([])
    for i in range(0, height-window_width+1, stride):
        for j in range(0, width-window_width+1, stride):
            xs = images[:,:,i:i+window_width,j:j+window_width]
            xs = xs.reshape(num_images,window_width*window_width*num_channels)

            if ctr == 0:
                outer = xs
                ctr += 1
            else:
                outer = torch.cat([outer,xs])
                outer = outer.reshape(num_images*(ctr+1),window_width*window_width*num_channels)
                ctr += 1

    timothy = torch.tensor([])
    for i in range(num_images):
        xsg = outer[i::num_images,::]
        if i == 0:
            timothy = xsg
        else:
            timothy = torch.cat([timothy,xsg])
    return timothy.t()




    raise NotImplementedError("Question 9.")

def pad(images, padding):
    """
    Adds padding to a tensor of images.

    The tensor is assumed to have shape (B, C, W, W), where B is the batch
    size, C is the number of input channels, and W is the width of each
    (square) image.

    Padding is the number of zeroes we want to add as a border to each
    image in the tensor.

    """
    num_images, num_channels, height, width = images.shape

    a = torch.zeros(num_images,num_channels,height,padding) ##These 3 lines create the horizontal padding
    ee = torch.cat([images,a],dim=3)
    ff = torch.cat([a,ee],dim = 3)

    b = torch.zeros(num_images,num_channels,padding,width+2*padding) ##These 3 lines create the vertical padding
    hh = torch.cat([b,ff],dim=2)
    ii = torch.cat([hh,b],dim=2)

    return ii


def convolve(kernels, images, stride, padding):
    """
    Convolves a kernel tensor with an image tensor, as described in the
    notes on "Computing Convolutions." See the unit tests for example input
    and output.

    """
    kp = create_kernel_row_matrix(kernels)
    num_kernels,y = kp.shape

    num_images1, num_channels1, height1, width1 = kernels.shape
    num_images, num_channels, height, width = images.shape
    padup = pad(images,padding)

    img = create_window_column_matrix(padup, width1,stride)

    mp = torch.mm(kp,img)
    mp1,mp2 = mp.shape

    rp = width
    starting_index = 0

    ending_index = 2**width1
    rm = num_kernels

    outer = torch.tensor([])

    ctr1 = 0
    width = ((mp1*mp2)//num_images)//num_kernels
    width2 = int(math.sqrt(width))

    while ending_index<mp2+1:

        lm1 = mp[:,starting_index:ending_index]
        lm3 = lm1.reshape((2**width1)*num_kernels)

        if starting_index == 0:
            outer = lm3
        else:
            outer = torch.cat([outer,lm3])
        starting_index = starting_index+ 2**width1
        ending_index = ending_index + 2**width1

    xs = outer.reshape(num_images,num_kernels,width2,width2)
    return xs


    #raise NotImplementedError("Question 11.")



class ConvLayer(Module):
    """A convolutional layer for images."""

    def __init__(self, input_channels, num_kernels,
                 kernel_size, stride, padding):
        super(ConvLayer, self).__init__()
        self.stride = stride
        self.weight = Parameter(torch.empty(num_kernels, input_channels,
                                            kernel_size, kernel_size))
        self.offset = Parameter(torch.empty(num_kernels, 1, 1))
        self.padding = padding
        # randomly initializes the parameters
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        init.kaiming_uniform_(self.offset, a=math.sqrt(5))

    def forward(self, x):
        """This will only work after you've implemented convolve (above)."""
        return self.offset + convolve(self.weight, x,
                                      self.stride, self.padding)


class Flatten(Module):
    """
    Flattens a tensor into a matrix. The first dimension of the input
    tensor and the output tensor should agree.

    For instance, a 3x4x5x2 tensor would be flattened into a 3x40 matrix.

    See the unit tests for example input and output.

    """
    def __init__(self):
        super(Flatten,self).__init__()

    def forward(self,images):
        num_images, num_channels, height, width = images.shape
        flatten = images.reshape(num_images,num_channels*height*width)
        return flatten


        #raise NotImplementedError("Question 12.")



def create_cnn(num_kernels, kernel_size,
               output_classes, dense_hidden_size,
               image_width, is_grayscale=True,
               use_torch_conv_layer = True,
               use_maxpool=True):
    """
    Builds a CNN with two convolutional layers and two feedforward layers.

    Maxpool is added by default, but can be disabled.

    """
    if use_torch_conv_layer:
        Conv = Conv2d
    else:
        Conv = ConvLayer
    padding = kernel_size//2
    output_width = image_width
    if use_maxpool:
        output_width = output_width // 16
    model = Sequential()
    if is_grayscale:
        num_input_channels = 1
    else:
        num_input_channels = 3
    model.add_module("conv1", Conv(num_input_channels, num_kernels,
                                   kernel_size=kernel_size,
                                   stride=1, padding=padding))
    model.add_module("relu1", ReLU())
    if use_maxpool:
        model.add_module("pool1", MaxPool2d(kernel_size=4, stride=4, padding=0))
    model.add_module("conv2", Conv(num_kernels, num_kernels,
                                              kernel_size=kernel_size,
                                              stride=1, padding=padding))
    model.add_module("relu2", ReLU())
    if use_maxpool:
        model.add_module("pool2", MaxPool2d(kernel_size=4, stride=4, padding=0))
    model.add_module("flatten", Flatten())
    model.add_module("dense1", Dense(num_kernels * output_width**2,
                                     dense_hidden_size,
                                     init_bound = 0.1632993161855452))
    model.add_module("relu3", ReLU())
    model.add_module("dense2", Dense(dense_hidden_size, output_classes,
                                     init_bound = 0.2992528008322899))
    return model










class Classifier:
    """
    Allows the trained CNN to be saved to disk and loaded back in.

    You can call a Classifier instance as a function on an image filename
    to obtain a probability distribution over whether it is a zebra.

    """

    def __init__(self, net, num_kernels, kernel_size,
                 dense_hidden_size, categories, image_width):
        self.net = net
        self.num_kernels = num_kernels
        self.kernel_size = kernel_size
        self.dense_hidden_size = dense_hidden_size
        self.image_width = image_width
        self.categories = categories

    def __call__(self, img_filename):
        self.net.eval()
        image = retrieve_image(img_filename, self.image_width)
        inputs = image.float().unsqueeze(dim=0)
        outputs = torch.softmax(self.net(inputs), dim=1)
        result = dict()
        for i, category in enumerate(self.categories):
            result[category] = outputs[0][i].item()
        return result

    def save(self, filename):
        model_file = filename + '.model'
        with torch.no_grad():
            torch.save(self.net.state_dict(), model_file)
        config = {'dense_hidden_size': self.dense_hidden_size,
                  'num_kernels': self.num_kernels,
                  'kernel_size': self.kernel_size,
                  'image_width': self.image_width,
                  'categories': self.categories,
                  'model_file': model_file}
        with open(filename + '.json', 'w') as outfile:
            json.dump(config, outfile)

    @staticmethod
    def load(config_file):
        with open(config_file) as f:
            data = json.load(f)
        net = create_cnn(data['num_kernels'],
                         data['kernel_size'],
                         len(data['categories']),
                         data['dense_hidden_size'],
                         data['image_width'])
        net.load_state_dict(torch.load(data['model_file']))
        return Classifier(net,
                          data['num_kernels'],
                          data['kernel_size'],
                          data['dense_hidden_size'],
                          data['categories'],
                          data['image_width'])





def run(data_config, n_epochs, num_kernels,
        kernel_size, dense_hidden_size,
        use_maxpool, use_torch_conv_layer):
    """
    Runs a training regime for a CNN.

    """
    train_set = DataPartition(data_config, './data', 'train')
    test_set = DataPartition(data_config, './data', 'test')
    manager = DataManager(train_set, test_set)
    loss = nlog_softmax_loss
    learning_rate = .001
    image_width = 64
    net = create_cnn(num_kernels = num_kernels, kernel_size= kernel_size,
                                 output_classes=2, image_width=image_width,
                                 dense_hidden_size=dense_hidden_size,
                                 use_maxpool = use_maxpool,
                                 use_torch_conv_layer = use_torch_conv_layer)
    optimizer = optim.Adam(net.parameters(), lr=learning_rate)
    best_net, monitor = minibatch_training(net, manager,
                                           batch_size=32, n_epochs=n_epochs,
                                           optimizer=optimizer, loss=loss)
    classifier = Classifier(best_net, num_kernels, kernel_size,
                            dense_hidden_size, manager.categories, image_width)
    return classifier, monitor





def experiment1():
    return run('stripes.data.json',
               n_epochs = 20,
               num_kernels = 20,
               kernel_size = 3,
               dense_hidden_size = 64,
               use_maxpool = True,
               use_torch_conv_layer = False)

def experiment2():
    return run('stripes.data.json',
               n_epochs = 20,
               num_kernels = 20,
               kernel_size = 3,
               dense_hidden_size = 64,
               use_maxpool = True,
               use_torch_conv_layer = True)

def experiment3():
    return run('stripes.data.json',
               n_epochs = 20,
               num_kernels = 20,
               kernel_size= 3,
               dense_hidden_size=64,
               use_maxpool=False,
               use_torch_conv_layer = True)


def experiment4():
    return run('zebra.data.json',
               n_epochs = 8,
               num_kernels = 20,
               kernel_size= 7,
               dense_hidden_size=64,
               use_maxpool=True,
               use_torch_conv_layer = True)
