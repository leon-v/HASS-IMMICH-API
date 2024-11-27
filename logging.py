""" Customised logging """

import logging

class VSCodeFormatter(logging.Formatter):
    """ Customised logging formatter for VSCode """

    def formatException(self, ei):
        """ Format exception information """
        result = super().formatException(ei)
        result = self.do_replacements(result)
        return result

    def format(self, record: logging.LogRecord):
        """ Format log """
        result = super().format(record)
        # Replace 'File "file", line line' with 'file:line'
        if record.exc_info:
            result = self.do_replacements(result)
        return result

    def do_replacements(self, result: str):
        """ Perform replacements """
        result = result.replace('File "', 'File "')
        result = result.replace('", line ', ':')
        result = result.replace(', in ', '" in ')
        return result


def setup_logging():
    """Set up the custom logger."""
    # Get the logger
    logger = logging.getLogger('homeassistant')
    # logger.setLevel(logging.DEBUG)

    # Create a console handler
    ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)

    # Create and set the custom formatter
    formatter = VSCodeFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)