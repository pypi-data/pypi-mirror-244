import json
import os

import pytest

from govcf.variant_files import (
    iterate_vcf_calls,
    iterate_vcf_files,
    ensure_collection,
    determine_zyg,
    format_GT,
    SampleSubstitute,
)

VCF_DIR = os.path.join(os.path.dirname(__file__), "vcfs")


@pytest.mark.parametrize(
    "input_vcf",
    [
        os.path.join(VCF_DIR, fname)
        for fname in sorted(os.listdir(VCF_DIR))
        if fname.endswith(".vcf")
    ],
)
def test_iter_calls(input_vcf):
    assert os.path.isfile(input_vcf)
    filename = os.path.basename(input_vcf)[:-4]

    # create actual json
    all_records = []
    for records in [
        rec
        for rec in iterate_vcf_calls(input_vcf, include_vaf=True)
        if rec.get("__type__") != "SKIPPED_CALL"
    ]:
        # file path has "real" path which won't work
        records.pop("file_path", None)
        records.pop("__record__", None)  # not in expected output
        all_records.append(records)

    actual = json.dumps(all_records, indent=4, sort_keys=True)

    # assemble expect json
    output_calls = os.path.join(VCF_DIR, "{}.json".format(filename))
    assert os.path.isfile(output_calls), "No Output: {}".format(filename)
    expect = json.load(open(output_calls))
    expect = json.dumps(expect, indent=4, sort_keys=True)

    assert expect == actual, "{} Mismatch:\n{}\n".format(filename, actual)


def test_iter_files():
    file_paths = [
        os.path.join(VCF_DIR, "annotated.vcf"),
        os.path.join(VCF_DIR, "pheo.vcf"),
        os.path.join(VCF_DIR, "spec.vcf"),
    ]

    counts = dict(HEADER=0, CALL=0)
    for record in [
        rec
        for rec in iterate_vcf_files(file_paths)
        if rec.get("__type__") != "SKIPPED_CALL"
    ]:
        counts[record.get("__type__")] += 1
    assert counts == dict(HEADER=3, CALL=16)


def test_ensure_collection():
    assert ensure_collection(None) == []
    assert ensure_collection(iter(range(3))) == [0, 1, 2]
    assert ensure_collection(1) == [1]
    assert ensure_collection((1, 2)) == (1, 2)


def test_determine_zyg():
    assert determine_zyg((1,)) == "hemizygous"
    assert determine_zyg((1, None)) == "unknown"
    assert determine_zyg((None, 1)) == "unknown"
    assert determine_zyg((1, 2)) == "heterozygous"
    assert determine_zyg((2, 2)) == "homozygous"


def test_format_GT():
    info = {"GT": (1, 2)}
    sample = SampleSubstitute(name="sample", phased=True)

    info2 = {"GT": (2, None)}
    sample2 = SampleSubstitute(name="sample2", phased=False)

    assert format_GT(info, sample) == "1|2"
    assert format_GT(info2, sample2) == "2/."
