from pic_template.chips.top import top

def test_top_builds():
    """Test that the top-level chip builds without errors."""
    c = top()
    assert c is not None
    # Component builds successfully if we can access its bounding box
    assert c.bbox is not None


