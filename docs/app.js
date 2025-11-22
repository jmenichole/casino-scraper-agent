// Global state
let casinoData = [];
let currentTheme = 'light';

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    loadThemePreference();
    checkForSampleData();
}

// Event Listeners
function setupEventListeners() {
    // Theme toggle
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    
    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab || e.target.closest('.tab-btn').dataset.tab));
    });
    
    // Refresh data
    document.getElementById('refreshData').addEventListener('click', refreshData);
    
    // Search
    document.getElementById('searchInput').addEventListener('input', filterCasinos);
    
    // Sort
    document.getElementById('sortBy').addEventListener('change', sortCasinos);
    
    // File upload
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const uploadBox = document.querySelector('.upload-box');
    
    browseBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileUpload);
    
    // Drag and drop
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = 'var(--primary-color)';
    });
    
    uploadBox.addEventListener('dragleave', () => {
        uploadBox.style.borderColor = 'var(--border-color)';
    });
    
    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.style.borderColor = 'var(--border-color)';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    // Sample data button
    document.getElementById('loadSampleData').addEventListener('click', loadSampleData);
    
    // Modal
    const modal = document.getElementById('casinoModal');
    const closeBtn = modal.querySelector('.close');
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Theme Management
function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme();
    localStorage.setItem('theme', currentTheme);
}

function applyTheme() {
    document.documentElement.setAttribute('data-theme', currentTheme);
    const icon = document.querySelector('#themeToggle i');
    icon.className = currentTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}

function loadThemePreference() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        currentTheme = savedTheme;
        applyTheme();
    }
}

// Tab Navigation
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`.tab-btn[data-tab="${tabName}"]`).classList.add('active');
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
}

// Data Loading
function handleFileUpload(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    if (file.type !== 'application/json') {
        showUploadStatus('Please upload a valid JSON file', 'error');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const data = JSON.parse(e.target.result);
            loadCasinoData(data);
            showUploadStatus(`Successfully loaded ${data.length} casino(s)`, 'success');
            
            // Save to localStorage
            localStorage.setItem('casinoData', JSON.stringify(data));
            
            // Switch to dashboard
            setTimeout(() => switchTab('dashboard'), 1000);
        } catch (error) {
            showUploadStatus('Error parsing JSON file: ' + error.message, 'error');
        }
    };
    reader.readAsText(file);
}

function showUploadStatus(message, type) {
    const statusEl = document.getElementById('uploadStatus');
    statusEl.textContent = message;
    statusEl.className = `upload-status ${type}`;
}

function loadSampleData() {
    // Sample casino data
    const sampleData = [
        {
            "name": "Royal Fortune Casino",
            "url": "https://www.royalfortune-casino.example.com/",
            "description": "A premium online casino offering a wide selection of games with top-tier security and fast withdrawals.",
            "licenses": [
                {
                    "authority": "Malta Gaming Authority",
                    "license_number": "MGA/B2C/123/2020",
                    "jurisdiction": "Malta",
                    "verified": true,
                    "verification_date": "2024-01-15T00:00:00Z"
                },
                {
                    "authority": "UK Gambling Commission",
                    "license_number": "UKGC-54321",
                    "jurisdiction": "United Kingdom",
                    "verified": true,
                    "verification_date": "2024-01-15T00:00:00Z"
                }
            ],
            "rtp_info": [
                {
                    "game_name": "Starburst",
                    "rtp_percentage": 96.1,
                    "game_category": "Slots",
                    "provider": "NetEnt"
                },
                {
                    "game_name": "Book of Dead",
                    "rtp_percentage": 96.21,
                    "game_category": "Slots",
                    "provider": "Play'n GO"
                },
                {
                    "game_name": "European Roulette",
                    "rtp_percentage": 97.3,
                    "game_category": "Table Games",
                    "provider": "Evolution Gaming"
                }
            ],
            "fairness": [
                {
                    "testing_agency": "eCOGRA",
                    "certification": "Safe and Fair",
                    "certified": true,
                    "last_audit_date": "2024-01-01T00:00:00Z"
                }
            ],
            "providers": [
                {
                    "name": "NetEnt",
                    "games_count": 150,
                    "popular_games": ["Starburst", "Gonzo's Quest"]
                },
                {
                    "name": "Microgaming",
                    "games_count": 200,
                    "popular_games": ["Mega Moolah", "Immortal Romance"]
                },
                {
                    "name": "Evolution Gaming",
                    "games_count": 50,
                    "popular_games": ["Lightning Roulette", "Dream Catcher"]
                },
                {
                    "name": "Play'n GO",
                    "games_count": 100,
                    "popular_games": []
                }
            ],
            "security": {
                "ssl_certificate": true,
                "encryption_type": "256-bit SSL",
                "two_factor_auth": true,
                "responsible_gambling_tools": ["Self-Exclusion", "Deposit Limits", "Time Limits", "Reality Check"],
                "data_protection_compliance": ["GDPR", "PCI DSS"]
            },
            "withdrawal_methods": [
                {
                    "method": "Visa",
                    "min_amount": 20.0,
                    "max_amount": 5000.0,
                    "processing_time": "1-3 days",
                    "fees": "Free"
                },
                {
                    "method": "PayPal",
                    "min_amount": 10.0,
                    "max_amount": 10000.0,
                    "processing_time": "0-24 hours",
                    "fees": "Free"
                },
                {
                    "method": "Bank Transfer",
                    "min_amount": 100.0,
                    "max_amount": 50000.0,
                    "processing_time": "3-5 days",
                    "fees": "Free"
                }
            ],
            "reviews": [
                {
                    "source": "TrustPilot",
                    "rating": 4.5,
                    "review_count": 1250,
                    "positive_aspects": ["Fast withdrawals", "Great game selection", "Professional support"],
                    "negative_aspects": ["Limited crypto options"],
                    "review_date": "2024-01-20T00:00:00Z"
                }
            ],
            "collection_date": "2024-11-22T01:00:00Z",
            "data_completeness_score": 100.0
        },
        {
            "name": "Lucky Star Casino",
            "url": "https://www.luckystar-casino.example.com/",
            "description": "Experience the thrill of gaming with generous bonuses and 24/7 customer support.",
            "licenses": [
                {
                    "authority": "Curacao eGaming",
                    "license_number": "CEG-789456",
                    "jurisdiction": "Curacao",
                    "verified": false
                }
            ],
            "rtp_info": [
                {
                    "game_name": "Mega Fortune",
                    "rtp_percentage": 96.0,
                    "game_category": "Slots",
                    "provider": "NetEnt"
                },
                {
                    "game_name": "Blackjack Classic",
                    "rtp_percentage": 99.5,
                    "game_category": "Table Games",
                    "provider": "Microgaming"
                }
            ],
            "fairness": [
                {
                    "testing_agency": "iTech Labs",
                    "certification": "RNG Certified",
                    "certified": true,
                    "last_audit_date": "2024-03-15T00:00:00Z"
                }
            ],
            "providers": [
                {
                    "name": "NetEnt",
                    "games_count": 120,
                    "popular_games": ["Mega Fortune"]
                },
                {
                    "name": "Microgaming",
                    "games_count": 180,
                    "popular_games": ["Blackjack Classic"]
                },
                {
                    "name": "Pragmatic Play",
                    "games_count": 95,
                    "popular_games": []
                }
            ],
            "security": {
                "ssl_certificate": true,
                "encryption_type": "128-bit SSL",
                "two_factor_auth": false,
                "responsible_gambling_tools": ["Self-Exclusion", "Deposit Limits"],
                "data_protection_compliance": ["GDPR"]
            },
            "withdrawal_methods": [
                {
                    "method": "Visa",
                    "min_amount": 30.0,
                    "max_amount": 3000.0,
                    "processing_time": "2-5 days",
                    "fees": "Free"
                },
                {
                    "method": "Bitcoin",
                    "min_amount": 50.0,
                    "max_amount": 10000.0,
                    "processing_time": "0-2 hours",
                    "fees": "Network fees apply"
                }
            ],
            "reviews": [
                {
                    "source": "AskGamblers",
                    "rating": 4.0,
                    "review_count": 650,
                    "positive_aspects": ["Good bonuses", "Fast crypto withdrawals"],
                    "negative_aspects": ["Limited payment options"],
                    "review_date": "2024-02-10T00:00:00Z"
                }
            ],
            "collection_date": "2024-11-22T02:00:00Z",
            "data_completeness_score": 85.7
        }
    ];
    
    loadCasinoData(sampleData);
    localStorage.setItem('casinoData', JSON.stringify(sampleData));
    showUploadStatus('Sample data loaded successfully!', 'success');
    setTimeout(() => switchTab('dashboard'), 1000);
}

function checkForSampleData() {
    const savedData = localStorage.getItem('casinoData');
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            loadCasinoData(data);
        } catch (error) {
            console.error('Error loading saved data:', error);
        }
    }
}

function loadCasinoData(data) {
    casinoData = Array.isArray(data) ? data : [data];
    updateDashboard();
    updateCasinosList();
}

function refreshData() {
    if (casinoData.length > 0) {
        updateDashboard();
        updateCasinosList();
        
        // Show feedback
        const btn = document.getElementById('refreshData');
        const icon = btn.querySelector('i');
        icon.classList.add('fa-spin');
        setTimeout(() => icon.classList.remove('fa-spin'), 1000);
    }
}

// Dashboard Updates
function updateDashboard() {
    if (casinoData.length === 0) return;
    
    // Calculate stats
    const totalCasinos = casinoData.length;
    const totalLicenses = casinoData.reduce((sum, casino) => sum + (casino.licenses?.length || 0), 0);
    const totalProviders = [...new Set(casinoData.flatMap(casino => 
        (casino.providers || []).map(p => p.name)
    ))].length;
    
    const avgRating = casinoData.reduce((sum, casino) => {
        const reviews = casino.reviews || [];
        const avgCasinoRating = reviews.length > 0 
            ? reviews.reduce((s, r) => s + r.rating, 0) / reviews.length 
            : 0;
        return sum + avgCasinoRating;
    }, 0) / casinoData.length;
    
    const avgRtp = casinoData.reduce((sum, casino) => {
        const rtpInfo = casino.rtp_info || [];
        const avgCasinoRtp = rtpInfo.length > 0 
            ? rtpInfo.reduce((s, r) => s + r.rtp_percentage, 0) / rtpInfo.length 
            : 0;
        return sum + avgCasinoRtp;
    }, 0) / casinoData.length;
    
    const avgCompleteness = casinoData.reduce((sum, casino) => 
        sum + (casino.data_completeness_score || 0), 0) / casinoData.length;
    
    // Update stat cards
    document.getElementById('totalCasinos').textContent = totalCasinos;
    document.getElementById('totalLicenses').textContent = totalLicenses;
    document.getElementById('totalProviders').textContent = totalProviders;
    document.getElementById('avgRating').textContent = avgRating.toFixed(1);
    document.getElementById('avgRtp').textContent = avgRtp.toFixed(1) + '%';
    document.getElementById('avgCompleteness').textContent = avgCompleteness.toFixed(0) + '%';
    
    // Update charts
    updateTopProvidersChart();
    updateJurisdictionsChart();
    updateRecentCollections();
}

function updateTopProvidersChart() {
    const providerCounts = {};
    
    casinoData.forEach(casino => {
        (casino.providers || []).forEach(provider => {
            providerCounts[provider.name] = (providerCounts[provider.name] || 0) + 1;
        });
    });
    
    const sortedProviders = Object.entries(providerCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    const maxCount = Math.max(...sortedProviders.map(p => p[1]));
    
    const chartHtml = `
        <div class="bar-chart">
            ${sortedProviders.map(([name, count]) => `
                <div class="bar-item">
                    <div class="bar-label">${name}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: ${(count / maxCount) * 100}%"></div>
                    </div>
                    <div class="bar-value">${count}</div>
                </div>
            `).join('')}
        </div>
    `;
    
    document.getElementById('topProvidersChart').innerHTML = chartHtml;
}

function updateJurisdictionsChart() {
    const jurisdictionCounts = {};
    
    casinoData.forEach(casino => {
        (casino.licenses || []).forEach(license => {
            jurisdictionCounts[license.jurisdiction] = (jurisdictionCounts[license.jurisdiction] || 0) + 1;
        });
    });
    
    const sortedJurisdictions = Object.entries(jurisdictionCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    const maxCount = Math.max(...sortedJurisdictions.map(j => j[1]));
    
    const chartHtml = `
        <div class="bar-chart">
            ${sortedJurisdictions.map(([name, count]) => `
                <div class="bar-item">
                    <div class="bar-label">${name}</div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: ${(count / maxCount) * 100}%"></div>
                    </div>
                    <div class="bar-value">${count}</div>
                </div>
            `).join('')}
        </div>
    `;
    
    document.getElementById('jurisdictionsChart').innerHTML = chartHtml;
}

function updateRecentCollections() {
    const recentCasinos = [...casinoData]
        .sort((a, b) => new Date(b.collection_date) - new Date(a.collection_date))
        .slice(0, 5);
    
    const timelineHtml = recentCasinos.map(casino => `
        <div class="timeline-item">
            <h4>${casino.name}</h4>
            <p>Collected on ${new Date(casino.collection_date).toLocaleString()}</p>
            <p>Completeness: ${casino.data_completeness_score?.toFixed(0) || 0}%</p>
        </div>
    `).join('');
    
    document.getElementById('recentCollections').innerHTML = timelineHtml || '<p>No recent collections</p>';
}

// Casinos List
function updateCasinosList() {
    const grid = document.getElementById('casinosGrid');
    
    if (casinoData.length === 0) {
        grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-secondary);">No casino data loaded. Upload a JSON file or load sample data.</p>';
        return;
    }
    
    const cardsHtml = casinoData.map((casino, index) => createCasinoCard(casino, index)).join('');
    grid.innerHTML = cardsHtml;
    
    // Add click listeners
    document.querySelectorAll('.casino-card').forEach((card, index) => {
        card.addEventListener('click', () => showCasinoDetails(casinoData[index]));
    });
}

function createCasinoCard(casino, index) {
    const avgRating = casino.reviews?.length > 0 
        ? (casino.reviews.reduce((s, r) => s + r.rating, 0) / casino.reviews.length).toFixed(1)
        : 'N/A';
    
    const avgRtp = casino.rtp_info?.length > 0 
        ? (casino.rtp_info.reduce((s, r) => s + r.rtp_percentage, 0) / casino.rtp_info.length).toFixed(1)
        : 'N/A';
    
    const hasSSL = casino.security?.ssl_certificate;
    const has2FA = casino.security?.two_factor_auth;
    
    return `
        <div class="casino-card" data-index="${index}">
            <div class="casino-card-header">
                <h3>${casino.name}</h3>
                <a href="${casino.url}" class="url" target="_blank" onclick="event.stopPropagation()">
                    ${casino.url}
                </a>
            </div>
            <div class="casino-card-body">
                <p>${casino.description || 'No description available'}</p>
                
                <div class="casino-stats">
                    <div class="casino-stat">
                        <i class="fas fa-certificate"></i>
                        <span>${casino.licenses?.length || 0} Licenses</span>
                    </div>
                    <div class="casino-stat">
                        <i class="fas fa-gamepad"></i>
                        <span>${casino.providers?.length || 0} Providers</span>
                    </div>
                    <div class="casino-stat">
                        <i class="fas fa-star"></i>
                        <span>${avgRating} Rating</span>
                    </div>
                    <div class="casino-stat">
                        <i class="fas fa-percent"></i>
                        <span>${avgRtp}% RTP</span>
                    </div>
                </div>
                
                <div class="casino-badges">
                    ${hasSSL ? '<span class="badge badge-success">SSL Secured</span>' : ''}
                    ${has2FA ? '<span class="badge badge-success">2FA</span>' : ''}
                    ${casino.data_completeness_score >= 90 
                        ? '<span class="badge badge-success">High Quality</span>' 
                        : casino.data_completeness_score >= 70 
                            ? '<span class="badge badge-warning">Good Quality</span>'
                            : '<span class="badge badge-primary">Basic Info</span>'}
                </div>
            </div>
        </div>
    `;
}

function filterCasinos() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const cards = document.querySelectorAll('.casino-card');
    
    cards.forEach((card, index) => {
        const casino = casinoData[index];
        const matchesSearch = 
            casino.name.toLowerCase().includes(searchTerm) ||
            casino.description?.toLowerCase().includes(searchTerm) ||
            casino.url.toLowerCase().includes(searchTerm);
        
        card.style.display = matchesSearch ? 'block' : 'none';
    });
}

function sortCasinos() {
    const sortBy = document.getElementById('sortBy').value;
    
    const sorted = [...casinoData].sort((a, b) => {
        switch (sortBy) {
            case 'name':
                return a.name.localeCompare(b.name);
            case 'rating':
                const avgA = a.reviews?.length > 0 
                    ? a.reviews.reduce((s, r) => s + r.rating, 0) / a.reviews.length 
                    : 0;
                const avgB = b.reviews?.length > 0 
                    ? b.reviews.reduce((s, r) => s + r.rating, 0) / b.reviews.length 
                    : 0;
                return avgB - avgA;
            case 'completeness':
                return (b.data_completeness_score || 0) - (a.data_completeness_score || 0);
            case 'date':
                return new Date(b.collection_date) - new Date(a.collection_date);
            default:
                return 0;
        }
    });
    
    casinoData = sorted;
    updateCasinosList();
}

// Casino Details Modal
function showCasinoDetails(casino) {
    const modal = document.getElementById('casinoModal');
    const detailsEl = document.getElementById('casinoDetails');
    
    const avgRating = casino.reviews?.length > 0 
        ? (casino.reviews.reduce((s, r) => s + r.rating, 0) / casino.reviews.length).toFixed(1)
        : 'N/A';
    
    detailsEl.innerHTML = `
        <h2>${casino.name}</h2>
        <p><a href="${casino.url}" target="_blank">${casino.url}</a></p>
        <p style="color: var(--text-secondary); margin-bottom: 2rem;">${casino.description || 'No description available'}</p>
        
        <div style="display: grid; gap: 1.5rem;">
            <div class="config-card">
                <h3><i class="fas fa-certificate"></i> Licenses (${casino.licenses?.length || 0})</h3>
                ${casino.licenses?.length > 0 ? `
                    <ul style="list-style: none; padding: 0;">
                        ${casino.licenses.map(l => `
                            <li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                                <strong>${l.authority}</strong> - ${l.jurisdiction}
                                ${l.license_number ? `<br><small>License: ${l.license_number}</small>` : ''}
                                ${l.verified ? '<br><span class="badge badge-success">Verified</span>' : ''}
                            </li>
                        `).join('')}
                    </ul>
                ` : '<p style="color: var(--text-secondary);">No license information available</p>'}
            </div>
            
            <div class="config-card">
                <h3><i class="fas fa-gamepad"></i> Game Providers (${casino.providers?.length || 0})</h3>
                ${casino.providers?.length > 0 ? `
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                        ${casino.providers.map(p => `
                            <span class="badge badge-primary">${p.name} ${p.games_count ? `(${p.games_count})` : ''}</span>
                        `).join('')}
                    </div>
                ` : '<p style="color: var(--text-secondary);">No provider information available</p>'}
            </div>
            
            <div class="config-card">
                <h3><i class="fas fa-percent"></i> RTP Information</h3>
                ${casino.rtp_info?.length > 0 ? `
                    <ul style="list-style: none; padding: 0;">
                        ${casino.rtp_info.slice(0, 5).map(r => `
                            <li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                                <strong>${r.game_name}</strong> - ${r.rtp_percentage}%
                                <br><small>${r.provider || 'Unknown'} | ${r.game_category || 'N/A'}</small>
                            </li>
                        `).join('')}
                        ${casino.rtp_info.length > 5 ? `<li style="padding: 0.5rem 0; color: var(--text-secondary);">...and ${casino.rtp_info.length - 5} more</li>` : ''}
                    </ul>
                ` : '<p style="color: var(--text-secondary);">No RTP information available</p>'}
            </div>
            
            <div class="config-card">
                <h3><i class="fas fa-shield-alt"></i> Security</h3>
                ${casino.security ? `
                    <div class="casino-stats">
                        <div class="casino-stat">
                            <i class="fas ${casino.security.ssl_certificate ? 'fa-check-circle text-success' : 'fa-times-circle text-danger'}"></i>
                            <span>SSL Certificate</span>
                        </div>
                        <div class="casino-stat">
                            <i class="fas ${casino.security.two_factor_auth ? 'fa-check-circle text-success' : 'fa-times-circle text-danger'}"></i>
                            <span>2FA Available</span>
                        </div>
                    </div>
                    ${casino.security.encryption_type ? `<p><strong>Encryption:</strong> ${casino.security.encryption_type}</p>` : ''}
                    ${casino.security.responsible_gambling_tools?.length > 0 ? `
                        <p><strong>Responsible Gambling:</strong></p>
                        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                            ${casino.security.responsible_gambling_tools.map(t => `<span class="badge badge-success">${t}</span>`).join('')}
                        </div>
                    ` : ''}
                ` : '<p style="color: var(--text-secondary);">No security information available</p>'}
            </div>
            
            <div class="config-card">
                <h3><i class="fas fa-money-bill-wave"></i> Withdrawal Methods</h3>
                ${casino.withdrawal_methods?.length > 0 ? `
                    <ul style="list-style: none; padding: 0;">
                        ${casino.withdrawal_methods.map(w => `
                            <li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                                <strong>${w.method}</strong>
                                <br><small>${w.min_amount ? `Min: $${w.min_amount}` : ''} 
                                ${w.max_amount ? `| Max: $${w.max_amount}` : ''}
                                ${w.processing_time ? `| ${w.processing_time}` : ''}</small>
                            </li>
                        `).join('')}
                    </ul>
                ` : '<p style="color: var(--text-secondary);">No withdrawal information available</p>'}
            </div>
            
            <div class="config-card">
                <h3><i class="fas fa-star"></i> Reviews (Avg: ${avgRating})</h3>
                ${casino.reviews?.length > 0 ? `
                    <ul style="list-style: none; padding: 0;">
                        ${casino.reviews.map(r => `
                            <li style="padding: 1rem 0; border-bottom: 1px solid var(--border-color);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                    <strong>${r.source}</strong>
                                    <span>${'⭐'.repeat(Math.round(r.rating))} ${r.rating}/5</span>
                                </div>
                                ${r.review_count ? `<small>${r.review_count} reviews</small><br>` : ''}
                                ${r.positive_aspects?.length > 0 ? `
                                    <p style="color: var(--success-color); margin-top: 0.5rem;">
                                        <strong>Pros:</strong> ${r.positive_aspects.join(', ')}
                                    </p>
                                ` : ''}
                                ${r.negative_aspects?.length > 0 ? `
                                    <p style="color: var(--danger-color);">
                                        <strong>Cons:</strong> ${r.negative_aspects.join(', ')}
                                    </p>
                                ` : ''}
                            </li>
                        `).join('')}
                    </ul>
                ` : '<p style="color: var(--text-secondary);">No review information available</p>'}
            </div>
            
            <div class="config-card">
                <h3><i class="fas fa-info-circle"></i> Collection Info</h3>
                <p><strong>Collection Date:</strong> ${new Date(casino.collection_date).toLocaleString()}</p>
                <p><strong>Data Completeness:</strong> ${casino.data_completeness_score?.toFixed(0) || 0}%</p>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}
