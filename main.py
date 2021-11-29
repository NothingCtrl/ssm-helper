# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from app import app

load_dotenv()

if __name__ == "__main__":
    app.run("0.0.0.0", port=int(os.getenv("APP_PORT", "8080")), debug=(os.getenv('DEBUG') and os.getenv('DEBUG') in ('true', 'True', '1')))
