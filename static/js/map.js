/**
 * Gerenciador do Mapa Leaflet para visualização das regiões
 */
class MapController {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.map = null;
        this.regions = new Map();
        this.markers = new Map();
        
        // Configurações padrão
        this.options = {
            center: [-30.0346, -51.2177], // Porto Alegre
            zoom: 11,
            maxZoom: 18,
            minZoom: 9,
            ...options
        };
        
        // Callbacks
        this.onRegionClick = null;
        this.onRegionHover = null;
        this.onMapReady = null;
    }
    
    initialize() {
        // Cria o mapa
        this.map = L.map(this.containerId).setView(this.options.center, this.options.zoom);
        
        // Adiciona camada de tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: this.options.maxZoom,
            minZoom: this.options.minZoom
        }).addTo(this.map);
        
        // Configurações do mapa
        this.map.setMaxBounds([
            [-31.5, -52.5], // Southwest
            [-28.5, -49.5]  // Northeast
        ]);
        
        if (this.onMapReady) {
            this.onMapReady(this.map);
        }
        
        console.log('Mapa inicializado');
    }
    
    loadRegions(regionsData) {
        regionsData.forEach(region => {
            this.addRegion(region);
        });
    }
    
    addRegion(regionData) {
        // Para demonstração, cria círculos em posições aleatórias
        // Em produção, usaria os dados GeoJSON reais do campo 'geojson'
        const baseLatLng = this.getRegionPosition(regionData.numero);
        
        const circle = L.circle(baseLatLng, {
            color: this.getRegionColor(regionData.status || 'Normal'),
            fillColor: this.getRegionColor(regionData.status || 'Normal'),
            fillOpacity: 0.7,
            radius: 2000,
            weight: 2
        });
        
        // Adiciona dados customizados
        circle.regionId = regionData.id;
        circle.regionData = regionData;
        
        // Eventos
        circle.on('click', (e) => {
            if (this.onRegionClick) {
                this.onRegionClick(regionData, e);
            }
            this.showRegionPopup(regionData, e.latlng);
        });
        
        circle.on('mouseover', (e) => {
            circle.setStyle({ weight: 4 });
            if (this.onRegionHover) {
                this.onRegionHover(regionData, e);
            }
        });
        
        circle.on('mouseout', (e) => {
            circle.setStyle({ weight: 2 });
        });
        
        // Adiciona ao mapa
        circle.addTo(this.map);
        
        // Armazena referência
        this.regions.set(regionData.id, circle);
        
        console.log(`Região ${regionData.nome} adicionada ao mapa`);
    }
    
    updateRegion(regionId, newData) {
        const region = this.regions.get(regionId);
        if (region) {
            // Atualiza cor baseada no status
            const color = this.getRegionColor(newData.status_cor || 'Verde');
            region.setStyle({
                color: color,
                fillColor: color
            });
            
            // Atualiza dados
            region.regionData = { ...region.regionData, ...newData };
            
            console.log(`Região ${regionId} atualizada`);
        }
    }
    
    updateAllRegions(regionsData) {
        regionsData.forEach(regionData => {
            this.updateRegion(regionData.regiao_id, regionData);
        });
    }
    
    showRegionPopup(regionData, latlng) {
        const status = regionData.status_cor || 'Verde';
        const statusClass = this.getStatusClass(status);
        const statusIcon = this.getStatusIcon(status);
        
        const popupContent = `
            <div class="region-popup">
                <h6><strong>${regionData.regiao_nome || regionData.nome}</strong></h6>
                <p class="mb-1">Região ${regionData.numero || regionData.regiao_id}</p>
                
                <div class="status-badge">
                    <span class="badge ${statusClass}">
                        <i class="${statusIcon}"></i> 
                        ${regionData.status_descricao || status}
                    </span>
                </div>
                
                <div class="mt-2">
                    <small class="text-muted">
                        <i class="fas fa-tint"></i> Água: ${this.getNivelText(regionData.nivel_agua)}<br>
                        <i class="fas fa-cloud-rain"></i> Chuva: ${this.getVolumeText(regionData.volume_chuva)}<br>
                        <i class="fas fa-users"></i> Pessoas: ${regionData.pessoas_detectadas ? 'Detectadas' : 'Não detectadas'}
                        ${regionData.confianca_ia ? '<br><i class="fas fa-brain"></i> Confiança: ' + (regionData.confianca_ia * 100).toFixed(1) + '%' : ''}
                    </small>
                </div>
                
                <div class="mt-2">
                    <button class="btn btn-sm btn-primary" onclick="abrirModalRegiao(${regionData.regiao_id || regionData.id})">
                        Ver Detalhes
                    </button>
                </div>
            </div>
        `;
        
        L.popup()
            .setLatLng(latlng)
            .setContent(popupContent)
            .openOn(this.map);
    }
    
    getRegionPosition(numero) {
        // Posições aproximadas das regiões de Porto Alegre
        // Em produção, isso viria dos dados GeoJSON
        const positions = {
            1: [-30.0346, -51.2177],  // Centro
            2: [-30.0200, -51.2000],  // Norte
            3: [-30.0500, -51.2000],  // Sul
            4: [-30.0346, -51.2400],  // Leste
            5: [-30.0346, -51.1900],  // Oeste
            6: [-30.0100, -51.2100],
            7: [-30.0600, -51.2100],
            8: [-30.0250, -51.2300],
            9: [-30.0450, -51.2300],
            10: [-30.0150, -51.1950],
            11: [-30.0550, -51.1950],
            12: [-30.0300, -51.2450],
            13: [-30.0400, -51.2450],
            14: [-30.0200, -51.1850],
            15: [-30.0500, -51.1850],
            16: [-30.0350, -51.2250]
        };
        
        return positions[numero] || [-30.0346, -51.2177];
    }
    
    getRegionColor(status) {
        switch (status.toLowerCase()) {
            case 'verde':
            case 'normal':
                return '#28a745';
            case 'amarelo':
            case 'alerta':
                return '#ffc107';
            case 'vermelho':
            case 'crítico':
            case 'critico':
                return '#dc3545';
            default:
                return '#28a745';
        }
    }
    
    getStatusClass(status) {
        switch (status.toLowerCase()) {
            case 'verde':
            case 'normal':
                return 'status-normal';
            case 'amarelo':
            case 'alerta':
                return 'status-alerta';
            case 'vermelho':
            case 'crítico':
            case 'critico':
                return 'status-critico';
            default:
                return 'status-normal';
        }
    }
    
    getStatusIcon(status) {
        switch (status.toLowerCase()) {
            case 'verde':
            case 'normal':
                return 'fas fa-check-circle';
            case 'amarelo':
            case 'alerta':
                return 'fas fa-exclamation-triangle';
            case 'vermelho':
            case 'crítico':
            case 'critico':
                return 'fas fa-exclamation-circle';
            default:
                return 'fas fa-question-circle';
        }
    }
    
    getNivelText(nivel) {
        switch (nivel) {
            case 1: return 'Normal';
            case 2: return 'Alerta';
            case 3: return 'Crítico';
            default: return 'N/A';
        }
    }
    
    getVolumeText(volume) {
        switch (volume) {
            case 1: return 'Baixa';
            case 2: return 'Moderada';
            case 3: return 'Intensa';
            default: return 'N/A';
        }
    }
    
    // Métodos de utilidade
    centerOnRegion(regionId) {
        const region = this.regions.get(regionId);
        if (region) {
            this.map.setView(region.getLatLng(), 14);
        }
    }
    
    highlightRegion(regionId) {
        const region = this.regions.get(regionId);
        if (region) {
            region.setStyle({
                weight: 5,
                color: '#ffffff'
            });
            
            setTimeout(() => {
                region.setStyle({
                    weight: 2,
                    color: this.getRegionColor(region.regionData.status_cor || 'Verde')
                });
            }, 2000);
        }
    }
    
    addMarker(latlng, options = {}) {
        const marker = L.marker(latlng, options).addTo(this.map);
        return marker;
    }
    
    removeMarker(marker) {
        if (marker) {
            this.map.removeLayer(marker);
        }
    }
    
    fitBounds() {
        if (this.regions.size > 0) {
            const group = new L.featureGroup(Array.from(this.regions.values()));
            this.map.fitBounds(group.getBounds(), { padding: [20, 20] });
        }
    }
    
    destroy() {
        if (this.map) {
            this.map.remove();
            this.map = null;
        }
        this.regions.clear();
        this.markers.clear();
    }
}

// Exporta para uso global
window.MapController = MapController;