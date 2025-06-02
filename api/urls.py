from django.urls import path
from . import views

urlpatterns = [
    # Endpoints básicos dos modelos
    path('regioes/', views.RegiaoListView.as_view(), name='regiao-list'),
    path('regioes/<int:pk>/', views.RegiaoDetailView.as_view(), name='regiao-detail'),
    path('status/', views.StatusListView.as_view(), name='status-list'),
    path('cadastros/', views.CadastroListCreateView.as_view(), name='cadastro-list-create'),
    path('cadastros/<int:pk>/', views.CadastroDetailView.as_view(), name='cadastro-detail'),
    path('medicoes/', views.MedicaoListView.as_view(), name='medicao-list'),
    path('riscos/', views.RiscoHumanoListView.as_view(), name='risco-list'),
    
    # Endpoints especializados
    path('situacao-atual/', views.situacao_atual, name='situacao-atual'),
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    path('simulacao/executar/', views.executar_simulacao, name='executar-simulacao'),
]