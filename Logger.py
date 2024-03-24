import logging

def logger_setup(logfile):
    logger = logging.getLogger(logfile)
    logger.setLevel(logging.DEBUG)

    # file_hander = logging.handlers.RotatingFileHandler(
    file_hander = RotatingFileHandler(
        f"{logfile}.log",
        maxBytes=51200000,
        backupCount=10,
        encoding="utf8",
        delay=0,
    )
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s:%(name)s:%(lineno)d %(message)s"
    )
    file_hander.setLevel(logging.DEBUG)
    file_hander.setFormatter(formatter)
    logger.addHandler(file_hander)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%d %H:%M:%S")
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger
