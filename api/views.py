from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
from django.utils import timezone
from datetime import datetime, timedelta
from core.models import (
    Regiao, VolumeChuva, NivelAgua, Status, TextoAlerta,
    Cadastro, Medicao, RiscoHumano, EnvioAlerta
)
from .serializers import (
    RegiaoSerializer, VolumeChuvaSerializer, NivelAguaSerializer,
    StatusSerializer, CadastroSerializer, CadastroCreateSerializer,
    MedicaoSerializer, RiscoHumanoSerializer, EnvioAlertaSerializer,
    SituacaoAtualSerializer, HistoricoAlertasSerializer,
    DashboardStatsSerializer, RegiaoStatusSerializer
)
from simulator.generator import run_simulation, get_simulation_summary

# Views básicas dos modelos

class RegiaoListView(generics.ListAPIView):
    """Lista todas as regiões de Porto Alegre"""
    queryset = Regiao.objects.all().order_by('numero')
    serializer_class = RegiaoSerializer

class RegiaoDetailView(generics.RetrieveAPIView):
    """Detalhes de uma região específica"""
    queryset = Regiao.objects.all()
    serializer_class = RegiaoSerializer

class StatusListView(generics.ListAPIView):
    """Lista todos os status possíveis"""
    queryset = Status.objects.all().order_by('nivel')
    serializer_class = StatusSerializer

class CadastroListCreateView(generics.ListCreateAPIView):
    """Lista e cria cadastros de usuários"""
    queryset = Cadastro.objects.all().order_by('-created_at')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CadastroCreateSerializer
        return CadastroSerializer

class CadastroDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes, atualização e exclusão de cadastro"""
    queryset = Cadastro.objects.all()
    serializer_class = CadastroSerializer

class MedicaoListView(generics.ListAPIView):
    """Lista medições mais recentes"""
    serializer_class = MedicaoSerializer
    
    def get_queryset(self):
        # Últimas 24 horas por padrão
        since = timezone.now() - timedelta(hours=24)
        queryset = Medicao.objects.select_related(
            'regiao', 'nivel_agua', 'volume_chuva'
        ).filter(data__gte=since).order_by('-data')
        
        # Filtro por região se especificado
        regiao_id = self.request.query_params.get('regiao', None)
        if regiao_id:
            queryset = queryset.filter(regiao_id=regiao_id)
            
        return queryset

class RiscoHumanoListView(generics.ListAPIView):
    """Lista análises de risco humano"""
    serializer_class = RiscoHumanoSerializer
    
    def get_queryset(self):
        # Últimas 24 horas por padrão
        since = timezone.now() - timedelta(hours=24)
        queryset = RiscoHumano.objects.select_related(
            'medicao__regiao', 'status'
        ).filter(data__gte=since).order_by('-data')
        
        # Filtro por risco detectado
        risco = self.request.query_params.get('risco', None)
        if risco is not None:
            queryset = queryset.filter(risco=risco.lower() == 'true')
            
        return queryset

# Views especializadas

@api_view(['GET'])
def situacao_atual(request):
    """View para situação atual de todas as regiões"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                r.id,
                r.numero,
                r.nome as regiao,
                COALESCE(s.descricao, 'Normal') as status_atual,
                COALESCE(s.cor, 'Verde') as cor_atual,
                COUNT(DISTINCT c.id) as usuarios_cadastrados,
                MAX(m.data) as ultima_medicao
            FROM core_regiao r
            LEFT JOIN core_medicao m ON r.id = m.regiao_id
            LEFT JOIN core_riscohumano rh ON m.id = rh.medicao_id
            LEFT JOIN core_status s ON rh.status_id = s.id
            LEFT JOIN core_cadastro c ON r.id = c.regiao_id AND c.situacao = 'ATIVO'
            GROUP BY r.id, r.numero, r.nome, s.descricao, s.cor
            ORDER BY r.numero
        """)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'numero': row[1],
                'nome': row[2],
                'status_atual': row[3],
                'cor_atual': row[4],
                'usuarios_cadastrados': row[5],
                'ultima_medicao': row[6]
            })
    
    serializer = SituacaoAtualSerializer(results, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def dashboard_stats(request):
    """Estatísticas para o dashboard principal"""
    # Contadores básicos
    total_regioes = Regiao.objects.count()
    total_usuarios = Cadastro.objects.count()
    usuarios_ativos = Cadastro.objects.filter(situacao='ATIVO').count()
    
    # Alertas de hoje
    hoje = timezone.now().date()
    alertas_hoje = EnvioAlerta.objects.filter(data__date=hoje).count()
    
    data = {
        'total_regioes': total_regioes,
        'regioes_normais': 0,
        'regioes_alerta': 0, 
        'regioes_criticas': 0,
        'total_usuarios': total_usuarios,
        'usuarios_ativos': usuarios_ativos,
        'alertas_hoje': alertas_hoje,
        'ultima_atualizacao': timezone.now()
    }
    
    serializer = DashboardStatsSerializer(data)
    return Response(serializer.data)

@api_view(['POST'])
def executar_simulacao(request):
    """Executa uma rodada de simulação manualmente"""
    try:
        resultado = run_simulation()
        return Response({
            'sucesso': True,
            'resultado': resultado,
            'timestamp': timezone.now()
        })
    except Exception as e:
        return Response({
            'sucesso': False,
            'erro': str(e),
            'timestamp': timezone.now()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
