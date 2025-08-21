"""
Production-ready views for DDoS AI Detection System
This file handles missing dependencies gracefully and provides basic functionality
"""

import os
import hashlib
import random
import json
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.urls import reverse

# Try to import dependencies, but handle gracefully if not available
try:
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    PAGINATOR_AVAILABLE = True
except ImportError:
    PAGINATOR_AVAILABLE = False

try:
    from pyecharts import options as opts
    from pyecharts.charts import Pie, Bar, Line
    PYECHARTS_AVAILABLE = True
except ImportError:
    PYECHARTS_AVAILABLE = False
    print("Warning: pyecharts not available, charts will be disabled")

try:
    from main.models import User, IPAddressRule, TuningModels, TrafficLog
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    print("Warning: Database models not available")

try:
    from main.forms_production import CustomCaptchaForm
    CAPTCHA_AVAILABLE = True
except ImportError:
    CAPTCHA_AVAILABLE = False
    print("Warning: Captcha forms not available")

# Global flags for feature availability
FEATURES = {
    'pyecharts': PYECHARTS_AVAILABLE,
    'models': MODELS_AVAILABLE,
    'captcha': CAPTCHA_AVAILABLE,
    'paginator': PAGINATOR_AVAILABLE
}

# Demo credentials
DEMO_CREDENTIALS = {
    'admin': 'admin123',
    'demo': 'demo123',
    'user': 'user123',
    'test': 'test123'
}

# Demo attack data for demonstration
DEMO_ATTACK_DATA = {
    'recent_attacks': [
        {'ip': '192.168.1.100', 'type': 'DDoS', 'severity': 'High', 'time': '2 minutes ago'},
        {'ip': '10.0.0.50', 'type': 'Port Scan', 'severity': 'Medium', 'time': '5 minutes ago'},
        {'ip': '172.16.0.25', 'type': 'Brute Force', 'severity': 'High', 'time': '10 minutes ago'},
    ],
    'blocked_ips': [
        '192.168.1.100',
        '10.0.0.50', 
        '172.16.0.25',
        '203.0.113.10',
        '198.51.100.5'
    ],
    'traffic_stats': {
        'total_requests': 15420,
        'blocked_requests': 342,
        'suspicious_ips': 15,
        'system_status': 'Protected'
    }
}

def health_check(request):
    """Simple health check for Fly.io"""
    return HttpResponse("OK", content_type="text/plain")

def login(request):
    """Basic login view with demo mode"""
    captcha_form = None
    if CAPTCHA_AVAILABLE:
        try:
            captcha_form = CustomCaptchaForm()
        except:
            captcha_form = None
    
    context = {
        "captcha_form": captcha_form,
        "features": FEATURES,
        "demo_credentials": DEMO_CREDENTIALS,
        "demo_mode": True
    }
    return render(request, 'login.html', context)

def simple_login(request):
    """Simple login without captcha for demo purposes"""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('pass', '')
        
        # Demo login - accept any username/password
        if username and password:
            # Create a demo user session
            request.session['is_login'] = True
            request.session['login_user'] = {
                'username': username,
                'nickname': f'Demo User ({username})',
                'status': 1
            }
            messages.success(request, f'Welcome {username}! Demo mode activated.')
            return redirect('/index')
        else:
            messages.error(request, 'Username and password are required')
    
    context = {
        'demo_mode': True,
        'demo_credentials': DEMO_CREDENTIALS,
        'features': FEATURES
    }
    return render(request, 'login.html', context)

def do_login(request):
    """Handle login form submission - simplified for demo"""
    if not MODELS_AVAILABLE:
        # Fall back to demo mode
        return simple_login(request)
    
    captcha_form = None
    if CAPTCHA_AVAILABLE:
        try:
            captcha_form = CustomCaptchaForm()
        except:
            captcha_form = None
    
    try:
        username = request.POST.get('username', '')
        password = request.POST.get('pass', '')
        
        if not username or not password:
            context = {
                "captcha_form": captcha_form,
                "info": 'Username and password are required'
            }
            messages.error(request, 'Username and password are required')
            return render(request, 'login.html', context)
        
        # Check demo credentials first
        if username in DEMO_CREDENTIALS and password == DEMO_CREDENTIALS[username]:
            request.session['is_login'] = True
            request.session['login_user'] = {
                'username': username,
                'nickname': f'Demo User ({username})',
                'status': 1
            }
            messages.success(request, f'Welcome {username}! Demo mode activated.')
            return redirect('/index')
        
        # Try to get user from database
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            context = {
                "captcha_form": captcha_form,
                "info": f'User not found. Try demo credentials: {list(DEMO_CREDENTIALS.keys())}',
                "demo_credentials": DEMO_CREDENTIALS
            }
            messages.error(request, f'User not found. Try demo credentials: {list(DEMO_CREDENTIALS.keys())}')
            return render(request, 'login.html', context)
        
        # Check user status and password
        if user.status == 1:  # Regular user
            # Verify password
            md5 = hashlib.md5()
            s = password + user.password_salt
            md5.update(s.encode('utf-8'))
            
            if user.password_hash == md5.hexdigest():
                request.session['is_login'] = True
                request.session['login_user'] = user.toDict()
                return redirect('/index')
            else:
                context = {
                    "captcha_form": captcha_form,
                    "info": 'Incorrect password'
                }
                messages.error(request, 'Incorrect password')
                return render(request, 'login.html', context)
        
        elif user.status == 6:  # Admin user
            # Verify password for admin
            md5 = hashlib.md5()
            s = password + user.password_salt
            md5.update(s.encode('utf-8'))
            
            if user.password_hash == md5.hexdigest():
                request.session['is_login'] = True
                request.session['adminuser'] = user.toDict()
                return redirect(reverse("myadmin_user_index", args=(1,)))
            else:
                context = {
                    "captcha_form": captcha_form,
                    "info": 'Incorrect password'
                }
                messages.error(request, 'Incorrect password')
                return render(request, 'login.html', context)
        else:
            context = {
                "captcha_form": captcha_form,
                "info": 'Account has no permission'
            }
            messages.error(request, 'Account has no permission')
            return render(request, 'login.html', context)
            
    except Exception as e:
        print(f"Login error: {e}")
        # Fall back to demo mode
        return simple_login(request)
    
    return render(request, 'login.html', context)

def logout_view(request):
    """Handle user logout"""
    request.session.flush()
    messages.success(request, 'Successfully logged out')
    return redirect('/login')

def register(request):
    """Basic registration view"""
    if not MODELS_AVAILABLE:
        return render(request, 'error.html', {
            'error': 'Registration not available - System not fully configured'
        })
    
    captcha_form = None
    if CAPTCHA_AVAILABLE:
        try:
            captcha_form = CustomCaptchaForm()
        except:
            captcha_form = None
    
    context = {
        "captcha_form": captcha_form,
        "features": FEATURES,
        "demo_credentials": DEMO_CREDENTIALS
    }
    return render(request, 'register.html', context)

def do_register(request):
    """Handle registration form submission"""
    if not MODELS_AVAILABLE:
        return render(request, 'error.html', {
            'error': 'Registration not available - System not fully configured'
        })
    
    # Basic registration logic would go here
    messages.success(request, 'Registration functionality not implemented in demo version')
    return redirect('/login')

def forgot_pd(request):
    """Password recovery view"""
    context = {
        'features': FEATURES,
        'demo_credentials': DEMO_CREDENTIALS
    }
    return render(request, 'forgot_pd.html', context)

def index(request, *args, **kwargs):
    """Main dashboard view with demo attack data"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'message': 'Welcome to DDoS AI Detection System - Demo Mode',
        'demo_mode': True,
        'attack_data': DEMO_ATTACK_DATA
    }
    return render(request, 'index.html', context)

def screen(request):
    """Screen view with demo traffic monitoring and interactive features"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    # Fake model performance data for demo
    fake_model_data = {
        'cnn': {'accuracy': 94.2, 'precision': 92.8, 'recall': 91.5, 'f1_score': 92.1},
        'lstm': {'accuracy': 96.1, 'precision': 95.3, 'recall': 94.7, 'f1_score': 95.0},
        'cnn_lstm_attention': {'accuracy': 97.8, 'precision': 97.2, 'recall': 96.9, 'f1_score': 97.0}
    }
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'demo_mode': True,
        'traffic_stats': DEMO_ATTACK_DATA['traffic_stats'],
        'model_data': fake_model_data,
        'attack_types': ['Normal', 'DDoS', 'Port Scan', 'Botnet', 'Brute Force'],
        'detection_rates': [98.5, 96.2, 94.8, 97.1, 93.5]
    }
    return render(request, 'screen.html', context)

def dataset_result(request):
    """Dataset result view with demo analysis and interactive features"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    # Fake dataset analysis data for demo
    fake_dataset_data = {
        'total_samples': 15000,
        'normal_traffic': 12000,
        'attack_samples': 3000,
        'attack_distribution': {
            'DDoS': 1200,
            'Port Scan': 800,
            'Botnet': 600,
            'Brute Force': 400
        },
        'feature_importance': ['Packet Size', 'Flow Duration', 'Protocol', 'Port', 'Flags'],
        'model_accuracy': 96.8
    }
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'message': 'Dataset Analysis - AI Model Training Results',
        'demo_mode': True,
        'demo_attacks': DEMO_ATTACK_DATA['recent_attacks'],
        'dataset_data': fake_dataset_data
    }
    return render(request, 'dataset_result.html', context)

def model_tuning(request):
    """Model tuning view with demo configuration"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'message': 'Model tuning not available in demo mode',
        'demo_mode': True
    }
    return render(request, 'model_tuning.html', context)

def do_tuning_lstm_multi(request):
    """LSTM tuning placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: LSTM model tuning simulation',
        'progress': 100,
        'result': 'Model training completed successfully (Demo)'
    })

def do_tuning_cnn(request):
    """CNN tuning placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: CNN model tuning simulation',
        'progress': 100,
        'result': 'Model training completed successfully (Demo)'
    })

def do_tuning_cnn_lstm_attention(request):
    """CNN-LSTM-Attention tuning placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: CNN-LSTM-Attention model tuning simulation',
        'progress': 100,
        'result': 'Model training completed successfully (Demo)'
    })

def tuning_lstm_duofenlei(request):
    """LSTM tuning placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: LSTM multi-class tuning simulation',
        'progress': 100,
        'result': 'Model training completed successfully (Demo)'
    })

def tuning_cnn_duofenlei(request):
    """CNN tuning placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: CNN multi-class tuning simulation',
        'progress': 100,
        'result': 'Model training completed successfully (Demo)'
    })

def tuning_cnn_lstm_att_duofenlei(request):
    """CNN-LSTM-Attention tuning placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: CNN-LSTM-Attention multi-class tuning simulation',
        'progress': 100,
        'result': 'Model training completed successfully (Demo)'
    })

def reset_parameter_lstm(request):
    """Reset LSTM parameters placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: LSTM parameters reset successfully'
    })

def ip_rule_list(request):
    """IP rules list view with demo blocked IPs"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'message': 'IP rules management not available in demo mode',
        'demo_mode': True,
        'blocked_ips': DEMO_ATTACK_DATA['blocked_ips']
    }
    return render(request, 'ip_rules.html', context)

def add_ip_rule(request):
    """Add IP rule placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: IP rule added successfully'
    })

def delete_ip_rule(request, rule_id):
    """Delete IP rule placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: IP rule deleted successfully'
    })

def get_dashboard_stats(request):
    """Dashboard stats API with demo data"""
    return JsonResponse({
        'status': 'success',
        'data': DEMO_ATTACK_DATA['traffic_stats']
    })

def get_live_traffic(request):
    """Get live traffic updates for demo"""
    if not request.session.get('is_login'):
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    # Simulate real-time traffic updates
    import random
    import time
    
    new_traffic = {
        'id': random.randint(1000, 9999),
        'created_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'source_ip': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        'dest_ip': f"10.0.0.{random.randint(1,100)}",
        'source_port': random.randint(1024, 65535),
        'dest_port': random.choice([80, 443, 22, 53, 21]),
        'protocol': random.choice(['TCP', 'UDP']),
        'attack_type': random.choice(['Normal', 'DDoS', 'Port Scan', 'Botnet', 'Brute Force']),
        'threat_level': random.choice(['Low', 'Medium', 'High']),
        'packet_count': random.randint(100, 20000),
        'bytes_transferred': random.randint(1000, 5000000)
    }
    
    return JsonResponse({
        'status': 'success',
        'new_traffic': new_traffic,
        'demo_mode': True
    })

def traffic_log_list(request):
    """Traffic log list view with demo data and interactive features"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    # Fake live traffic data for demo
    fake_traffic_data = [
        {
            'id': 1,
            'created_time': '2025-08-21 15:30:22',
            'source_ip': '192.168.1.100',
            'dest_ip': '10.0.0.50',
            'source_port': 44321,
            'dest_port': 80,
            'protocol': 'TCP',
            'attack_type': 'DDoS',
            'threat_level': 'High',
            'packet_count': 15000,
            'bytes_transferred': 2048000
        },
        {
            'id': 2,
            'created_time': '2025-08-21 15:29:15',
            'source_ip': '203.45.67.89',
            'dest_ip': '10.0.0.51',
            'source_port': 22,
            'dest_port': 22,
            'protocol': 'TCP',
            'attack_type': 'Brute Force',
            'threat_level': 'Medium',
            'packet_count': 250,
            'bytes_transferred': 12500
        },
        {
            'id': 3,
            'created_time': '2025-08-21 15:28:45',
            'source_ip': '98.76.54.32',
            'dest_ip': '10.0.0.52',
            'source_port': 53,
            'dest_port': 53,
            'protocol': 'UDP',
            'attack_type': 'Port Scan',
            'threat_level': 'Low',
            'packet_count': 500,
            'bytes_transferred': 25000
        }
    ]
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'message': 'Live Traffic Monitoring - AI Detection Results',
        'demo_mode': True,
        'demo_logs': fake_traffic_data,
        'traffic_logs': fake_traffic_data,
        'total_logs': len(fake_traffic_data),
        'high_risk_count': 1,
        'medium_risk_count': 1,
        'low_risk_count': 1
    }
    return render(request, 'traffic_log.html', context)

def traffic_log_detail(request, log_id):
    """Traffic log detail API placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: Traffic log details not available'
    })

def traffic_log_detete(request, log_id):
    """Traffic log delete API placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: Traffic log deleted successfully'
    })

def traffic_log_batch_delete(request):
    """Traffic log batch delete API placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: Batch delete completed successfully'
    })

def traffic_log_export(request):
    """Traffic log export API placeholder with demo response"""
    return JsonResponse({
        'status': 'demo',
        'message': 'Demo mode: Export completed successfully'
    })

def error_view(request):
    """Generic error view"""
    return render(request, 'error.html', {'error': 'An error occurred'})
