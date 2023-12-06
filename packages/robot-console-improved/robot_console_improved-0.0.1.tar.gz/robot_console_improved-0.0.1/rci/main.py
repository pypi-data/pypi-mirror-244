import sys
import warnings
from importlib.metadata import entry_points

from robot.output.console import VerboseOutput, DottedOutput, QuietOutput, NoOutput
from robot.run import run_cli

ENTRY_POINT_GROUP = 'robot.output.console'

import robot.output.logger
from robot.errors import DataError


def custom_console_output(type='verbose', width=78, colors='AUTO', markers='AUTO',
                          stdout=None, stderr=None):
    upper = type.upper()
    if upper == 'VERBOSE':
        return VerboseOutput(width, colors, markers, stdout, stderr)
    if upper == 'DOTTED':
        return DottedOutput(width, colors, stdout, stderr)
    if upper == 'QUIET':
        return QuietOutput(colors, stderr)
    if upper == 'NONE':
        return NoOutput()
    discoveries = entry_points(group=ENTRY_POINT_GROUP, name=type)
    if discoveries:
        if len(discoveries) > 1:
            warnings.warn("Multiple console outputs with name '%s' found. "
                          "Using first entry (%s)."
                          % (type, discoveries[0].value))
        constructor = discoveries[0].load()
        return constructor(width, colors, markers, stdout, stderr)
    values = ["VERBOSE", "DOTTED", "QUIET", "NONE"]
    discoveries = entry_points(group=ENTRY_POINT_GROUP)
    values.extend(discovery.name for discovery in discoveries)
    raise DataError("Invalid console output type '%s'. Available: %s."
                    % (type, ', '.join(values)))


if __name__ == "__main__":
    robot.output.logger.ConsoleOutput = custom_console_output
    run_cli(sys.argv[1:])
