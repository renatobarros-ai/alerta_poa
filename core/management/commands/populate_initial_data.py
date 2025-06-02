from django.core.management.base import BaseCommand
from core.models import VolumeChuva, NivelAgua, Status, TextoAlerta, Regiao, Cadastro

class Command(BaseCommand):
    help = 'Popula dados iniciais obrigatórios do sistema'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a recriação dos dados mesmo se já existirem',
        )
    
    def handle(self, *args, **options):
        force = options['force']
        
        self.stdout.write('Iniciando população de dados iniciais...')
        
        # 1. Volume de Chuva
        self.create_volume_chuva(force)
        
        # 2. Nível de Água
        self.create_nivel_agua(force)
        
        # 3. Status
        self.create_status(force)
        
        # 4. Textos de Alerta
        self.create_texto_alerta(force)
        
        # 5. Regiões de Porto Alegre
        self.create_regioes(force)
        
        # 6. Usuários de exemplo (opcional)
        self.create_usuarios_exemplo()
        
        self.stdout.write(
            self.style.SUCCESS('Dados iniciais populados com sucesso!')
        )
    
    def create_volume_chuva(self, force):
        if VolumeChuva.objects.exists() and not force:
            self.stdout.write('Volume de chuva já existe, pulando...')
            return
        
        if force:
            VolumeChuva.objects.all().delete()
        
        volumes = [
            (1, 'Baixa'),
            (2, 'Moderada'),
            (3, 'Intensa'),
        ]
        
        for nivel, descricao in volumes:
            VolumeChuva.objects.get_or_create(
                nivel=nivel,
                defaults={'descricao': descricao}
            )
        
        self.stdout.write('✓ Volumes de chuva criados')
    
    def create_nivel_agua(self, force):
        if NivelAgua.objects.exists() and not force:
            self.stdout.write('Níveis de água já existem, pulando...')
            return
        
        if force:
            NivelAgua.objects.all().delete()
        
        niveis = [
            (1, 'Normal'),
            (2, 'Alerta'),
            (3, 'Crítico'),
        ]
        
        for nivel, descricao in niveis:
            NivelAgua.objects.get_or_create(
                nivel=nivel,
                defaults={'descricao': descricao}
            )
        
        self.stdout.write('✓ Níveis de água criados')
    
    def create_status(self, force):
        if Status.objects.exists() and not force:
            self.stdout.write('Status já existem, pulando...')
            return
        
        if force:
            Status.objects.all().delete()
        
        status_list = [
            (0, 'Normal', 'Verde', 'Nenhum', False),
            (1, 'Preventivo', 'Amarelo', 'Monitoramento', True),
            (2, 'Crítico', 'Vermelho', 'Evacuação', True),
        ]
        
        for nivel, descricao, cor, tipo_alerta, cnn_ativa in status_list:
            Status.objects.get_or_create(
                nivel=nivel,
                defaults={
                    'descricao': descricao,
                    'cor': cor,
                    'tipo_alerta': tipo_alerta,
                    'cnn_ativa': cnn_ativa
                }
            )
        
        self.stdout.write('✓ Status criados')
    
    def create_texto_alerta(self, force):
        if TextoAlerta.objects.exists() and not force:
            self.stdout.write('Textos de alerta já existem, pulando...')
            return
        
        if force:
            TextoAlerta.objects.all().delete()
        
        # Busca os status criados
        try:
            status_preventivo = Status.objects.get(nivel=1)
            status_critico = Status.objects.get(nivel=2)
            
            textos = [
                (status_preventivo, 'ATENÇÃO: Condições de risco detectadas na sua região. Mantenha-se alerta e evite áreas alagáveis.'),
                (status_critico, 'ALERTA CRÍTICO: Risco iminente de alagamento com pessoas em área de perigo. Procure local seguro imediatamente!'),
            ]
            
            for status, texto in textos:
                TextoAlerta.objects.get_or_create(
                    status=status,
                    defaults={'texto': texto}
                )
            
            self.stdout.write('✓ Textos de alerta criados')
            
        except Status.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Erro: Status não encontrados. Execute primeiro a criação de status.')
            )
    
    def create_regioes(self, force):
        if Regiao.objects.exists() and not force:
            self.stdout.write('Regiões já existem, pulando...')
            return
        
        if force:
            Regiao.objects.all().delete()
        
        # 16 regiões administrativas de Porto Alegre
        regioes = [
            (1, 'Centro Histórico'),
            (2, 'Noroeste'),
            (3, 'Nordeste'),
            (4, 'Leste'),
            (5, 'Sudeste'),
            (6, 'Sul'),
            (7, 'Sudoeste'),
            (8, 'Oeste'),
            (9, 'Centro-Sul'),
            (10, 'Cristal'),
            (11, 'Cruzeiro'),
            (12, 'Norte'),
            (13, 'Eixo Baltazar'),
            (14, 'Partenon'),
            (15, 'Glória'),
            (16, 'Restinga'),
        ]
        
        for numero, nome in regioes:
            # GeoJSON simplificado (em produção, usaria dados reais)
            geojson = f'{{"type":"Polygon","coordinates":[[[-51.{220+numero},-30.{30+numero*2}],[-51.{210+numero},-30.{30+numero*2}],[-51.{210+numero},-30.{40+numero*2}],[-51.{220+numero},-30.{40+numero*2}],[-51.{220+numero},-30.{30+numero*2}]]]}}'
            
            Regiao.objects.get_or_create(
                numero=numero,
                defaults={
                    'nome': nome,
                    'geojson': geojson
                }
            )
        
        self.stdout.write('✓ Regiões de Porto Alegre criadas')
    
    def create_usuarios_exemplo(self):
        if Cadastro.objects.exists():
            self.stdout.write('Usuários de exemplo já existem, pulando...')
            return
        
        # Cria alguns usuários de exemplo para teste
        regioes = list(Regiao.objects.all()[:5])  # Primeiras 5 regiões
        
        usuarios_exemplo = [
            ('João Silva', '51999887766', 'joao.silva@email.com'),
            ('Maria Santos', '51988776655', 'maria.santos@email.com'),
            ('Pedro Costa', '51977665544', 'pedro.costa@email.com'),
            ('Ana Oliveira', '51966554433', 'ana.oliveira@email.com'),
            ('Carlos Souza', '51955443322', 'carlos.souza@email.com'),
        ]
        
        for i, (nome, telefone, email) in enumerate(usuarios_exemplo):
            if i < len(regioes):
                Cadastro.objects.get_or_create(
                    email=email,
                    defaults={
                        'nome': nome,
                        'telefone': telefone,
                        'regiao': regioes[i],
                        'situacao': 'ATIVO'
                    }
                )
        
        self.stdout.write('✓ Usuários de exemplo criados')