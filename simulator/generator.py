import random
from datetime import datetime
from django.utils import timezone
from core.models import Regiao, Medicao, NivelAgua, VolumeChuva, RiscoHumano, Status
from ia.detector import detect_people_in_region
import logging

logger = logging.getLogger(__name__)

class DataSimulator:
    """Simulador de dados de sensores para todas as regiões de Porto Alegre"""
    
    def __init__(self):
        self.niveis_agua = {1: 'Normal', 2: 'Alerta', 3: 'Crítico'}
        self.volumes_chuva = {1: 'Baixa', 2: 'Moderada', 3: 'Intensa'}
        
    def simulate_region_data(self, regiao_id):
        """
        Simula dados de uma região específica
        
        Args:
            regiao_id: ID da região
            
        Returns:
            dict: Dados simulados da região
        """
        # Simulação realística com tendências
        nivel_agua = self._generate_water_level()
        volume_chuva = self._generate_rain_volume()
        
        # Determina se deve avaliar risco (nível água ou chuva >= 2)
        avaliar_risco = nivel_agua >= 2 or volume_chuva >= 2
        
        return {
            'regiao_id': regiao_id,
            'nivel_agua': nivel_agua,
            'volume_chuva': volume_chuva,
            'avaliar_risco': avaliar_risco,
            'timestamp': timezone.now()
        }
    
    def _generate_water_level(self):
        """Gera nível de água com distribuição realística"""
        # 70% Normal, 25% Alerta, 5% Crítico
        rand = random.random()
        if rand < 0.70:
            return 1  # Normal
        elif rand < 0.95:
            return 2  # Alerta
        else:
            return 3  # Crítico
    
    def _generate_rain_volume(self):
        """Gera volume de chuva com distribuição realística"""
        # 60% Baixa, 30% Moderada, 10% Intensa
        rand = random.random()
        if rand < 0.60:
            return 1  # Baixa
        elif rand < 0.90:
            return 2  # Moderada
        else:
            return 3  # Intensa
    
    def simulate_all_regions(self):
        """
        Simula dados para todas as regiões cadastradas
        
        Returns:
            list: Lista com dados simulados de todas as regiões
        """
        results = []
        regioes = Regiao.objects.all()
        
        for regiao in regioes:
            data = self.simulate_region_data(regiao.id)
            results.append(data)
            
        return results
    
    def save_simulation_to_db(self):
        """
        Gera e salva dados simulados no banco de dados
        
        Returns:
            dict: Resumo da simulação
        """
        results = {
            'medicoes_criadas': 0,
            'riscos_avaliados': 0,
            'alertas_gerados': 0,
            'timestamp': timezone.now()
        }
        
        try:
            regioes = Regiao.objects.all()
            
            for regiao in regioes:
                # Gera dados simulados
                data = self.simulate_region_data(regiao.id)
                
                # Busca ou cria instâncias de NivelAgua e VolumeChuva
                nivel_agua = NivelAgua.objects.get(nivel=data['nivel_agua'])
                volume_chuva = VolumeChuva.objects.get(nivel=data['volume_chuva'])
                
                # Cria medição
                medicao = Medicao.objects.create(
                    regiao=regiao,
                    nivel_agua=nivel_agua,
                    volume_chuva=volume_chuva,
                    avaliar_risco=data['avaliar_risco']
                )
                results['medicoes_criadas'] += 1
                
                # Se deve avaliar risco, executa CNN
                if data['avaliar_risco']:
                    risco_result = self._process_risk_analysis(medicao)
                    results['riscos_avaliados'] += 1
                    
                    # Se detectou risco crítico, pode gerar alertas
                    if risco_result['alerta_critico']:
                        results['alertas_gerados'] += 1
                        
        except Exception as e:
            logger.error(f"Erro na simulação: {e}")
            results['erro'] = str(e)
            
        return results
    
    def _process_risk_analysis(self, medicao):
        """
        Processa análise de risco usando CNN
        
        Args:
            medicao: Instância de Medicao
            
        Returns:
            dict: Resultado da análise
        """
        # Executa detecção de pessoas via CNN
        detection_result = detect_people_in_region(
            region_id=medicao.regiao.id,
            simulate=True
        )
        
        # Determina status baseado na lógica de alertas
        status_nivel = self._calculate_alert_status(
            medicao=medicao,
            pessoas_detectadas=detection_result['pessoas_detectadas']
        )
        
        # Busca o status correspondente
        status = Status.objects.get(nivel=status_nivel)
        
        # Cria registro de risco humano
        risco_humano = RiscoHumano.objects.create(
            medicao=medicao,
            risco=detection_result['pessoas_detectadas'],
            status=status,
            processamento_tempo=detection_result['tempo_processamento'],
            confianca_ia=detection_result['confianca'],
            imagem=f"simulada_regiao_{medicao.regiao.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )
        
        return {
            'risco_detectado': detection_result['pessoas_detectadas'],
            'status_nivel': status_nivel,
            'alerta_critico': status_nivel == 2,
            'confianca': detection_result['confianca']
        }
    
    def _calculate_alert_status(self, medicao, pessoas_detectadas):
        """
        Calcula o nível de status/alerta baseado na lógica definida
        
        Lógica:
        - Normal (0): água=1 E chuva=1
        - Alerta (1): (água>=2 OU chuva>=2) E pessoas=False
        - Crítico (2): (água>=2 OU chuva>=2) E pessoas=True
        
        Args:
            medicao: Instância de Medicao
            pessoas_detectadas: bool
            
        Returns:
            int: Nível do status (0, 1 ou 2)
        """
        nivel_agua = medicao.nivel_agua.nivel
        volume_chuva = medicao.volume_chuva.nivel
        
        # Condição normal: água e chuva baixas
        if nivel_agua == 1 and volume_chuva == 1:
            return 0  # Normal (Verde)
        
        # Condições de risco: água ou chuva elevadas
        if nivel_agua >= 2 or volume_chuva >= 2:
            if pessoas_detectadas:
                return 2  # Crítico (Vermelho)
            else:
                return 1  # Alerta (Amarelo)
        
        # Fallback para normal
        return 0

# Instância global do simulador
simulator = DataSimulator()

def run_simulation():
    """Executa uma rodada de simulação completa"""
    return simulator.save_simulation_to_db()

def get_simulation_summary():
    """Retorna resumo da situação atual das regiões"""
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                s.nivel,
                s.descricao,
                s.cor,
                COUNT(rh.id) as total_regioes
            FROM status s
            LEFT JOIN risco_humano rh ON s.id = rh.id_status
            LEFT JOIN medicao m ON rh.id_medicao = m.id
            WHERE m.data >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
            GROUP BY s.nivel, s.descricao, s.cor
            ORDER BY s.nivel
        """)
        
        results = cursor.fetchall()
        
    summary = {
        'total_regioes': Regiao.objects.count(),
        'status_distribution': [
            {
                'nivel': row[0],
                'descricao': row[1],
                'cor': row[2],
                'count': row[3]
            }
            for row in results
        ],
        'ultima_simulacao': timezone.now()
    }
    
    return summary