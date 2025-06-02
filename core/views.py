from django.shortcuts import render
from django.http import JsonResponse
from .models import Regiao, Status, Cadastro

def dashboard(request):
    """View principal com mapa interativo"""
    context = {
        'page_title': 'Dashboard - Sistema de Monitoramento',
        'total_regioes': Regiao.objects.count(),
    }
    return render(request, 'dashboard.html', context)

def historico(request):
    """View do histórico de alertas"""
    context = {
        'page_title': 'Histórico de Alertas',
    }
    return render(request, 'historico.html', context)

def cadastro(request):
    """View de cadastro de usuários"""
    context = {
        'page_title': 'Cadastro de Usuários',
        'regioes': Regiao.objects.all().order_by('numero'),
    }
    return render(request, 'cadastro.html', context)
