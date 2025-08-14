"""
Production forms for DDoS AI Detection System
This file handles missing dependencies gracefully
"""

from django import forms

# Try to import captcha, but handle gracefully if not available
try:
    from captcha.fields import CaptchaField
    CAPTCHA_AVAILABLE = True
except ImportError:
    CAPTCHA_AVAILABLE = False
    print("Warning: Captcha not available")

class CustomCaptchaForm(forms.Form):
    """Captcha form that works with or without captcha library"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if CAPTCHA_AVAILABLE:
            self.fields['captcha'] = CaptchaField(
                label='Captcha',
                required=True,
                error_messages={
                    'required': 'Captcha cannot be empty'
                }
            )
        else:
            # Create a dummy captcha field that always validates
            self.fields['captcha'] = forms.CharField(
                label='Captcha (Demo Mode)',
                required=False,
                widget=forms.TextInput(attrs={'placeholder': 'Demo mode - any value accepted'})
            )
    
    def clean_captcha(self):
        """Clean captcha field"""
        if CAPTCHA_AVAILABLE:
            # Use real captcha validation
            return super().clean_captcha()
        else:
            # In demo mode, accept any value
            return self.cleaned_data.get('captcha', 'demo')

class SimpleLoginForm(forms.Form):
    """Simple login form without captcha"""
    username = forms.CharField(
        label='Username',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
