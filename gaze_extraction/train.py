import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Load the data from a CSV file
data = pd.read_csv("your_data.csv")  # Replace "your_data.csv" with the path to your CSV file

# Assuming your CSV file contains two columns "feature1" and "feature2" and "output1" and "output2"
# Adjust these column names to match your actual dataset
features = data[["feature1", "feature2"]].values
outputs = data[["output1", "output2"]].values

# Split the data into a training set and a test set
X_train, X_test, Y_train, Y_test = train_test_split(features, outputs, test_size=0.2, random_state=42)

# Scale the data (optional but often recommended for neural networks)
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert data to PyTorch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
Y_train = torch.tensor(Y_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
Y_test = torch.tensor(Y_test, dtype=torch.float32)

# Define the neural network model
class ComplexNN(nn.Module):
    def __init__(self):
        super(ComplexNN, self).__init()
        self.fc1 = nn.Linear(2, 4)  # Two input features, four neurons in the hidden layer
        self.fc2 = nn.Linear(4, 2)  # Four neurons in the hidden layer, two output features
        self.activation = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.activation(x)
        x = self.fc2(x)
        x = torch.tanh(x)  # Using tanh activation for outputs to keep them between -1 and 1
        return x

# Create an instance of the more complex neural network
net = ComplexNN()

# Define a loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr=0.1)

# Training loop
for epoch in range(2000):
    optimizer.zero_grad()  # Zero the gradient buffers
    output = net(X_train)
    loss = criterion(output, Y_train)
    loss.backward()
    optimizer.step()

# Test the more complex neural network with new data
test_data = torch.tensor([[0.3, 0.8]], dtype=torch.float32)
predicted_output = net(test_data)

print("Predicted Output:", predicted_output)
