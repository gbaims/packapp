from gbaims.packapp.io.config import Config

# logconfig_dict = Config().logging.as_dict()  # type: ignore


_config = Config().logging  # type: ignore
# errorlog = "-"
loglevel = _config.level
# accesslog = "-"
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
