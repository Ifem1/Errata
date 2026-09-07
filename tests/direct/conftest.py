import pytest


@pytest.fixture(scope="session", autouse=True)
def _windows_gltest_tempfile_compat():
    """The v0.29.2 loader unlinks an fd-0 tempfile while it is still open on Windows."""
    if __import__("os").name != "nt":
        yield
        return
    import os

    original_unlink = os.unlink

    def unlink_after_fd_close(path):
        try:
            original_unlink(path)
        except PermissionError:
            # The loader has duplicated this descriptor onto stdin; it is
            # released by the VM after contract loading completes.
            pass

    os.unlink = unlink_after_fd_close
    yield
    os.unlink = original_unlink


@pytest.fixture(autouse=True)
def _enable_pickling_validation(direct_vm):
    direct_vm.check_pickling = True

    original_refresh = direct_vm._refresh_gl_message

    def refresh_with_datetime():
        original_refresh()
        import sys

        gl = sys.modules.get("genlayer.gl")
        if gl is not None and isinstance(getattr(gl, "message_raw", None), dict):
            gl.message_raw["datetime"] = direct_vm._datetime

    direct_vm._refresh_gl_message = refresh_with_datetime
    direct_vm._refresh_gl_message()
    yield
