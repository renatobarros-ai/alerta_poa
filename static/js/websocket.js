/**
 * WebSocket Manager para conexão em tempo real
 */
class WebSocketManager {
    constructor(url) {
        this.url = url;
        this.socket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 1000;
        
        // Callbacks
        this.onStatusUpdate = null;
        this.onRegionAlert = null;
        this.onSystemNotification = null;
        this.onConnect = null;
        this.onDisconnect = null;
        this.onError = null;
        
        this.updateConnectionStatus('Desconectado', false);
    }
    
    connect() {
        try {
            this.socket = new WebSocket(this.url);
            
            this.socket.onopen = (event) => {
                console.log('WebSocket conectado');
                this.reconnectAttempts = 0;
                this.updateConnectionStatus('Conectado', true);
                
                if (this.onConnect) {
                    this.onConnect(event);
                }
            };
            
            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (error) {
                    console.error('Erro ao processar mensagem WebSocket:', error);
                }
            };
            
            this.socket.onclose = (event) => {
                console.log('WebSocket desconectado');
                this.updateConnectionStatus('Desconectado', false);
                
                if (this.onDisconnect) {
                    this.onDisconnect(event);
                }
                
                // Tenta reconectar automaticamente
                this.attemptReconnect();
            };
            
            this.socket.onerror = (error) => {
                console.error('Erro no WebSocket:', error);
                this.updateConnectionStatus('Erro', false);
                
                if (this.onError) {
                    this.onError(error);
                }
            };
            
        } catch (error) {
            console.error('Erro ao conectar WebSocket:', error);
            this.updateConnectionStatus('Erro', false);
        }
    }
    
    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }
    
    send(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(message));
        } else {
            console.warn('WebSocket não está conectado');
        }
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'initial_data':
            case 'status_update':
                if (this.onStatusUpdate && data.data) {
                    this.onStatusUpdate(data.data);
                }
                break;
                
            case 'region_alert':
                if (this.onRegionAlert) {
                    this.onRegionAlert(data);
                }
                break;
                
            case 'system_notification':
                if (this.onSystemNotification) {
                    this.onSystemNotification(data);
                } else {
                    // Mostra notificação padrão
                    this.showDefaultNotification(data);
                }
                break;
                
            case 'region_update':
                // Atualização específica de região
                if (this.onStatusUpdate && data.data) {
                    this.onStatusUpdate([data.data]);
                }
                break;
                
            case 'error':
                console.error('Erro do servidor WebSocket:', data.message);
                break;
                
            default:
                console.log('Mensagem WebSocket não reconhecida:', data);
        }
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            this.updateConnectionStatus(`Reconectando... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`, false);
            
            setTimeout(() => {
                console.log(`Tentativa de reconexão ${this.reconnectAttempts}`);
                this.connect();
            }, this.reconnectDelay * this.reconnectAttempts);
        } else {
            this.updateConnectionStatus('Falha na conexão', false);
            console.error('Número máximo de tentativas de reconexão atingido');
        }
    }
    
    requestUpdate() {
        this.send({
            type: 'request_update'
        });
    }
    
    subscribeToRegion(regionId) {
        this.send({
            type: 'subscribe_region',
            region_id: regionId
        });
    }
    
    updateConnectionStatus(status, isConnected) {
        const statusElement = document.getElementById('conexao-status');
        const textElement = document.getElementById('conexao-texto');
        
        if (statusElement && textElement) {
            textElement.textContent = status;
            
            statusElement.className = isConnected ? 
                'conexao-status badge conexao-online' : 
                'conexao-status badge conexao-offline';
        }
    }
    
    showDefaultNotification(data) {
        if (window.Utils && window.Utils.showAlert) {
            const alertType = data.level === 'error' ? 'danger' : 
                            data.level === 'warning' ? 'warning' : 'info';
            window.Utils.showAlert(data.message, alertType);
        }
    }
    
    // Método para verificar se está conectado
    isConnected() {
        return this.socket && this.socket.readyState === WebSocket.OPEN;
    }
    
    // Método para obter o estado da conexão
    getReadyState() {
        if (!this.socket) return 'CLOSED';
        
        switch (this.socket.readyState) {
            case WebSocket.CONNECTING: return 'CONNECTING';
            case WebSocket.OPEN: return 'OPEN';
            case WebSocket.CLOSING: return 'CLOSING';
            case WebSocket.CLOSED: return 'CLOSED';
            default: return 'UNKNOWN';
        }
    }
}

// Classe auxiliar para gerenciar múltiplas conexões WebSocket
class WebSocketPool {
    constructor() {
        this.connections = new Map();
    }
    
    add(name, url) {
        const manager = new WebSocketManager(url);
        this.connections.set(name, manager);
        return manager;
    }
    
    get(name) {
        return this.connections.get(name);
    }
    
    remove(name) {
        const manager = this.connections.get(name);
        if (manager) {
            manager.disconnect();
            this.connections.delete(name);
        }
    }
    
    disconnectAll() {
        this.connections.forEach(manager => manager.disconnect());
        this.connections.clear();
    }
    
    broadcastToAll(message) {
        this.connections.forEach(manager => {
            if (manager.isConnected()) {
                manager.send(message);
            }
        });
    }
}

// Exporta para uso global
window.WebSocketManager = WebSocketManager;
window.WebSocketPool = WebSocketPool;