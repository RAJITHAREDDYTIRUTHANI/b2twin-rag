"""
Vercel serverless function wrapper for Biosphere 2 RAG Flask app
Optimized for Vercel's serverless environment - lazy initialization
"""
import sys
import os
import importlib.util

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import Flask for fallback app only
from flask import Flask

# Lazy import cache
_main_app = None
_import_lock = False

def get_app():
    """Lazy load the main app on first request using importlib"""
    global _main_app, _import_lock
    
    if _main_app is not None:
        return _main_app
        
    if _import_lock:
        # Import in progress, return fallback
        return create_fallback_app()
    
    try:
        _import_lock = True
        
        # Dynamically import the module (prevents execution at import time)
        module_path = os.path.join(os.path.dirname(__file__), '..', 'spectacular_rag_web_app.py')
        spec = importlib.util.spec_from_file_location("spectacular_rag_web_app", module_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            _main_app = module.app
            
            # Start background initialization (non-blocking)
            if hasattr(module, 'load_data_background'):
                import threading
                thread = threading.Thread(target=module.load_data_background, daemon=True)
                thread.start()
        else:
            raise ImportError("Could not load module")
            
    except Exception as e:
        print(f"Warning: Could not load main app: {e}")
        import traceback
        traceback.print_exc()
        _main_app = create_fallback_app()
    finally:
        _import_lock = False
    
    return _main_app

def create_fallback_app():
    """Create a minimal fallback Flask app"""
    fallback = Flask(__name__)
    
    @fallback.route('/')
    def index():
        return """
        <html>
        <body style="font-family: Arial; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <h1>Biosphere 2 RAG Analysis</h1>
        <p>System is initializing. Please refresh in a moment.</p>
        <p>Note: Heavy ML models may take time to load on first request.</p>
        </body>
        </html>
        """
    
    @fallback.route('/<path:path>')
    def catch_all(path):
        return {"error": "System initializing", "path": path}, 503
    
    return fallback

# Vercel expects the WSGI app directly
# We'll use a wrapper that lazy loads
class LazyApp:
    """Wrapper that lazy loads the Flask app"""
    def __call__(self, environ, start_response):
        return get_app()(environ, start_response)

# Export handler for Vercel
handler = LazyApp()
