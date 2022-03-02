from api import create_app
import os

port = int(os.environ.get('PORT', 8080))
print(f" the port is {port}")

app = create_app()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
