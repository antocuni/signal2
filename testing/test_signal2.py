import os
import ctypes
import signal
#
from signal2 import SA_SIGINFO, install_sigaction, sigval_t, sigqueue

def test_install_and_fire():
    calls = []
    def handler(signo, ptr_info, extra):
        info = ptr_info[0]
        val = info.si_value.sigval_int
        calls.append((signo, info.si_signo, val))
    install_sigaction(signal.SIGUSR2, SA_SIGINFO, handler)

    pid = os.getpid()
    val = sigval_t()
    val.sigval_int = 42
    sigqueue(pid, signal.SIGUSR2, val)
    assert calls == [(signal.SIGUSR2, signal.SIGUSR2, 42)]
