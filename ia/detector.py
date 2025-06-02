import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import time
import os
from django.conf import settings

class PeopleDetector:
    def __init__(self):
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.load_model()
    
    def load_model(self):
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'detector.pth')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")
        
        try:
            # Carrega o modelo PyTorch
            self.model = torch.load(model_path, map_location=self.device)
            self.model.eval()
            print(f"Modelo CNN carregado com sucesso em: {self.device}")
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            # Fallback: cria um modelo simples se não conseguir carregar
            self._create_fallback_model()
    
    def _create_fallback_model(self):
        """Cria um modelo simples para demonstração se o original não carregar"""
        class SimpleCNN(nn.Module):
            def __init__(self):
                super(SimpleCNN, self).__init__()
                self.features = nn.Sequential(
                    nn.Conv2d(3, 64, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(kernel_size=2, stride=2),
                    nn.Conv2d(64, 128, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(kernel_size=2, stride=2),
                )
                self.classifier = nn.Sequential(
                    nn.AdaptiveAvgPool2d((7, 7)),
                    nn.Flatten(),
                    nn.Linear(128 * 7 * 7, 512),
                    nn.ReLU(inplace=True),
                    nn.Dropout(0.5),
                    nn.Linear(512, 2)  # 2 classes: com pessoas / sem pessoas
                )
            
            def forward(self, x):
                x = self.features(x)
                x = self.classifier(x)
                return x
        
        self.model = SimpleCNN().to(self.device)
        print("Usando modelo CNN de fallback para demonstração")
    
    def detect_people(self, image_path=None, image_tensor=None):
        """
        Detecta pessoas em uma imagem
        
        Args:
            image_path: Caminho para a imagem
            image_tensor: Tensor da imagem já processado
        
        Returns:
            dict: {
                'pessoas_detectadas': bool,
                'confianca': float,
                'tempo_processamento': float
            }
        """
        start_time = time.time()
        
        try:
            if image_path:
                # Carrega imagem do arquivo
                image = Image.open(image_path).convert('RGB')
                input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            elif image_tensor is not None:
                input_tensor = image_tensor.to(self.device)
            else:
                # Simula uma imagem para demonstração
                input_tensor = torch.randn(1, 3, 224, 224).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(input_tensor)
                
                # Aplica softmax para obter probabilidades
                probabilities = torch.softmax(outputs, dim=1)
                
                # Confiança para presença de pessoas (classe 1)
                confidence = probabilities[0][1].item()
                
                # Considera detectado se confiança > 0.7 (70%)
                pessoas_detectadas = confidence > 0.7
            
            processing_time = time.time() - start_time
            
            return {
                'pessoas_detectadas': pessoas_detectadas,
                'confianca': confidence,
                'tempo_processamento': processing_time
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"Erro na detecção: {e}")
            
            # Retorna resultado padrão em caso de erro
            return {
                'pessoas_detectadas': False,
                'confianca': 0.0,
                'tempo_processamento': processing_time
            }
    
    def simulate_detection(self, force_detection=False):
        """
        Simula detecção de pessoas para demonstração
        
        Args:
            force_detection: Se True, força detecção de pessoas
        
        Returns:
            dict: Resultado da simulação
        """
        start_time = time.time()
        
        if force_detection:
            # Simula detecção positiva
            confidence = 0.85 + (torch.rand(1).item() * 0.1)  # 85-95%
            pessoas_detectadas = True
        else:
            # Simulação aleatória mais realista
            confidence = torch.rand(1).item()
            pessoas_detectadas = confidence > 0.7
        
        processing_time = time.time() - start_time + 0.1  # Simula tempo de processamento
        
        return {
            'pessoas_detectadas': pessoas_detectadas,
            'confianca': confidence,
            'tempo_processamento': processing_time
        }

# Instância global do detector
detector = None

def get_detector():
    """Retorna a instância global do detector (singleton)"""
    global detector
    if detector is None:
        detector = PeopleDetector()
    return detector

def detect_people_in_region(region_id, simulate=True):
    """
    Detecta pessoas em uma região específica
    
    Args:
        region_id: ID da região
        simulate: Se True, usa simulação; se False, tenta usar imagem real
    
    Returns:
        dict: Resultado da detecção
    """
    detector_instance = get_detector()
    
    if simulate:
        # Para simulação, força detecção ocasionalmente para demonstrar alertas
        force_detection = torch.rand(1).item() > 0.8  # 20% chance de detectar
        return detector_instance.simulate_detection(force_detection=force_detection)
    else:
        # Aqui você poderia carregar uma imagem específica da região
        # Por exemplo: image_path = f"/caminho/cameras/regiao_{region_id}.jpg"
        return detector_instance.detect_people()