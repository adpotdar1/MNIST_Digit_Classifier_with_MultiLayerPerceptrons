import torch
import torch.nn as nn
from torch import optim
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as F
import matplotlib.pyplot as plt


transform = transforms.Compose(
    [
        transforms.ToTensor(),
        # Normalization is done to reduce values generated by multiplication of inputs and weights
        transforms.Normalize(mean=[0.5], std=[0.5])
    ]
)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

training_data = datasets.MNIST(root='data', train=True, download=True, transform= transform)
test_data = datasets.MNIST(root='data', train=False, download=True, transform= transform)

training_loader = DataLoader(training_data, batch_size=32, shuffle=True)
test_loader = DataLoader(test_data, batch_size=32, shuffle=False)

def printSizeOfFirstElement(loader, set_type):
    #create iterator
    input_iter = iter(loader)

    # get to next item
    batch = next(input_iter)

    # separate inputs and labels
    inputs, labels = batch

    print(f'Shape of image tensor in {set_type} dataset is {inputs[0].shape}')

def print_first_few_images(dataset):
    image, label = dataset[0]

    # Print the image
    plt.imshow(image, cmap='gray')
    plt.title(f'Label: {label}')


printSizeOfFirstElement(training_loader,'training')
printSizeOfFirstElement(test_loader, 'test')
print_first_few_images(training_data)
class MyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.activation2 = F.softmax
        self.layer1 = nn.Linear(in_features=784,out_features=500)
        self.layer2 = nn.Linear(in_features=500, out_features= 100)
        self.layer3 = nn.Linear(in_features=100,out_features=50)
        self.layer4 = nn.Linear(in_features=50, out_features=10)

    def forward(self, inputs):
        new_inputs = torch.flatten(inputs, 1)
        inputs = self.activation2(self.layer1(new_inputs))
        inputs = self.activation2(self.layer2(inputs))
        inputs = self.activation2(self.layer3(inputs))
        inputs = self.layer4(inputs)
        return inputs

max_epochs = 60;

net = MyNet()
net.to(device)

# Choose an optimizer
optimizer = optim.SGD(net.parameters(), lr=0.001)

# Choose a loss function
criterion = nn.CrossEntropyLoss()

# Establish a list for our history
train_loss_history = list()
val_loss_history = list()

for epoch in range(max_epochs):

    train_loss = 0.0
    train_correct = 0

    training_lost = []

    # set Net in training Mode
    net.train()
    for index, batch in enumerate(training_loader):
        data, labels = batch

        optimizer.zero_grad()

        outputs = net(data)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        _, preds = torch.max(outputs.data, 1)

        train_correct += (preds == labels).sum().item()
        train_loss += loss.item()


    print(f'Epoch {epoch + 1} training accuracy: {train_correct / len(training_loader):.2f}% training loss: {train_loss / len(training_loader):.5f}')
    train_loss_history.append(train_loss / len(training_loader))

# Now test using test data

val_loss = 0.0
val_correct = 0
net.eval()

for inputs, labels in test_loader:

    test_output = net(inputs)

    loss = criterion(test_output, labels)

    _, preds = torch.max(test_output.data, dim=1)

    val_correct += (preds == labels).sum().item()
    val_loss += loss.item()
print(
    f'Epoch is {epoch + 1}  with validation accuracy: {val_correct / len(test_loader):.2f}% validation loss: {val_loss / len(test_loader):.5f}')
val_loss_history.append(val_loss / len(test_loader))

torch.save()







