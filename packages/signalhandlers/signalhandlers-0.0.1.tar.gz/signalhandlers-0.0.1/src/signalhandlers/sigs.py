#!/usr/bin/env python

__all__ = [
    'install_exit_on_sigpipe_handler',
    'install_quiet_ctrl_c_handler',
]

def install_exit_on_sigpipe_handler():
    """
    if our output is being piped into a command like head
    that closes down the pipe we're writing our output to
    before we're done writing, we can stop writing early.
    python sends a BrokenPipeError by default, and writes
    the exception to stderr and this seems to be the only
    way to prevent python from doing that, so let's do it
    """

    def sigpipe(signum, frame):
        os._exit(0)

    import os
    import signal
    signal.signal(signal.SIGPIPE, sigpipe)

def install_quiet_ctrl_c_handler():

    """
    from gentoo's /usr/lib/python-exec/python3.*/revdep-rebuild

    ensure that ^C interrupts are handled quietly.
    """

    def exithandler(signum, frame):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        print()
        sys.exit(1)

    import signal
    signal.signal(signal.SIGINT, exithandler)
    signal.signal(signal.SIGTERM, exithandler)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
