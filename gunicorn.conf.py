# Gunicorn configuration file
import multiprocessing

# Workers
# For low-resource VPS (e.g. 512MB RAM), keep this low (2 is usually plenty for a portfolio).
# Avoid: multiprocessing.cpu_count() * 2 + 1 (This defaults to too many on shared vCPUs)
workers = 2
threads = 2
worker_class = 'gthread' # Threaded workers use less RAM than process workers

# Timeouts
timeout = 30
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
