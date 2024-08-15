import logging.config

import uvicorn
import yaml

import directories

with open(directories.logging, "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)


if __name__ == "__main__":
    uvicorn.run(
        "mydata_chatbot.apps.v1:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True,
    )
