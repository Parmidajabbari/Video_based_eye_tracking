import logging

# def __init__(self):
#     self.logger
# Configure the logging system
def configure_logging(self):
    logging.basicConfig(
        level=logging.DEBUG,  # Set the desired logging level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('my_app.log'),  # Log to a file
            logging.StreamHandler()  # Log to the console
        ]
    )
    self.logger = logging.getLogger(__name__)