import time
import matplotlib.pyplot as plt
import sys

class TrainingMonitor:
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def start(self, n_batches):
        print("=== STARTING TRAINING ===")
        self.training_start_time = time.time()
        self.n_batches = n_batches
        self.print_every = n_batches // 10   
        self.train_profile = []

    def start_epoch(self, epoch):
        sys.stdout.write("Epoch {}".format(epoch))
        self.running_loss = 0.0
        self.start_time = time.time()
        self.total_train_loss = 0

    def report_batch_loss(self, epoch, batch, loss):
        self.total_train_loss += loss
        if self.verbose:
            self.running_loss += loss
            if (batch + 1) % (self.print_every + 1) == 0:               
                print("Epoch {}, {:d}% \t train_loss: {:.2f} took: {:.2f}s".format(
                        epoch+1, int(100 * (batch+1) / self.n_batches), 
                        self.running_loss / self.print_every, time.time() - self.start_time))
                self.running_loss = 0.0
                self.start_time = time.time()                    
            
    def report_accuracies(self, epoch, train_acc, dev_acc):
        self.train_profile.append((train_acc, dev_acc))
        epoch_time = time.time() - self.start_time
        if train_acc is not None:
            print("Train accuracy = {:.2f}".format(train_acc))
        if dev_acc is not None:
            print("[{:.2f}sec] train loss = {:.2f}; test accuracy = {:.2f} ".format(
                    epoch_time, self.total_train_loss, dev_acc))

    def training_profile_graph(self):
        return [[x[0] for x in self.train_profile], 
                [x[1] for x in self.train_profile]]

    def stop(self):
        print("Training finished, took {:.2f}s".format(
                time.time() - self.training_start_time))

    @staticmethod
    def plot_average_and_max(monitors, description=""):
        valuelists = [monitor.training_profile_graph()[1] for monitor in monitors]
        values = [sum([valuelist[i] for valuelist in valuelists])/len(valuelists) for 
                  i in range(len(valuelists[0]))]
        overall = list(zip(range(len(values)), values))
        x = [el[0] for el in overall]
        y = [el[1] for el in overall]
        plt.plot(x,y, label='average' + description)
        values = [max([valuelist[i] for valuelist in valuelists]) for 
                  i in range(len(valuelists[0]))]
        overall = list(zip(range(len(values)), values))
        x = [el[0] for el in overall]
        y = [el[1] for el in overall]
        plt.plot(x,y, label='max' + description)
        plt.xlabel('epoch')
        plt.ylabel('test accuracy')
        plt.legend()

    @staticmethod
    def plot_average(monitors, description=""):
        valuelists = [monitor.training_profile_graph()[1] for monitor in monitors]
        values = [sum([valuelist[i] for valuelist in valuelists])/len(valuelists) for 
                  i in range(len(valuelists[0]))]
        overall = list(zip(range(len(values)), values))
        x = [el[0] for el in overall]
        y = [el[1] for el in overall]
        plt.plot(x,y, label='average' + description)
        plt.xlabel('epoch')
        plt.ylabel('test accuracy')
        plt.legend()

