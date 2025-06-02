from django.db import models

class Regiao(models.Model):
    numero = models.PositiveSmallIntegerField(unique=True)
    nome = models.CharField(max_length=100, unique=True)
    geojson = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'regiao'
        verbose_name = 'Região'
        verbose_name_plural = 'Regiões'
        indexes = [
            models.Index(fields=['numero'], name='idx_regiao_numero'),
        ]
    
    def __str__(self):
        return f"{self.numero} - {self.nome}"

class VolumeChuva(models.Model):
    nivel = models.PositiveSmallIntegerField(unique=True)
    descricao = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'volume_chuva'
        verbose_name = 'Volume de Chuva'
        verbose_name_plural = 'Volumes de Chuva'
    
    def __str__(self):
        return f"{self.nivel} - {self.descricao}"

class NivelAgua(models.Model):
    nivel = models.PositiveSmallIntegerField(unique=True)
    descricao = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'nivel_agua'
        verbose_name = 'Nível de Água'
        verbose_name_plural = 'Níveis de Água'
    
    def __str__(self):
        return f"{self.nivel} - {self.descricao}"

class Status(models.Model):
    nivel = models.PositiveSmallIntegerField(unique=True)
    descricao = models.CharField(max_length=50)
    cor = models.CharField(max_length=20)
    tipo_alerta = models.CharField(max_length=50)
    cnn_ativa = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'status'
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
        indexes = [
            models.Index(fields=['cnn_ativa'], name='idx_status_cnn_ativa'),
        ]
    
    def __str__(self):
        return f"{self.nivel} - {self.descricao} ({self.cor})"

class TextoAlerta(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='textos', db_column='id_status')
    texto = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'texto_alerta'
        verbose_name = 'Texto de Alerta'
        verbose_name_plural = 'Textos de Alerta'
        indexes = [
            models.Index(fields=['status'], name='idx_texto_alerta_status'),
        ]
    
    def __str__(self):
        return f"Texto para {self.status.descricao}"

class Cadastro(models.Model):
    SITUACAO_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
        ('BLOQUEADO', 'Bloqueado'),
    ]
    
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    regiao = models.ForeignKey(Regiao, on_delete=models.RESTRICT, related_name='usuarios', db_column='id_regiao')
    situacao = models.CharField(max_length=10, choices=SITUACAO_CHOICES, default='ATIVO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cadastro'
        verbose_name = 'Cadastro'
        verbose_name_plural = 'Cadastros'
        indexes = [
            models.Index(fields=['regiao'], name='idx_cadastro_regiao'),
            models.Index(fields=['situacao'], name='idx_cadastro_situacao'),
            models.Index(fields=['telefone'], name='idx_cadastro_telefone'),
        ]
    
    def __str__(self):
        return f"{self.nome} - {self.regiao.nome}"

class Medicao(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    regiao = models.ForeignKey(Regiao, on_delete=models.CASCADE, related_name='medicoes', db_column='id_regiao')
    nivel_agua = models.ForeignKey(NivelAgua, on_delete=models.RESTRICT, db_column='id_nivel_agua')
    volume_chuva = models.ForeignKey(VolumeChuva, on_delete=models.RESTRICT, db_column='id_volume_chuva')
    avaliar_risco = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'medicao'
        verbose_name = 'Medição'
        verbose_name_plural = 'Medições'
        indexes = [
            models.Index(fields=['data'], name='idx_medicao_data'),
            models.Index(fields=['regiao'], name='idx_medicao_regiao'),
            models.Index(fields=['avaliar_risco'], name='idx_medicao_risco'),
            models.Index(fields=['regiao', 'data'], name='idx_medicao_regiao_data'),
        ]
    
    def __str__(self):
        return f"{self.regiao.nome} - {self.data.strftime('%d/%m/%Y %H:%M')}"

class RiscoHumano(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    medicao = models.OneToOneField(Medicao, on_delete=models.CASCADE, related_name='risco_humano', db_column='id_medicao')
    imagem = models.CharField(max_length=500, null=True, blank=True)
    risco = models.BooleanField(default=False)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT, db_column='id_status')
    processamento_tempo = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True, 
                                            help_text='Tempo processamento CNN em segundos')
    confianca_ia = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True,
                                     help_text='Nível de confiança da IA (0-1)')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'risco_humano'
        verbose_name = 'Risco Humano'
        verbose_name_plural = 'Riscos Humanos'
        indexes = [
            models.Index(fields=['data'], name='idx_risco_humano_data'),
            models.Index(fields=['risco'], name='idx_risco_humano_risco'),
            models.Index(fields=['status'], name='idx_risco_humano_status'),
        ]
    
    def __str__(self):
        return f"{self.medicao.regiao.nome} - {'RISCO' if self.risco else 'SEGURO'}"

class EnvioAlerta(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    risco_humano = models.ForeignKey(RiscoHumano, on_delete=models.CASCADE, related_name='envios', db_column='id_risco_humano')
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE, related_name='alertas_recebidos', db_column='id_cadastro')
    envio_whats = models.BooleanField(default=False)
    envio_email = models.BooleanField(default=False)
    sucesso_whats = models.BooleanField(null=True, blank=True)
    sucesso_email = models.BooleanField(null=True, blank=True)
    erro_whats = models.TextField(null=True, blank=True)
    erro_email = models.TextField(null=True, blank=True)
    tentativas_whats = models.PositiveSmallIntegerField(default=0)
    tentativas_email = models.PositiveSmallIntegerField(default=0)
    comentario = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'envio_alerta'
        verbose_name = 'Envio de Alerta'
        verbose_name_plural = 'Envios de Alerta'
        indexes = [
            models.Index(fields=['data'], name='idx_envio_alerta_data'),
            models.Index(fields=['risco_humano'], name='idx_envio_alerta_risco'),
            models.Index(fields=['cadastro'], name='idx_envio_alerta_cadastro'),
            models.Index(fields=['sucesso_whats', 'sucesso_email'], name='idx_envio_alerta_sucesso'),
        ]
    
    def __str__(self):
        return f"Alerta para {self.cadastro.nome} - {self.data.strftime('%d/%m/%Y %H:%M')}"
