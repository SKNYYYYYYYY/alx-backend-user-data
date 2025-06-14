import logging
class MyFormatter(logging.Formatter):
	def format(self, record):
		record.msg = record.msg.upper()
		return super().format(record)

logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
formatter = MyFormatter('%(levelname)s - %(asctime)s: %(message)s')
console.setFormatter(formatter)

logger.addHandler(console)



logger.info("Program started")
