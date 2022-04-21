from app import create_app
import os



app = create_app()

if __name__ == '__main__':
    app.run( port=int(os.getenv('PORT', 5555)), debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)