from app import app
from app.config import config

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT)