let currentUser = null;
let currentServer = null;
let userServers = [];
let botStats = {};

document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    loadBotStats();
});

async function checkAuth() {
    try {
        const res = await fetch('/api/session');
        const data = await res.json();
        
        if (data.authenticated) {
            currentUser = data.user;
            userServers = data.servers || [];
            showDashboard();
        } else {
            showLandingPage();
        }
    } catch (e) {
        console.log('Auth check failed:', e);
        showLandingPage();
    }
}

async function loadBotStats() {
    try {
        const res = await fetch('/api/stats');
        botStats = await res.json();
        
        document.getElementById('serverCount').textContent = botStats.servers || 0;
        document.getElementById('userCount').textContent = botStats.members || 0;
        document.getElementById('statServers').textContent = botStats.servers || 0;
        document.getElementById('statUsers').textContent = botStats.members || 0;
    } catch (e) {
        console.log('Stats load failed:', e);
    }
}

function showLandingPage() {
    document.getElementById('landing-page').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
}

function showDashboard() {
    document.getElementById('landing-page').style.display = 'none';
    document.getElementById('dashboard').style.display = 'flex';
    
    // Update user info
    if (currentUser) {
        document.getElementById('userName').textContent = currentUser.username || 'Kullanıcı';
        document.getElementById('userTag').textContent = currentUser.tag || '#0000';
        if (currentUser.avatar) {
            document.getElementById('userAvatar').src = currentUser.avatar;
        }
    }
    
    // Update server list
    document.getElementById('serverCountList').textContent = userServers.length;
    renderServerList();
    
    // Select first server if available
    if (userServers.length > 0) {
        selectServer(userServers[0].id);
    }
}

function renderServerList() {
    const container = document.getElementById('serverList');
    container.innerHTML = '';
    
    userServers.forEach(server => {
        const item = document.createElement('button');
        item.className = 'server-item' + (currentServer && currentServer.id === server.id ? ' active' : '');
        item.onclick = () => selectServer(server.id);
        
        const icon = server.icon || `https://cdn.discordapp.com/embed/avatars/${server.id % 5}.png`;
        
        item.innerHTML = `
            <div class="server-icon">
                <img src="${icon}" alt="${server.name}" onerror="this.src='https://cdn.discordapp.com/embed/avatars/0.png'">
            </div>
            <span class="server-name">${server.name}</span>
        `;
        
        container.appendChild(item);
    });
}

function selectServer(serverId) {
    currentServer = userServers.find(s => s.id === serverId);
    if (!currentServer) return;
    
    // Update UI
    document.querySelectorAll('.server-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelectorAll('.server-item').forEach(item => {
        if (item.querySelector('.server-name').textContent === currentServer.name) {
            item.classList.add('active');
        }
    });
    
    document.getElementById('currentServerName').textContent = currentServer.name;
    document.getElementById('overviewMembers').textContent = currentServer.members || 0;
    document.getElementById('overviewChannels').textContent = currentServer.channels || 0;
    document.getElementById('overviewRoles').textContent = currentServer.roles || 0;
    document.getElementById('overviewMessages').textContent = '0';
    
    // Show overview page
    showPage('overview');
    
    // Load settings
    loadServerSettings(serverId);
}

function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page-content').forEach(page => {
        page.style.display = 'none';
    });
    
    // Show selected page
    const page = document.getElementById('page-' + pageName);
    if (page) {
        page.style.display = 'block';
    }
    
    // Update header
    const titles = {
        'overview': 'Genel Bakış',
        'moderation': 'Moderasyon',
        'welcome': 'Hoş Geldin',
        'economy': 'Ekonomi',
        'levels': 'Seviye'
    };
    document.getElementById('pageTitle').textContent = titles[pageName] || 'Genel Bakış';
    
    // Show/hide save bar
    const saveBar = document.getElementById('saveBar');
    if (pageName !== 'overview') {
        saveBar.style.display = 'flex';
    } else {
        saveBar.style.display = 'none';
    }
}

async function loadServerSettings(serverId) {
    try {
        const res = await fetch(`/api/server/${serverId}/settings`);
        const data = await res.json();
        
        if (data.error) {
            showToast('❌ ' + data.error, 'error');
            return;
        }
        
        const settings = data.settings || data;
        
        // Moderation
        if (settings.moderation) {
            document.getElementById('modAntispam').checked = settings.moderation.antispam || false;
            document.getElementById('modAntilink').checked = settings.moderation.antilink || false;
            document.getElementById('modAnticaps').checked = settings.moderation.anticaps || false;
            document.getElementById('modAutorole').checked = settings.moderation.autorole || false;
            document.getElementById('autoroleRoleId').value = settings.moderation.autorole_role_id || '';
            document.getElementById('logChannelId').value = settings.moderation.log_channel_id || '';
        }
        
        // Welcome
        if (settings.welcome) {
            document.getElementById('welcomeEnabled').checked = settings.welcome.enabled || false;
            document.getElementById('welcomeChannelId').value = settings.welcome.channel || '';
            document.getElementById('welcomeMessage').value = settings.welcome.message || '';
        }
        
        // Leave
        if (settings.leave) {
            document.getElementById('leaveEnabled').checked = settings.leave.enabled || false;
            document.getElementById('leaveChannelId').value = settings.leave.channel || '';
            document.getElementById('leaveMessage').value = settings.leave.message || '';
        }
        
        // Economy
        if (settings.economy) {
            document.getElementById('economyEnabled').checked = settings.economy.enabled !== false;
            document.getElementById('dailyReward').value = settings.economy.daily_reward || 250;
            document.getElementById('startBalance').value = settings.economy.start_balance || 500;
        }
        
        // Levels
        if (settings.levels) {
            document.getElementById('levelsEnabled').checked = settings.levels.enabled !== false;
            document.getElementById('xpPerMessage').value = settings.levels.xp_per_message || 5;
        }
    } catch (e) {
        console.log('Settings load failed:', e);
    }
}

async function saveSettings() {
    if (!currentServer) return;
    
    const settings = {
        moderation: {
            antispam: document.getElementById('modAntispam').checked,
            antilink: document.getElementById('modAntilink').checked,
            anticaps: document.getElementById('modAnticaps').checked,
            autorole: document.getElementById('modAutorole').checked,
            autorole_role_id: document.getElementById('autoroleRoleId').value,
            log_channel_id: document.getElementById('logChannelId').value
        },
        welcome: {
            enabled: document.getElementById('welcomeEnabled').checked,
            channel_id: document.getElementById('welcomeChannelId').value,
            message: document.getElementById('welcomeMessage').value
        },
        leave: {
            enabled: document.getElementById('leaveEnabled').checked,
            channel_id: document.getElementById('leaveChannelId').value,
            message: document.getElementById('leaveMessage').value
        },
        economy: {
            enabled: document.getElementById('economyEnabled').checked,
            daily_reward: parseInt(document.getElementById('dailyReward').value) || 250,
            start_balance: parseInt(document.getElementById('startBalance').value) || 500
        },
        levels: {
            enabled: document.getElementById('levelsEnabled').checked,
            xp_per_message: parseInt(document.getElementById('xpPerMessage').value) || 5
        }
    };
    
    try {
        const res = await fetch(`/api/server/${currentServer.id}/settings`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(settings)
        });
        const result = await res.json();
        
        if (result.success) {
            showToast('✅ Ayarlar başarıyla kaydedildi!', 'success');
        } else {
            showToast('❌ Hata: ' + (result.message || 'Bilinmiyor'), 'error');
        }
    } catch (e) {
        showToast('❌ Bağlantı hatası', 'error');
    }
}

function logout() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'user_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    currentUser = null;
    currentServer = null;
    userServers = [];
    showLandingPage();
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('open');
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> ${message}`;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

async function goToPanel(e) {
    e.preventDefault();
    try {
        const res = await fetch('/api/session');
        const data = await res.json();
        
        if (data.authenticated && data.servers && data.servers.length > 0) {
            // Already logged in with servers - go to dashboard
            showDashboard();
        } else {
            // Not logged in - go to OAuth
            window.location.href = '/api/discord-oauth';
        }
    } catch (e) {
        window.location.href = '/api/discord-oauth';
    }
}

// Add toast styles dynamically
const toastStyle = document.createElement('style');
toastStyle.textContent = `
    .toast {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        padding: 15px 25px;
        border-radius: 10px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 1000;
        opacity: 0;
        transition: all 0.3s ease;
    }
    .toast.show {
        transform: translateX(-50%) translateY(0);
        opacity: 1;
    }
    .toast-success {
        background: var(--success);
        color: #000;
    }
    .toast-error {
        background: var(--danger);
        color: #fff;
    }
`;
document.head.appendChild(toastStyle);
