import sys
import os

cwd = os.getcwd()
fmt_path = cwd.split('/')
fmt_path.pop(-1)
app_dir = ('/').join(fmt_path)

sys.path.append(os.getcwd())
sys.path.append(f'{app_dir}/models')
sys.path.append(app_dir)

os.environ['APP_DIR'] = app_dir

import models
import configCollector
from fastapi import FastAPI

app = FastAPI()

@app.post("/config_device", response_model=models.ConfigResponse)
async def post_config(config_data: models.Device):
    c = configCollector.configCollector(config_data)
    results, status, msg = c.process_config_diff()
    print(results, status, msg)
    return models.ConfigResponse(results=results, status=status, msg=msg)