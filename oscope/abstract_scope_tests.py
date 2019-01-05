import datetime

import pytest

import oscope.abstract_scope as abs_scope

class BlockedScopeImpl(abs_scope.AbstractOscilloscope):
    def is_channel_ready(self, channel: int) -> bool:
        return False

class UnblockedScopeImpl(abs_scope.AbstractOscilloscope):
    def is_channel_ready(self, channel: int) -> bool:
        return True

def test_block_ready():
    with pytest.raises(TimeoutError):
        BlockedScopeImpl().block_on_channel_ready(1, datetime.timedelta(seconds=1))

def test_block_not_ready():
    UnblockedScopeImpl().block_on_channel_ready(1, datetime.timedelta(seconds=0.1))
