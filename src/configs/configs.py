import configparser
import json
import os
from datetime import datetime

DATE_TIME = str(datetime.now().strftime('%Y-%m-%d-%H'))

RETRY_TIMES = 3

# DO NOT CHANGE. It's not User-set parameters
CRAWL_MIN_PRICE_ITEM = 0
CRAWL_MAX_PRICE_ITEM = 150000

# Change To Your Brower Cookie
COOKIE = "Device-Id=nZhTDnoPH2q0iAkXO9U0; Locale-Supported=en; game=csgo; _ga=GA1.2.1993518637.1596430439; _gid=GA1.2.747740476.1596430439; NTES_YD_SESS=GskDhBj_y7lVvO02VbYuhjpzm8GexhDzZXX.CRsQ4kYZqcw9TbAHU1R00I7C3lno..P.OJQEJT7IWOsT7V5pvlG67YB2iIqiCs_uBj_TJ6y.XG3NLI76fKfrJLoxFf_BcuZeKqEefbHgtmCwur4u0bYO5SzTy2mPmCuviZNQ2LbYi7K694FsyEU_nKItr2oCF4d.XrlZjSI87y89W4et1NpRpXC7lmtTjz4eIj6bPSadO; S_INFO=1596430521|0|3&80##|1-8602881794; P_INFO=1-8602881794|1596430521|1|netease_buff|00&99|null&null&null#US&null#10#0|&0|null|1-8602881794; session=1-kRVXa6KVv1ZXkfaoXOCyF3JMpCJLva7t3LCXqvBEu_vf2041017361; _gat_gtag_UA_109989484_1=1; csrf_token=IjdmZDJhZTA0ZWVlYzU2MTQ0YjFhNzlhODM1MzZmZjg1ODBlMzA4ZDIi.EgkqQg.JGLTzPrIZyklrlGD_dawbGdTf8Y"


# Log file
LOG_PATH = "log"
NORMAL_LOGGER = os.path.join(LOG_PATH, 'log_' + DATE_TIME + '.log')
