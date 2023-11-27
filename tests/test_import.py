"""Test astro-dataset."""

import astro_dataset


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(astro_dataset.__name__, str)
