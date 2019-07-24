def retry(times = 3):
	def retry_func(func):
		def _(*args, **kwds):
			for i in range(times):
				try:
					func(*args, **kwds)
					return
				except AssertionError:
					pass
			raise AssertionError(func)
		return _
	return retry_func