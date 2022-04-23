from app import create_app
import os



app = create_app()

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.environ.get('PORT', 5555)))