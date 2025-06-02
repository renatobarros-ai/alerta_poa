"""
Detector de Pessoas em Inundações
Carrega modelo treinado e faz detecção.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import os

# Modelo (igual ao treino)
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

# Carregar modelo
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
checkpoint = torch.load('modelo/detector.pth', map_location=DEVICE)

model = CNN().to(DEVICE)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Transformação
transform = transforms.Compose([
    transforms.Resize((checkpoint['image_size'], checkpoint['image_size'])),
    transforms.ToTensor(),
])

print(f"Modelo carregado - Acurácia: {checkpoint['accuracy']:.1f}%")

def detectar_pessoas_em_risco(caminho_imagem):
    """
    Detecta pessoas em inundação
    
    Args:
        caminho_imagem (str): Caminho da imagem
        
    Returns:
        str: "PRESENÇA CONFIRMADA" ou "AUSENTE"
    """
    try:
        # Verificar arquivo
        if not os.path.exists(caminho_imagem):
            return "PRESENÇA CONFIRMADA"  # Segurança
        
        # Carregar imagem
        imagem = Image.open(caminho_imagem).convert('RGB')
        imagem_tensor = transform(imagem).unsqueeze(0).to(DEVICE)
        
        # Predição
        with torch.no_grad():
            output = model(imagem_tensor)
            confianca = output.item()
        
        # Classificar
        if confianca > 0.5:
            return "PRESENÇA CONFIRMADA"
        else:
            return "AUSENTE"
            
    except Exception:
        return "PRESENÇA CONFIRMADA"  # Segurança em caso de erro

# Teste rápido
if __name__ == "__main__":
    # Testar com uma imagem se existir
    test_img = "dataset/test/com_pessoas"
    if os.path.exists(test_img):
        primeira_img = os.path.join(test_img, os.listdir(test_img)[0])
        resultado = detectar_pessoas_em_risco(primeira_img)
        print(f"Teste: {resultado}")
