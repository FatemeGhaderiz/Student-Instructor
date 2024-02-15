import warnings
import pytest


def test_warning():
    with pytest.warns(UserWarning, match="your_warning_message_here"):
        # Code that should trigger the warning
        warnings.warn("your_warning_message_here", UserWarning)
