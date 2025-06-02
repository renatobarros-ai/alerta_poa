from rest_framework import serializers
from core.models import (
    Regiao, VolumeChuva, NivelAgua, Status, TextoAlerta,
    Cadastro, Medicao, RiscoHumano, EnvioAlerta
)

class RegiaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regiao
        fields = ['id', 'numero', 'nome', 'geojson', 'created_at', 'updated_at']

class VolumeChuvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolumeChuva
        fields = ['id', 'nivel', 'descricao', 'created_at']

class NivelAguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelAgua
        fields = ['id', 'nivel', 'descricao', 'created_at']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'nivel', 'descricao', 'cor', 'tipo_alerta', 'cnn_ativa', 'created_at']

class TextoAlertaSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    
    class Meta:
        model = TextoAlerta
        fields = ['id', 'status', 'texto', 'created_at', 'updated_at']

class CadastroSerializer(serializers.ModelSerializer):
    regiao_nome = serializers.CharField(source='regiao.nome', read_only=True)
    
    class Meta:
        model = Cadastro
        fields = [
            'id', 'nome', 'telefone', 'email', 'regiao', 'regiao_nome',
            'situacao', 'created_at', 'updated_at'
        ]

class CadastroCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadastro
        fields = ['nome', 'telefone', 'email', 'regiao', 'situacao']
        
    def validate_email(self, value):
        if Cadastro.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está cadastrado.")
        return value

class MedicaoSerializer(serializers.ModelSerializer):
    regiao_nome = serializers.CharField(source='regiao.nome', read_only=True)
    nivel_agua_descricao = serializers.CharField(source='nivel_agua.descricao', read_only=True)
    volume_chuva_descricao = serializers.CharField(source='volume_chuva.descricao', read_only=True)
    
    class Meta:
        model = Medicao
        fields = [
            'id', 'data', 'regiao', 'regiao_nome',
            'nivel_agua', 'nivel_agua_descricao',
            'volume_chuva', 'volume_chuva_descricao',
            'avaliar_risco', 'created_at'
        ]

class RiscoHumanoSerializer(serializers.ModelSerializer):
    medicao = MedicaoSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    
    class Meta:
        model = RiscoHumano
        fields = [
            'id', 'data', 'medicao', 'imagem', 'risco', 'status',
            'processamento_tempo', 'confianca_ia', 'created_at'
        ]

class EnvioAlertaSerializer(serializers.ModelSerializer):
    risco_humano = RiscoHumanoSerializer(read_only=True)
    cadastro = CadastroSerializer(read_only=True)
    
    class Meta:
        model = EnvioAlerta
        fields = [
            'id', 'data', 'risco_humano', 'cadastro',
            'envio_whats', 'envio_email', 'sucesso_whats', 'sucesso_email',
            'erro_whats', 'erro_email', 'tentativas_whats', 'tentativas_email',
            'comentario', 'created_at', 'updated_at'
        ]

# Serializers para Views específicas

class SituacaoAtualSerializer(serializers.Serializer):
    """Serializer para a view de situação atual das regiões"""
    id = serializers.IntegerField()
    numero = serializers.IntegerField()
    nome = serializers.CharField()
    status_atual = serializers.CharField()
    cor_atual = serializers.CharField()
    usuarios_cadastrados = serializers.IntegerField()
    ultima_medicao = serializers.DateTimeField(allow_null=True)

class HistoricoAlertasSerializer(serializers.Serializer):
    """Serializer para a view de histórico de alertas"""
    id = serializers.IntegerField()
    data = serializers.DateTimeField()
    regiao = serializers.CharField()
    usuario = serializers.CharField()
    telefone = serializers.CharField()
    email = serializers.EmailField()
    tipo_alerta = serializers.CharField()
    cor = serializers.CharField()
    envio_whats = serializers.BooleanField()
    envio_email = serializers.BooleanField()
    sucesso_whats = serializers.BooleanField(allow_null=True)
    sucesso_email = serializers.BooleanField(allow_null=True)
    confianca_ia = serializers.DecimalField(max_digits=5, decimal_places=3, allow_null=True)

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer para estatísticas do dashboard"""
    total_regioes = serializers.IntegerField()
    regioes_normais = serializers.IntegerField()
    regioes_alerta = serializers.IntegerField()
    regioes_criticas = serializers.IntegerField()
    total_usuarios = serializers.IntegerField()
    usuarios_ativos = serializers.IntegerField()
    alertas_hoje = serializers.IntegerField()
    ultima_atualizacao = serializers.DateTimeField()

class RegiaoStatusSerializer(serializers.Serializer):
    """Serializer simplificado para status das regiões (WebSocket)"""
    regiao_id = serializers.IntegerField()
    regiao_nome = serializers.CharField()
    status_nivel = serializers.IntegerField()
    status_cor = serializers.CharField()
    status_descricao = serializers.CharField()
    pessoas_detectadas = serializers.BooleanField()
    nivel_agua = serializers.IntegerField()
    volume_chuva = serializers.IntegerField()
    confianca_ia = serializers.DecimalField(max_digits=5, decimal_places=3, allow_null=True)
    timestamp = serializers.DateTimeField()