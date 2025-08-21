// Demo Interactive JavaScript for DDoS AI Detection System

document.addEventListener('DOMContentLoaded', function() {
    console.log('Demo Interactive JS loaded');
    
    // Make sidebar collapsible
    setupSidebar();
    
    // Setup interactive features based on current page
    setupPageFeatures();
    
    // Setup real-time updates
    setupRealTimeUpdates();
});

function setupSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }
    
    // Add click outside to close functionality
    document.addEventListener('click', function(e) {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('collapsed');
        }
    });
}

function setupPageFeatures() {
    const currentPath = window.location.pathname;
    
    if (currentPath.includes('screen')) {
        setupModelAnalysis();
    } else if (currentPath.includes('dataset_res')) {
        setupDatasetAnalysis();
    } else if (currentPath.includes('traffic-log')) {
        setupTrafficMonitoring();
    } else if (currentPath.includes('index')) {
        setupDashboard();
    }
}

function setupModelAnalysis() {
    // Add interactive model comparison
    const modelCards = document.querySelectorAll('.model-card');
    
    modelCards.forEach(card => {
        card.addEventListener('click', function() {
            showModelDetails(this.dataset.model);
        });
    });
    
    // Add fake performance charts
    addPerformanceCharts();
}

function setupDatasetAnalysis() {
    // Add interactive dataset visualization
    addDatasetCharts();
    
    // Make attack type distribution clickable
    const attackTypes = document.querySelectorAll('.attack-type');
    attackTypes.forEach(type => {
        type.addEventListener('click', function() {
            showAttackDetails(this.dataset.type);
        });
    });
}

function setupTrafficMonitoring() {
    // Add search functionality
    const searchForm = document.querySelector('#search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            performSearch();
        });
    }
    
    // Add export functionality
    const exportBtn = document.querySelector('#export-csv');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            exportTrafficData();
        });
    }
    
    // Add delete functionality
    const deleteBtn = document.querySelector('#delete-selected');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function() {
            deleteSelectedLogs();
        });
    }
}

function setupDashboard() {
    // Add real-time stats updates
    updateDashboardStats();
    
    // Add alert trend visualization
    addAlertTrendChart();
}

function addPerformanceCharts() {
    const chartContainer = document.querySelector('#performance-chart');
    if (!chartContainer) return;
    
    // Simulate chart rendering
    simulateChartRendering(chartContainer, {
        labels: ['CNN', 'LSTM', 'CNN-LSTM-Attention'],
        datasets: [{
            label: 'Accuracy (%)',
            data: [94.2, 96.1, 97.8],
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            borderColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            borderWidth: 2
        }]
    });
    
    // Add attack detection chart
    const attackChartContainer = document.querySelector('#attack-detection-chart');
    if (attackChartContainer) {
        simulateAttackDetectionChart(attackChartContainer);
    }
}

function addDatasetCharts() {
    const chartContainer = document.querySelector('#dataset-chart');
    if (!chartContainer) return;
    
    // Create fake dataset visualization
    const chartData = {
        total: 15000,
        normal: 12000,
        attacks: 3000,
        distribution: {
            'DDoS': 1200,
            'Port Scan': 800,
            'Botnet': 600,
            'Brute Force': 400
        }
    };
    
    // Render fake chart
    renderDatasetChart(chartContainer, chartData);
}

function addAlertTrendChart() {
    const chartContainer = document.querySelector('#alert-trend');
    if (!chartContainer) return;
    
    // Create fake trend data
    const trendData = {
        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
        datasets: [{
            label: 'Alerts',
            data: [5, 12, 8, 15, 22, 18],
            borderColor: '#FF6384',
            backgroundColor: 'rgba(255, 99, 132, 0.1)',
            tension: 0.4
        }]
    };
    
    // Simulate trend chart
    simulateTrendChart(chartContainer, trendData);
}

function performSearch() {
    const sourceIP = document.querySelector('#source-ip').value;
    const threatLevel = document.querySelector('#threat-level').value;
    
    // Simulate search results
    const results = simulateSearch(sourceIP, threatLevel);
    displaySearchResults(results);
}

function exportTrafficData() {
    // Simulate CSV export
    const csvContent = generateFakeCSV();
    downloadCSV(csvContent, 'traffic_logs.csv');
}

function deleteSelectedLogs() {
    // Simulate deletion
    const selectedLogs = document.querySelectorAll('input[name="log-select"]:checked');
    if (selectedLogs.length > 0) {
        selectedLogs.forEach(log => {
            log.closest('tr').remove();
        });
        showNotification('Selected logs deleted successfully');
    } else {
        showNotification('Please select logs to delete');
    }
}

function updateDashboardStats() {
    // Simulate real-time stats updates
    setInterval(() => {
        const stats = generateFakeStats();
        updateStatsDisplay(stats);
    }, 5000);
}

function setupRealTimeUpdates() {
    // Simulate real-time traffic updates
    setInterval(() => {
        fetch('/api/live-traffic')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    addNewTrafficEntry(data.new_traffic);
                }
            })
            .catch(error => {
                console.log('Demo mode: Simulating live traffic update');
                addNewTrafficEntry(generateFakeTraffic());
            });
    }, 8000);
}

// Helper functions
function showModelDetails(model) {
    const details = {
        'cnn': 'Convolutional Neural Network - Excellent at pattern recognition in network packets',
        'lstm': 'Long Short-Term Memory - Great for sequential traffic analysis',
        'cnn_lstm_attention': 'Hybrid model with attention mechanism - Best overall performance'
    };
    
    showNotification(details[model] || 'Model details not available');
}

function showAttackDetails(attackType) {
    const details = {
        'DDoS': 'Distributed Denial of Service - Multiple sources overwhelming target',
        'Port Scan': 'Systematic port scanning to find vulnerabilities',
        'Botnet': 'Network of compromised devices under attacker control',
        'Brute Force': 'Repeated login attempts to gain unauthorized access'
    };
    
    showNotification(details[attackType] || 'Attack details not available');
}

function simulateSearch(sourceIP, threatLevel) {
    // Return fake search results
    return [
        {
            id: Math.floor(Math.random() * 1000),
            created_time: new Date().toLocaleString(),
            source_ip: sourceIP || '192.168.1.100',
            dest_ip: '10.0.0.50',
            threat_level: threatLevel || 'High',
            attack_type: 'DDoS'
        }
    ];
}

function displaySearchResults(results) {
    const resultsContainer = document.querySelector('#search-results');
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = results.map(result => `
        <div class="search-result">
            <strong>${result.attack_type}</strong> from ${result.source_ip} 
            (${result.threat_level} risk) - ${result.created_time}
        </div>
    `).join('');
}

function generateFakeCSV() {
    return `ID,Time,Source IP,Dest IP,Threat Level,Attack Type
1,2025-08-21 15:30:22,192.168.1.100,10.0.0.50,High,DDoS
2,2025-08-21 15:29:15,203.45.67.89,10.0.0.51,Medium,Brute Force
3,2025-08-21 15:28:45,98.76.54.32,10.0.0.52,Low,Port Scan`;
}

function downloadCSV(content, filename) {
    const blob = new Blob([content], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
    showNotification('CSV exported successfully');
}

function generateFakeStats() {
    return {
        total_alerts: Math.floor(Math.random() * 50) + 20,
        high_risk: Math.floor(Math.random() * 10) + 5,
        medium_risk: Math.floor(Math.random() * 15) + 8,
        low_risk: Math.floor(Math.random() * 25) + 10
    };
}

function updateStatsDisplay(stats) {
    Object.keys(stats).forEach(key => {
        const element = document.querySelector(`#${key.replace('_', '-')}`);
        if (element) {
            element.textContent = stats[key];
        }
    });
}

function generateFakeTraffic() {
    const attackTypes = ['Normal', 'DDoS', 'Port Scan', 'Botnet', 'Brute Force'];
    const threatLevels = ['Low', 'Medium', 'High'];
    
    return {
        id: Math.floor(Math.random() * 10000),
        created_time: new Date().toLocaleString(),
        source_ip: `${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
        dest_ip: `10.0.0.${Math.floor(Math.random() * 100)}`,
        attack_type: attackTypes[Math.floor(Math.random() * attackTypes.length)],
        threat_level: threatLevels[Math.floor(Math.random() * threatLevels.length)]
    };
}

function addNewTrafficEntry(traffic) {
    const tableBody = document.querySelector('#traffic-table tbody');
    if (!tableBody) return;
    
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td><input type="checkbox" name="log-select"></td>
        <td>${traffic.created_time}</td>
        <td>${traffic.source_ip}</td>
        <td>${traffic.dest_ip}</td>
        <td>${traffic.attack_type}</td>
        <td><span class="badge badge-${traffic.threat_level.toLowerCase()}">${traffic.threat_level}</span></td>
        <td><button class="btn btn-sm btn-info">View</button></td>
    `;
    
    tableBody.insertBefore(newRow, tableBody.firstChild);
    
    // Remove old entries if too many
    if (tableBody.children.length > 20) {
        tableBody.removeChild(tableBody.lastChild);
    }
    
    showNotification(`New ${traffic.threat_level} risk traffic detected from ${traffic.source_ip}`);
}

function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 15px;
        border-radius: 5px;
        z-index: 1000;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Chart simulation functions
function simulateChartRendering(container, data) {
    container.innerHTML = `
        <div class="chart-placeholder">
            <h4>Model Performance Comparison</h4>
            <div class="chart-bars">
                ${data.datasets[0].data.map((value, index) => `
                    <div class="chart-bar" style="height: ${value * 2}px; background: ${data.datasets[0].backgroundColor[index]}">
                        <span class="bar-label">${data.labels[index]}</span>
                        <span class="bar-value">${value}%</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function simulateAttackDetectionChart(container) {
    container.innerHTML = `
        <div class="chart-placeholder">
            <h4>Attack Detection Rates by Type</h4>
            <div class="attack-rates">
                <div class="attack-rate-item">
                    <span class="attack-name">Normal Traffic</span>
                    <div class="rate-bar">
                        <div class="rate-fill" style="width: 98.5%; background: #28a745;"></div>
                        <span class="rate-value">98.5%</span>
                    </div>
                </div>
                <div class="attack-rate-item">
                    <span class="attack-name">DDoS Attacks</span>
                    <div class="rate-bar">
                        <div class="rate-fill" style="width: 96.2%; background: #dc3545;"></div>
                        <span class="rate-value">96.2%</span>
                    </div>
                </div>
                <div class="attack-rate-item">
                    <span class="attack-name">Port Scans</span>
                    <div class="rate-bar">
                        <div class="rate-fill" style="width: 94.8%; background: #ffc107;"></div>
                        <span class="rate-value">94.8%</span>
                    </div>
                </div>
                <div class="attack-rate-item">
                    <span class="attack-name">Botnet Activity</span>
                    <div class="rate-bar">
                        <div class="rate-fill" style="width: 97.1%; background: #17a2b8;"></div>
                        <span class="rate-value">97.1%</span>
                    </div>
                </div>
                <div class="attack-rate-item">
                    <span class="attack-name">Brute Force</span>
                    <div class="rate-bar">
                        <div class="rate-fill" style="width: 93.5%; background: #6f42c1;"></div>
                        <span class="rate-value">93.5%</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function renderDatasetChart(container, data) {
    container.innerHTML = `
        <div class="dataset-visualization">
            <h4>Dataset Overview</h4>
            <div class="dataset-stats">
                <div class="stat-item">
                    <span class="stat-number">${data.total.toLocaleString()}</span>
                    <span class="stat-label">Total Samples</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${data.normal.toLocaleString()}</span>
                    <span class="stat-label">Normal Traffic</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${data.attacks.toLocaleString()}</span>
                    <span class="stat-label">Attack Samples</span>
                </div>
            </div>
            <div class="attack-distribution">
                <h5>Attack Type Distribution</h5>
                ${Object.entries(data.distribution).map(([type, count]) => `
                    <div class="attack-type" data-type="${type}">
                        <span class="attack-name">${type}</span>
                        <span class="attack-count">${count}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    // Add dataset stats chart
    const statsContainer = document.querySelector('#dataset-stats');
    if (statsContainer) {
        renderDatasetStatsChart(statsContainer, data);
    }
}

function simulateTrendChart(container, data) {
    container.innerHTML = `
        <div class="trend-chart">
            <h4>Alert Trend (24 Hours)</h4>
            <div class="trend-line">
                ${data.datasets[0].data.map((value, index) => `
                    <div class="trend-point" style="left: ${(index / (data.labels.length - 1)) * 100}%; bottom: ${(value / 25) * 100}%">
                        <span class="point-value">${value}</span>
                    </div>
                `).join('')}
            </div>
            <div class="trend-labels">
                ${data.labels.map(label => `<span class="point-label">${label}</span>`).join('')}
            </div>
        </div>
    `;
}

function renderDatasetStatsChart(container, data) {
    container.innerHTML = `
        <div class="dataset-stats-chart">
            <h4>Dataset Statistics</h4>
            <div class="stats-overview">
                <div class="stat-circle">
                    <div class="circle-progress" style="background: conic-gradient(#007bff 0deg ${(data.model_accuracy / 100) * 360}deg, #e9ecef 0deg);">
                        <div class="circle-center">
                            <span class="accuracy-value">${data.model_accuracy}%</span>
                            <span class="accuracy-label">Accuracy</span>
                        </div>
                    </div>
                </div>
                <div class="feature-importance">
                    <h5>Top Features</h5>
                    ${data.feature_importance.map((feature, index) => `
                        <div class="feature-item">
                            <span class="feature-rank">${index + 1}</span>
                            <span class="feature-name">${feature}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}
