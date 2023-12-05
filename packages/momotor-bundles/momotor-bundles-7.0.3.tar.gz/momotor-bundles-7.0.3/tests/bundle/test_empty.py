import pytest

from momotor.bundles import ResultsBundle
from momotor.bundles.exception import BundleLoadError

from bundle_test_helpers import parametrize_use_lxml


@parametrize_use_lxml
def test_empty_results(use_lxml):
    with pytest.raises(BundleLoadError):
        ResultsBundle.from_bytes_factory(b'', use_lxml=use_lxml, legacy=False)
