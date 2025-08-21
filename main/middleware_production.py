"""
Production middleware for handling special cases
"""

class HealthCheckMiddleware:
    """Middleware to handle health check requests without host validation"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if this is a health check request
        if request.path == '/health':
            # For health checks, we'll bypass the host validation
            # This is safe as it's only for internal health checks
            request.META['HTTP_HOST'] = 'df-defence.fly.dev'
        
        response = self.get_response(request)
        return response
