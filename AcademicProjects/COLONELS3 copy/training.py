import torch
from torch.nn import Parameter
import torch.optim as optim
from copy import deepcopy
from torch.nn import init
from monitor import TrainingMonitor

LEARNING_RATE=0.001


def minibatch_training(net, manager, batch_size,
                       n_epochs, optimizer, loss):
    """
    Trains a neural network using the training partition of the
    provided DataManager.

    Arguments
    - net: the Module you want to train.
    - manager: the DataManager
    - batch_size: the desired size of each minibatch
    - n_epochs: the desired number of epochs for minibatch training
    - optimizer: the desired optimization algorithm to use (should be an
                 instance of torch.optim.Optimizer)
    - loss: the loss function to optimize

    """
    monitor = TrainingMonitor()
    train_loader = manager.train(batch_size)
    best_accuracy = float('-inf')
    best_net = None
    monitor.start(len(train_loader))
    for epoch in range(n_epochs):
        monitor.start_epoch(epoch)
        net.train() # puts the module in "training mode", e.g. ensures
                    # requires_grad is on for the parameters
        for i, data in enumerate(train_loader, 0):
            evidence, response = manager.evidence_and_response(data)
            optimizer.zero_grad()
            output = net(evidence)
            batch_loss = loss(output, response)
            batch_loss.backward()
            optimizer.step()
            monitor.report_batch_loss(epoch, i, batch_loss.data.item())
        net.eval() # puts the module in "evaluation mode", e.g. ensures
                   # requires_grad is off for the parameters
        dev_accuracy = manager.evaluate(net, "test")
        monitor.report_accuracies(epoch, None, dev_accuracy)
        if dev_accuracy >= best_accuracy:
            best_net = deepcopy(net)
            best_accuracy = dev_accuracy
    monitor.stop()
    return best_net, monitor



class Dense(torch.nn.Module):

    def __init__(self, input_size, output_size, init_bound=0.2):
        """
        A Module that multiplies an evidence matrix (with input_size
        evidence vectors) with a weight vector to produce output_size
        output vectors per evidence vector. See the unit tests in test.py
        for specific examples.

        - Rather than initializing every weight to 1, it initializes
          the weights uniformly at random from the range
          (-init_bound, init_bound).
        - An offset variable is added to each evidence vector. e.g. Suppose
          the evidence tensor (a batch of evidence vectors) is
          [[6.2, 127.0], [5.4, 129.0]]. The forward method will first
          prepend offset variables to each evidence vector, i.e. it
          becomes [[1.0, 6.2, 127.0], [1.0, 5.4, 129.0]]. Then, it takes the
          dot product of the weight vector with each of the new evidence
          vectors.

        """
        super(Dense, self).__init__()
        self.weight = Parameter(torch.empty(output_size, 1+input_size))
        init.uniform_(self.weight, -init_bound, init_bound)

    def unit_weights(self):
        """Resets all weights to 1. For testing purposes."""
        init.ones_(self.weight)

    def forward(self, x):
        """
        Computes the linear combination of the weight vector with
        each of the evidence vectors in the evidence matrix x.

        Note that this function will add an offset variable to each
        evidence vector. e.g. Suppose the evidence matrix (a batch of
        evidence vectors) is [[6.2, 127.0], [5.4, 129.0]]. The forward
        method will first prepend offset variables to each evidence vector,
        i.e. the evidence matrix becomes
        [[1.0, 6.2, 127.0], [1.0, 5.4, 129.0]]. Then, it takes the dot
        product of the weight vector with each of the new evidence vectors.

        """
        x2 = torch.cat([torch.ones(x.shape[0],1),x], dim=1)
        return torch.matmul(self.weight,x2.t()).t()
    


def one_layer_feedforward():
    """
    Just your standard run-of-the-mill logistic regression model with two
    input features and two response values.

    """
    net = torch.nn.Sequential()
    net.add_module("dense1", Dense(input_size = 2,
                                   output_size = 2,
                                   init_bound = 0.2))
    return net



class ReLU(torch.nn.Module):
    """
    Implements a rectified linear unit. The ```.forward``` method takes
    a torch.Tensor as its argument, and returns a torch.Tensor of the
    same shape, where all negative entries are replaced by 0.
    For instance:

        t = torch.tensor([[-3., 0., 3.2],
                          [2., -3.5, 1.]])
        relu = ReLU()
        relu.forward(t)

    should return the tensor:

        torch.tensor([[0., 0., 3.2],
                      [2., 0., 1.]])

    """
    def __init__(self):
        super(ReLU, self).__init__()

    def forward(self, x):
        return torch.clamp(x, min=0)


def two_layer_feedforward(H):
    """
    A two-layer feedforward neural network with two input features, H hidden
    features, and two response values.

    init_bound is set to 0.2 for all dense layers.

    """
    model = torch.nn.Sequential()
    model.add_module("dense1", Dense(2, H, init_bound = 0.2))
    model.add_module("relu", ReLU())
    model.add_module("dense2", Dense(H, 2, init_bound = 0.2))
    return model





def nlog_softmax_loss(X, y):
    """
    A loss function based on softmax, described in colonels2.ipynb.
    X is the (batch) output of the neural network, while y is a response
    vector.

    See the unit tests in test.py for expected functionality.

    """
    def log_softmax(X):
        exponentiated = torch.exp(X)
        normalizer = torch.sum(exponentiated, dim=1).unsqueeze(dim=1)
        return -torch.log(exponentiated / normalizer)
    softmax = log_softmax(X)
    result = torch.stack([softmax[i][y[i].item()] for i in range(len(y))])
    return torch.mean(result)




def run_disease_training(manager, net):
    """
    Trains a neural network on the data in the provided DataManager.

    Parameters like batch size and the number of epochs are hardcoded
    for the Disease dataset, so an example call to this function should
    look something like:

        run_disease_training(make_disease_data(num_train=5000, num_test=500),
                             one_layer_feedforward())

    """
    loss = nlog_softmax_loss
    learning_rate = .001
    optimizer = optim.Adam(net.parameters(), lr=learning_rate)
    best_net, monitor = minibatch_training(net, manager,
                                           batch_size=64, n_epochs=50,
                                           optimizer=optimizer, loss=loss)
    return best_net, monitor


def trials(n, trainer):
    """
    Runs n trials of a particular training function. Example use:

        trainer = lambda: run_disease_training(underweight_mgr,
                                               one_layer_feedforward())
        monitors = trials(5, trainer)

    Returns a list of the monitors created during each trial.

    """
    monitors = []
    for i in range(n):
        print("*** RUNNING TRIAL {} ***".format(i))
        classifier, monitor = trainer()
        monitors.append(monitor)
    return monitors
