import pytest
from govcf import BEDFilter, iterate_vcf_calls
import os


TEST_BED = os.path.join(os.path.dirname(__file__), "bed/test.bed")
TEST_VCF = os.path.join(os.path.dirname(__file__), "bed/test.vcf")


def test_bed_filter():
    bed = BEDFilter(TEST_BED, padding=0)
    assert bed((9, 133588266))
    assert (9, 133588266) in bed
    assert list(filter(bed, [(9, 133588266), (9, 1)])) == [(9, 133588266)]

    iterator = iterate_vcf_calls(TEST_VCF, bed_filter=bed)

    header = next(iterator)
    assert header.get("file_path") == os.path.realpath(TEST_VCF)

    call = next(iterator)
    assert call.get("chr") == "2"

    with pytest.raises(StopIteration):
        next(iterator)
