# tests/layers_test.py
from pic_template.pdk.layers import LAYER

def test_layers_are_valid_gds_layers():
    for name in dir(LAYER):
        if name.startswith('_'):
            continue
        value = getattr(LAYER, name)
        if not isinstance(value, tuple):
            continue
        assert isinstance(value, tuple), f"{name} does not resolve to (layer, datatype)"
        assert len(value) == 2
        assert all(isinstance(v, int) for v in value)


def test_no_duplicate_layers():
    seen = {}

    for name in dir(LAYER):
        if name.startswith('_'):
            continue
        value = getattr(LAYER, name)
        if not isinstance(value, tuple):
            continue
        if value in seen:
            raise AssertionError(
                f"Duplicate layer {value}: {name} and {seen[value]}"
            )
        seen[value] = name
