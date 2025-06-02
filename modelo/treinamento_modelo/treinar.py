"""
Treinamento CNN - Detecção de Pessoas em Inundações
Executa uma vez, salva o modelo, pronto.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
import os

# Configurações
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
IMAGE_SIZE = 64
BATCH_SIZE = 8
EPOCHS = 25
LR = 0.001

print(f"Dispositivo: {DEVICE}")

# Transformações
transform_train = transforms.Compose([
    transforms.Resize((72, 72)),
    transforms.RandomResizedCrop(IMAGE_SIZE, scale=(0.8, 1.0)),
    transforms.RandomHorizontalFlip(p=0.3),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.3, contrast=0.2),
    transforms.ToTensor(),
])

transform_test = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
])

# Dataset
train_dataset = ImageFolder('dataset/train', transform=transform_train)
test_dataset = ImageFolder('dataset/test', transform=transform_test)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

print(f"Treino: {len(train_dataset)} | Teste: {len(test_dataset)}")

# Modelo
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout2d(0.25)
        self.fc1 = nn.Linear(64 * 16 * 16, 128)
        self.fc2 = nn.Linear(128, 1)
        
    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.dropout(x)
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = self.dropout(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

model = CNN().to(DEVICE)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

# Treinamento
print("\nIniciando treinamento...")

for epoch in range(EPOCHS):
    # Treino
    model.train()
    train_loss = 0
    train_correct = 0
    train_total = 0
    
    for data, target in train_loader:
        data, target = data.to(DEVICE), target.float().to(DEVICE)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output.squeeze(), target)
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item()
        predicted = (output.squeeze() > 0.5).float()
        train_total += target.size(0)
        train_correct += (predicted == target).sum().item()
    
    # Teste
    model.eval()
    test_loss = 0
    test_correct = 0
    test_total = 0
    
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(DEVICE), target.float().to(DEVICE)
            output = model(data)
            loss = criterion(output.squeeze(), target)
            
            test_loss += loss.item()
            predicted = (output.squeeze() > 0.5).float()
            test_total += target.size(0)
            test_correct += (predicted == target).sum().item()
    
    train_acc = 100 * train_correct / train_total
    test_acc = 100 * test_correct / test_total
    
    print(f"Época {epoch+1}: Treino {train_acc:.1f}% | Teste {test_acc:.1f}%")

# Salvar modelo
os.makedirs('modelo', exist_ok=True)
torch.save({
    'model_state_dict': model.state_dict(),
    'image_size': IMAGE_SIZE,
    'accuracy': test_acc
}, 'modelo/detector.pth')

print(f"\nModelo salvo! Acurácia final: {test_acc:.1f}%")
