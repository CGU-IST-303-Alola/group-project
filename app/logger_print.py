from functools import wraps
PRINT_LOGS_ENABLED = True

def print_logs(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		kwargs["LOGS_STATUS"] = PRINT_LOGS_ENABLED
		if PRINT_LOGS_ENABLED:
			print(f"Start\t{func.__name__}()")
		result = func(*args, **kwargs)
		if PRINT_LOGS_ENABLED:
			print(f"End\t{func.__name__}()")
		return result
	return wrapper
