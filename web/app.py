from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import threading
import asyncio
import json
import os

app = Flask(__name__)
CORS(app)

# Bot referansı (main.py'den alınacak)
bot = None

# Veri dosyaları
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def set_bot(bot_instance):
    global bot
    bot = bot_instance

# HTML dosyalarını serve et
@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('web', filename)

# API Endpoints
@app.route('/api/stats')
def get_stats():
    if not bot:
        return jsonify({'error': 'Bot not connected'}), 500
    
    return jsonify({
        'servers': len(bot.guilds),
        'members': sum(len(g.members) for g in bot.guilds),
        'messages': 0,  # Mesaj sayacı eklenebilir
        'ping': int(bot.latency * 1000) if bot.latency else 0
    })

@app.route('/api/servers')
def get_servers():
    if not bot:
        return jsonify([])
    
    servers = []
    for guild in bot.guilds:
        servers.append({
            'id': str(guild.id),
            'name': guild.name,
            'icon': guild.icon.url if guild.icon else None,
            'members': guild.member_count,
            'channels': len(guild.channels),
            'roles': len(guild.roles)
        })
    
    return jsonify(servers)

@app.route('/api/users')
def get_users():
    # Veritabanından kullanıcıları al
    users_file = os.path.join(DATA_DIR, 'users.json')
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/economy')
def get_economy():
    economy_file = os.path.join(DATA_DIR, 'economy.json')
    if os.path.exists(economy_file):
        with open(economy_file, 'r') as f:
            data = json.load(f)
            
        # En zengin kullanıcıları sırala
        sorted_users = sorted(data.get('users', {}).items(), 
                            key=lambda x: x[1].get('money', 0), 
                            reverse=True)[:5]
        
        richest = []
        for user_id, user_data in sorted_users:
            richest.append({
                'id': user_id,
                'name': f'User#{user_id[:4]}',
                'avatar': 'https://cdn.discordapp.com/embed/avatars/0.png',
                'money': user_data.get('money', 0)
            })
        
        total_money = sum(u.get('money', 0) for u in data.get('users', {}).values())
        total_bank = sum(u.get('bank', 0) for u in data.get('users', {}).values())
        
        return jsonify({
            'totalMoney': total_money,
            'totalBank': total_bank,
            'transactions': data.get('transactions', 0),
            'richest': richest
        })
    
    return jsonify({
        'totalMoney': 0,
        'totalBank': 0,
        'transactions': 0,
        'richest': []
    })

@app.route('/api/economy/add', methods=['POST'])
def economy_add():
    data = request.json
    user_id = data.get('user')
    amount = data.get('amount', 0)
    
    economy_file = os.path.join(DATA_DIR, 'economy.json')
    
    if os.path.exists(economy_file):
        with open(economy_file, 'r') as f:
            eco_data = json.load(f)
    else:
        eco_data = {'users': {}, 'transactions': 0}
    
    if user_id not in eco_data['users']:
        eco_data['users'][user_id] = {'money': 0, 'bank': 0}
    
    eco_data['users'][user_id]['money'] += amount
    eco_data['transactions'] += 1
    
    with open(economy_file, 'w') as f:
        json.dump(eco_data, f)
    
    return jsonify({'success': True})

@app.route('/api/economy/remove', methods=['POST'])
def economy_remove():
    data = request.json
    user_id = data.get('user')
    amount = data.get('amount', 0)
    
    economy_file = os.path.join(DATA_DIR, 'economy.json')
    
    if os.path.exists(economy_file):
        with open(economy_file, 'r') as f:
            eco_data = json.load(f)
    else:
        return jsonify({'error': 'No data'}), 400
    
    if user_id in eco_data['users']:
        eco_data['users'][user_id]['money'] = max(0, eco_data['users'][user_id]['money'] - amount)
        
        with open(economy_file, 'w') as f:
            json.dump(eco_data, f)
        
        return jsonify({'success': True})
    
    return jsonify({'error': 'User not found'}), 400

@app.route('/api/economy/reset', methods=['POST'])
def economy_reset():
    economy_file = os.path.join(DATA_DIR, 'economy.json')
    
    eco_data = {'users': {}, 'transactions': 0}
    
    with open(economy_file, 'w') as f:
        json.dump(eco_data, f)
    
    return jsonify({'success': True})

@app.route('/api/announce', methods=['POST'])
async def announce():
    if not bot:
        return jsonify({'error': 'Bot not connected'}), 500
    
    data = request.json
    channel_id = int(data.get('channel'))
    message = data.get('message')
    
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Channel not found'}), 404

@app.route('/api/backup', methods=['POST'])
def create_backup():
    backup_dir = os.path.join(DATA_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'backup_{timestamp}'
    
    # Verileri yedekle
    backup_file = os.path.join(backup_dir, f'{backup_name}.json')
    
    backup_data = {}
    
    # Economy verileri
    economy_file = os.path.join(DATA_DIR, 'economy.json')
    if os.path.exists(economy_file):
        with open(economy_file, 'r') as f:
            backup_data['economy'] = json.load(f)
    
    # Users verileri
    users_file = os.path.join(DATA_DIR, 'users.json')
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            backup_data['users'] = json.load(f)
    
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f)
    
    return jsonify({'success': True, 'backup': backup_name})

@app.route('/api/premium')
def get_premium():
    premium_file = os.path.join(DATA_DIR, 'premium.json')
    
    if os.path.exists(premium_file):
        with open(premium_file, 'r') as f:
            return jsonify(json.load(f))
    
    # Varsayılan premium durumu
    return jsonify({
        'active': True,
        'expire': None,
        'features': {
            'music': True,
            'games': True,
            'stats': True,
            'auto': False,
            'custom': False,
            'priority': True
        }
    })

@app.route('/api/maintenance', methods=['POST'])
def maintenance_mode():
    data = request.json
    enabled = data.get('enabled', False)
    
    # Bakım modunu kaydet
    config_file = os.path.join(DATA_DIR, 'config.json')
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    config['maintenance'] = enabled
    
    with open(config_file, 'w') as f:
        json.dump(config, f)
    
    return jsonify({'success': True, 'maintenance': enabled})

# Bot çalışıyor mu kontrolü
@app.route('/api/health')
def health():
    return jsonify({
        'status': 'online',
        'bot': bot is not None
    })

def run_web(host='0.0.0.0', port=5000):
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    run_web()
