from django.contrib import admin
from .models import (
    Regiao, VolumeChuva, NivelAgua, Status, TextoAlerta,
    Cadastro, Medicao, RiscoHumano, EnvioAlerta
)

@admin.register(Regiao)
class RegiaoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'nome', 'created_at']
    list_filter = ['created_at']
    search_fields = ['nome', 'numero']
    ordering = ['numero']

@admin.register(VolumeChuva)
class VolumeChuvaAdmin(admin.ModelAdmin):
    list_display = ['nivel', 'descricao', 'created_at']
    ordering = ['nivel']

@admin.register(NivelAgua)
class NivelAguaAdmin(admin.ModelAdmin):
    list_display = ['nivel', 'descricao', 'created_at']
    ordering = ['nivel']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['nivel', 'descricao', 'cor', 'tipo_alerta', 'cnn_ativa']
    list_filter = ['cnn_ativa', 'cor']
    ordering = ['nivel']

@admin.register(TextoAlerta)
class TextoAlertaAdmin(admin.ModelAdmin):
    list_display = ['status', 'texto', 'created_at']
    list_filter = ['status', 'created_at']

@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'regiao', 'situacao', 'created_at']
    list_filter = ['situacao', 'regiao', 'created_at']
    search_fields = ['nome', 'email', 'telefone']
    ordering = ['-created_at']

@admin.register(Medicao)
class MedicaoAdmin(admin.ModelAdmin):
    list_display = ['regiao', 'data', 'nivel_agua', 'volume_chuva', 'avaliar_risco']
    list_filter = ['avaliar_risco', 'nivel_agua', 'volume_chuva', 'regiao', 'data']
    ordering = ['-data']

@admin.register(RiscoHumano)
class RiscoHumanoAdmin(admin.ModelAdmin):
    list_display = ['medicao', 'data', 'risco', 'status', 'confianca_ia', 'processamento_tempo']
    list_filter = ['risco', 'status', 'data']
    ordering = ['-data']

@admin.register(EnvioAlerta)
class EnvioAlertaAdmin(admin.ModelAdmin):
    list_display = ['cadastro', 'data', 'risco_humano', 'envio_whats', 'envio_email', 'sucesso_whats', 'sucesso_email']
    list_filter = ['envio_whats', 'envio_email', 'sucesso_whats', 'sucesso_email', 'data']
    ordering = ['-data']
