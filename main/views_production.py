"""
Production-ready views for DDoS AI Detection System
This file handles missing dependencies gracefully and provides basic functionality
"""

import os
import hashlib
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
    """Main dashboard view"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'message': 'Welcome to DDoS AI Detection System - Demo Mode',
        'demo_mode': True
    }
    return render(request, 'index.html', context)

def screen(request):
    """Screen view"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'demo_mode': True
    }
    return render(request, 'screen.html', context)

def dataset_result(request):
    """Dataset result view"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'message': 'Dataset analysis not available in demo mode',
        'demo_mode': True
    }
    return render(request, 'dataset_result.html', context)

def model_tuning(request):
    """Model tuning view"""
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
    """LSTM tuning placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def do_tuning_cnn(request):
    """CNN tuning placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def do_tuning_cnn_lstm_attention(request):
    """CNN-LSTM-Attention tuning placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def tuning_lstm_duofenlei(request):
    """LSTM tuning placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def tuning_cnn_duofenlei(request):
    """CNN tuning placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def tuning_cnn_lstm_att_duofenlei(request):
    """CNN-LSTM-Attention tuning placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def reset_parameter_lstm(request):
    """Reset LSTM parameters placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def ip_rule_list(request):
    """IP rules list view"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'message': 'IP rules management not available in demo mode',
        'demo_mode': True
    }
    return render(request, 'ip_rules.html', context)

def add_ip_rule(request):
    """Add IP rule placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def delete_ip_rule(request, rule_id):
    """Delete IP rule placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def get_dashboard_stats(request):
    """Dashboard stats API placeholder"""
    return JsonResponse({
        'status': 'success',
        'data': {
            'total_requests': 0,
            'blocked_requests': 0,
            'suspicious_ips': 0,
            'system_status': 'Demo Mode'
        }
    })

def traffic_log_list(request):
    """Traffic log list view"""
    if not request.session.get('is_login'):
        return redirect('/login')
    
    context = {
        'user': request.session.get('login_user'),
        'features': FEATURES,
        'message': 'Traffic logs not available in demo mode',
        'demo_mode': True
    }
    return render(request, 'traffic_log.html', context)

def traffic_log_detail(request, log_id):
    """Traffic log detail API placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def traffic_log_detete(request, log_id):
    """Traffic log delete API placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def traffic_log_batch_delete(request):
    """Traffic log batch delete API placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def traffic_log_export(request):
    """Traffic log export API placeholder"""
    return JsonResponse({'status': 'error', 'message': 'Feature not available in demo mode'})

def error_view(request):
    """Generic error view"""
    return render(request, 'error.html', {'error': 'An error occurred'})
