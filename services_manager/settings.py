from services_manager.utils.env import env_or_exit

APP_DEBUG_MODE = env_or_exit('APP_DEBUG_MODE', cast=bool)
LOGFILE_PATH = env_or_exit('LOGFILE_PATH', cast=str)
