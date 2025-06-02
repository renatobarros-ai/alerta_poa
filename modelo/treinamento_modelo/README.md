# CNN Detecção de Pessoas em Inundações

Sistema de detecção automática de pessoas em cenários de inundação utilizando Redes Neurais Convolucionais (CNN) com PyTorch.

## 📁 Estrutura do Projeto

```
modelo/
├── dataset/
│   ├── train/
│   │   ├── com_pessoas/     # 160 imagens
│   │   └── sem_pessoas/     # 160 imagens
│   └── test/
│       ├── com_pessoas/     # 40 imagens
│       └── sem_pessoas/     # 40 imagens
├── treinar.py              # Script de treinamento
├── requirements.txt        # Dependências
├── README.md              # Este arquivo
└── modelo/
    └── detector.pth       # Modelo treinado (gerado)
```

## 🚀 Instalação

```bash
pip install -r requirements.txt
```

## 📊 Preparação do Dataset

1. Colete **400 imagens** de inundações:
   - 200 **com pessoas** visíveis
   - 200 **sem pessoas**

2. Organize nas pastas:
   - `dataset/train/com_pessoas/` (160 imagens)
   - `dataset/train/sem_pessoas/` (160 imagens) 
   - `dataset/test/com_pessoas/` (40 imagens)
   - `dataset/test/sem_pessoas/` (40 imagens)

## 🔥 Treinamento

```bash
python treinar.py
```

**Resultado esperado:**
- Acurácia: 78-85%
- Tempo: ~10-25 minutos (GTX 1650)
- Modelo salvo em: `modelo/detector.pth`

## 🎯 Uso do Modelo

```python
# Copie o detector.pth para seu sistema e use:
from detector import detectar_pessoas_em_risco

resultado = detectar_pessoas_em_risco("imagem.jpg")
# Retorna: "PRESENÇA CONFIRMADA" ou "AUSENTE"
```

## ⚙️ Requisitos Técnicos

- **Python:** 3.8+
- **GPU:** CUDA compatível (recomendado)
- **RAM:** 8GB+
- **Dataset:** 400 imagens balanceadas

## 📋 Especificações

- **Arquitetura:** CNN customizada (2 blocos conv + 2 camadas densas)
- **Input:** Imagens 64x64 RGB
- **Output:** Classificação binária
- **Treinamento:** 25 épocas, Adam optimizer, BCELoss
- **Data Augmentation:** Flip, rotação, zoom, color jitter

## 🎓 Projeto Acadêmico

Este é um projeto acadêmico focado na implementação de CNN para detecção de pessoas em emergências urbanas. O objetivo é demonstrar conceitos de deep learning aplicados a sistemas de monitoramento inteligente.
