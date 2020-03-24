# RFE the same functioanlity is provided by https://github.com/channelcat/sanic/pull/1241
# Remove this file after applying that pull request
import uuid

from sanic.router import Router, REGEX_TYPES


class UUIDConverter:
    """This converter only accepts UUID strings:: Rule('/object/<identifier:uuid>')"""

    regex = r"[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-" r"[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}"

    def to_python(self, value):
        return uuid.UUID(value)

    def __call__(self, *args, **kwargs):
        return self.to_python(args[0])


def get_custom_converters():
    uuid_converter = UUIDConverter()
    converters = {"uuid": (uuid_converter, uuid_converter.regex)}
    return converters


class ExtRouter(Router):

    def __init__(self, converters=None):
        super().__init__()
        self._converters = REGEX_TYPES
        if converters:
            self._converters.update(converters)

    def parse_parameter_string(self, parameter_string):
        """Parse a parameter string into its constituent name, type, and
                pattern

                For example::

                    parse_parameter_string('<param_one:[A-z]>')` ->
                        ('param_one', str, '[A-z]')

                :param parameter_string: String to parse
                :return: tuple containing
                    (parameter_name, parameter_type, parameter_pattern)
                """
        # We could receive NAME or NAME:PATTERN
        name = parameter_string
        pattern = "string"
        if ":" in parameter_string:
            name, pattern = parameter_string.split(":", 1)
            if not name:
                raise ValueError(
                    "Invalid parameter syntax: {}".format(parameter_string)
                )

        default = (str, pattern)
        # Pull from pre-configured types
        _type, pattern = self._converters.get(pattern, default)

        return name, _type, pattern
