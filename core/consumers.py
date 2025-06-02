import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from datetime import timedelta

class AlagamentosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Adiciona o cliente ao grupo de atualizações de alagamentos
        await self.channel_layer.group_add(
            "alagamentos_updates",
            self.channel_name
        )
        await self.accept()
        
        # Envia dados iniciais
        await self.send_initial_data()

    async def disconnect(self, close_code):
        # Remove o cliente do grupo
        await self.channel_layer.group_discard(
            "alagamentos_updates",
            self.channel_name
        )

    async def receive(self, text_data):
        # Processa mensagens recebidas do cliente
        try:
            data = json.loads(text_data)
            message_type = data.get('type', '')
            
            if message_type == 'request_update':
                # Cliente solicita atualização manual
                await self.send_current_status()
            elif message_type == 'subscribe_region':
                # Cliente quer se inscrever em uma região específica
                region_id = data.get('region_id')
                if region_id:
                    await self.send_region_status(region_id)
                    
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))

    async def send_initial_data(self):
        """Envia dados iniciais ao conectar"""
        current_status = await self.get_current_status()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'data': current_status,
            'timestamp': timezone.now().isoformat()
        }))

    async def send_current_status(self):
        """Envia status atual de todas as regiões"""
        current_status = await self.get_current_status()
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'data': current_status,
            'timestamp': timezone.now().isoformat()
        }))

    async def send_region_status(self, region_id):
        """Envia status de uma região específica"""
        region_data = await self.get_region_data(region_id)
        await self.send(text_data=json.dumps({
            'type': 'region_update',
            'region_id': region_id,
            'data': region_data,
            'timestamp': timezone.now().isoformat()
        }))

    # Handlers para mensagens do grupo
    async def status_update(self, event):
        """Handler para atualizações de status vindas do grupo"""
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'data': event['data'],
            'timestamp': event['timestamp']
        }))

    async def region_alert(self, event):
        """Handler para alertas específicos de região"""
        await self.send(text_data=json.dumps({
            'type': 'region_alert',
            'region_id': event['region_id'],
            'alert_level': event['alert_level'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    async def system_notification(self, event):
        """Handler para notificações do sistema"""
        await self.send(text_data=json.dumps({
            'type': 'system_notification',
            'message': event['message'],
            'level': event.get('level', 'info'),
            'timestamp': event['timestamp']
        }))

    # Métodos de acesso ao banco de dados
    @database_sync_to_async
    def get_current_status(self):
        """Busca status atual de todas as regiões"""
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT
                    r.id as regiao_id,
                    r.numero,
                    r.nome as regiao_nome,
                    COALESCE(s.nivel, 0) as status_nivel,
                    COALESCE(s.cor, 'Verde') as status_cor,
                    COALESCE(s.descricao, 'Normal') as status_descricao,
                    COALESCE(rh.risco, 0) as pessoas_detectadas,
                    COALESCE(na.nivel, 1) as nivel_agua,
                    COALESCE(vc.nivel, 1) as volume_chuva,
                    rh.confianca_ia,
                    COALESCE(m.data, NOW()) as timestamp
                FROM core_regiao r
                LEFT JOIN (
                    SELECT regiao_id, MAX(data) as max_data
                    FROM core_medicao
                    WHERE data >= %s
                    GROUP BY regiao_id
                ) latest_m ON r.id = latest_m.regiao_id
                LEFT JOIN core_medicao m ON r.id = m.regiao_id AND m.data = latest_m.max_data
                LEFT JOIN core_riscohumano rh ON m.id = rh.medicao_id
                LEFT JOIN core_status s ON rh.status_id = s.id
                LEFT JOIN core_nivelagua na ON m.nivel_agua_id = na.id
                LEFT JOIN core_volumechuva vc ON m.volume_chuva_id = vc.id
                ORDER BY r.numero
            """, [timezone.now() - timedelta(hours=1)])
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'regiao_id': row[0],
                    'numero': row[1],
                    'regiao_nome': row[2],
                    'status_nivel': row[3],
                    'status_cor': row[4],
                    'status_descricao': row[5],
                    'pessoas_detectadas': bool(row[6]),
                    'nivel_agua': row[7],
                    'volume_chuva': row[8],
                    'confianca_ia': float(row[9]) if row[9] else None,
                    'timestamp': row[10].isoformat() if row[10] else None
                })
        
        return results

    @database_sync_to_async
    def get_region_data(self, region_id):
        """Busca dados de uma região específica"""
        from core.models import Regiao, Medicao, RiscoHumano
        
        try:
            regiao = Regiao.objects.get(id=region_id)
            
            # Última medição da região
            ultima_medicao = Medicao.objects.filter(
                regiao=regiao
            ).order_by('-data').first()
            
            if ultima_medicao:
                # Busca risco humano se existir
                risco_humano = getattr(ultima_medicao, 'risco_humano', None)
                
                return {
                    'regiao_id': regiao.id,
                    'numero': regiao.numero,
                    'nome': regiao.nome,
                    'status_nivel': risco_humano.status.nivel if risco_humano else 0,
                    'status_cor': risco_humano.status.cor if risco_humano else 'Verde',
                    'status_descricao': risco_humano.status.descricao if risco_humano else 'Normal',
                    'pessoas_detectadas': risco_humano.risco if risco_humano else False,
                    'nivel_agua': ultima_medicao.nivel_agua.nivel,
                    'volume_chuva': ultima_medicao.volume_chuva.nivel,
                    'confianca_ia': float(risco_humano.confianca_ia) if risco_humano and risco_humano.confianca_ia else None,
                    'timestamp': ultima_medicao.data.isoformat()
                }
            else:
                return {
                    'regiao_id': regiao.id,
                    'numero': regiao.numero,
                    'nome': regiao.nome,
                    'status_nivel': 0,
                    'status_cor': 'Verde',
                    'status_descricao': 'Normal',
                    'pessoas_detectadas': False,
                    'nivel_agua': 1,
                    'volume_chuva': 1,
                    'confianca_ia': None,
                    'timestamp': timezone.now().isoformat()
                }
                
        except Regiao.DoesNotExist:
            return None


# Funções auxiliares para enviar updates via WebSocket
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_status_update(data):
    """Envia atualização de status para todos os clientes conectados"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "alagamentos_updates",
        {
            "type": "status_update",
            "data": data,
            "timestamp": timezone.now().isoformat()
        }
    )

def send_region_alert(region_id, alert_level, message):
    """Envia alerta específico de região"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "alagamentos_updates",
        {
            "type": "region_alert",
            "region_id": region_id,
            "alert_level": alert_level,
            "message": message,
            "timestamp": timezone.now().isoformat()
        }
    )

def send_system_notification(message, level="info"):
    """Envia notificação do sistema"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "alagamentos_updates",
        {
            "type": "system_notification",
            "message": message,
            "level": level,
            "timestamp": timezone.now().isoformat()
        }
    )