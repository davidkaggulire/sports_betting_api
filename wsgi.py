from api import create_app
import os

port = int(os.environ.get('PORT', 8080))
app = create_app()
print(f" the port is {port}")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
