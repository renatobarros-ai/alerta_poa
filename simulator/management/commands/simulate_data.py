from django.core.management.base import BaseCommand
from django.utils import timezone
from simulator.generator import run_simulation
import time

class Command(BaseCommand):
    help = 'Executa simulação de dados de sensores para todas as regiões'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--continuous',
            action='store_true',
            help='Executa simulação contínua a cada 30 segundos',
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=30,
            help='Intervalo em segundos entre simulações (default: 30)',
        )
        parser.add_argument(
            '--rounds',
            type=int,
            default=1,
            help='Número de rodadas de simulação (default: 1)',
        )
    
    def handle(self, *args, **options):
        if options['continuous']:
            self.run_continuous_simulation(options['interval'])
        else:
            self.run_batch_simulation(options['rounds'])
    
    def run_continuous_simulation(self, interval):
        """Executa simulação contínua"""
        self.stdout.write(
            self.style.SUCCESS(
                f'Iniciando simulação contínua (intervalo: {interval}s)'
            )
        )
        
        try:
            while True:
                result = run_simulation()
                
                self.stdout.write(
                    f"[{timezone.now().strftime('%H:%M:%S')}] "
                    f"Medições: {result['medicoes_criadas']} | "
                    f"Riscos: {result['riscos_avaliados']} | "
                    f"Alertas: {result['alertas_gerados']}"
                )
                
                if 'erro' in result:
                    self.stdout.write(
                        self.style.ERROR(f"Erro: {result['erro']}")
                    )
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('\nSimulação interrompida pelo usuário')
            )
    
    def run_batch_simulation(self, rounds):
        """Executa simulação em lotes"""
        self.stdout.write(
            self.style.SUCCESS(f'Executando {rounds} rodada(s) de simulação')
        )
        
        total_medicoes = 0
        total_riscos = 0
        total_alertas = 0
        
        for i in range(rounds):
            result = run_simulation()
            
            total_medicoes += result['medicoes_criadas']
            total_riscos += result['riscos_avaliados']
            total_alertas += result['alertas_gerados']
            
            self.stdout.write(
                f"Rodada {i+1}/{rounds}: "
                f"Medições: {result['medicoes_criadas']} | "
                f"Riscos: {result['riscos_avaliados']} | "
                f"Alertas: {result['alertas_gerados']}"
            )
            
            if 'erro' in result:
                self.stdout.write(
                    self.style.ERROR(f"Erro na rodada {i+1}: {result['erro']}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nResumo Final:\n'
                f'Total de medições: {total_medicoes}\n'
                f'Total de riscos avaliados: {total_riscos}\n'
                f'Total de alertas gerados: {total_alertas}'
            )
        )