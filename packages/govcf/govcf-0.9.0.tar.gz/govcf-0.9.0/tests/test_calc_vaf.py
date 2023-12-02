from govcf.calculate_vaf import find
import pytest


def test_get_vcf_info_simple():
    call_info = {'AO': [0, 2379], 'RO': 12, 'DP': 2534}

    info_mapper = find(call_info.keys())
    assert info_mapper is not None

    obj = info_mapper(call_info, 2, "A")
    assert obj['ref_depth'] == 12
    assert obj['alt_depth'] == 2379
    assert obj['total_depth'] == 2534
    assert obj['vaf'] == 0.9388318863456985
    assert obj['vaf_alt'] == 0.9949811794228356


def test_get_vcf_info_simple_ad_rd():
    call_info = {'AD': [0, 2379], 'RD': 12, 'DP': 2534}

    info_mapper = find(call_info.keys())
    assert info_mapper is not None

    obj = info_mapper(call_info, 2, "A")
    assert obj['ref_depth'] == 12
    assert obj['alt_depth'] == 2379
    assert obj['total_depth'] == 2534
    assert obj['vaf'] == 0.9388318863456985
    assert obj['vaf_alt'] == 0.9949811794228356


def test_get_vcf_info_clcbio():
    call_info = {'GT': "1/2/3", 'CLCAD2': [0, 29, 29, 40], 'DP': 727}

    info_mapper = find(call_info.keys())
    assert info_mapper is not None

    obj = info_mapper(call_info, 1, "A")
    assert obj['ref_depth'] == 0
    assert obj['alt_depth'] == 29
    assert obj['total_depth'] == 727
    assert obj['vaf'] == 0.039889958734525444
    assert obj['vaf_alt'] == 1.0


def test_get_vcf_info_brli():
    call_info = {'AAC': 1, 'FRD': 0, 'FDP': 5829, 'FAD': [250], 'FAF': [0.043]}

    info_mapper = find(call_info.keys())
    assert info_mapper is not None

    obj = info_mapper(call_info, 1, "A")
    assert obj['ref_depth'] == 0
    assert obj['alt_depth'] == 250
    assert obj['total_depth'] == 5829
    assert obj['vaf'] == 0.04288900325956425
    assert obj['vaf_alt'] == 1.0


def test_populate_vafs_no_ref_depth():
    call_info = {'AO': [0, 2379], 'DP': 2534}

    info_mapper = find({"AO", "RO", "DP"})
    assert info_mapper is not None

    obj = info_mapper(call_info, 2, "A")
    assert obj['ref_depth'] is None
    assert obj['alt_depth'] == 2379
    assert obj['total_depth'] == 2534
    assert obj['vaf'] == 0.9388318863456985
    assert obj['vaf_alt'] == 0.9388318863456985


def test_populate_vafs_no_alt_depth():
    call_info = {'RO': 12, 'DP': 2534}

    info_mapper = find({"AO", "RO", "DP"})
    assert info_mapper is not None

    obj = info_mapper(call_info, 1, "A")
    assert obj['ref_depth'] == 12
    assert obj['alt_depth'] is None
    assert obj['total_depth'] == 2534
    assert obj['vaf'] is None
    assert obj['vaf_alt'] is None


def test_populate_vafs_no_alt_ref_depth():
    call_info = {'DP': 2534}

    info_mapper = find({"AO", "RO", "DP"})
    assert info_mapper is not None

    obj = info_mapper(call_info, 1, "A")
    assert obj['ref_depth'] is None
    assert obj['alt_depth'] is None
    assert obj['total_depth'] == 2534
    assert obj['vaf'] is None
    assert obj['vaf_alt'] is None


def test_populate_vafs_no_alt_ref_total_depth():
    call_info = {}

    info_mapper = find({"AO", "RO", "DP"})
    assert info_mapper is not None

    obj = info_mapper(call_info, 1, "A")
    assert obj['ref_depth'] is None
    assert obj['alt_depth'] is None
    assert obj['total_depth'] is None
    assert obj['vaf'] is None
    assert obj['vaf_alt'] is None


def test_populate_vafs_no_total_depth():
    call_info = {'AO': [0, 2379], 'RO': 12}

    info_mapper = find({"AO", "RO", "DP"})
    assert info_mapper is not None

    obj = info_mapper(call_info, 2, "A")
    assert obj['ref_depth'] == 12
    assert obj['alt_depth'] == 2379
    assert obj['total_depth'] is None
    assert obj['vaf'] == 0.9949811794228356
    assert obj['vaf_alt'] == 0.9949811794228356


def test_get_vcf_info_usc():
    call_info = {'AD': [105, 14], 'DP': 119}

    info_mapper = find({"AD", "DP"})
    assert info_mapper is not None

    obj = info_mapper(call_info, 1, "A")
    assert obj['ref_depth'] == 105
    assert obj['alt_depth'] == 14
    assert obj['total_depth'] == 119
    assert obj['vaf'] == pytest.approx(0.117647058823529)
    assert obj['vaf_alt'] == pytest.approx(0.117647058823529)


def test_get_vcf_info_usc_alt2():
    call_info = {'AD': [100, 10, 20], 'DP': 130}

    info_mapper = find({"AD", "DP"})
    assert info_mapper is not None

    obj = info_mapper(call_info, 2, "A")
    assert obj['ref_depth'] == 100
    assert obj['alt_depth'] == 20
    assert obj['total_depth'] == 130
    assert obj['vaf'] == pytest.approx(0.153846153846154)
    assert obj['vaf_alt'] == pytest.approx(0.166666666666667)


def test_strelka():
    call_info = {'TIR': [38, 42], 'DP': 146}

    info_mapper = find({"TIR", "DP", "AU", "CU", "GU", "TU"})
    assert info_mapper is not None

    obj = info_mapper(call_info, 1, "A")
    assert obj['ref_depth'] == 108
    assert obj['alt_depth'] == 38
    assert obj['total_depth'] == 146
    assert obj['vaf'] == pytest.approx(0.2602739726027397)
    assert obj['vaf_alt'] == pytest.approx(0.2602739726027397)

    call_info = {'DP': 106, 'AU': [0, 0], 'CU': [45, 46], 'GU': [60, 60], 'TU': [0, 0]}

    obj = info_mapper(call_info, 1, "C")
    assert obj['ref_depth'] == 61
    assert obj['alt_depth'] == 45
    assert obj['total_depth'] == 106
    assert obj['vaf'] == pytest.approx(0.42452830188679247)
    assert obj['vaf_alt'] == pytest.approx(0.42452830188679247)


def test_pheo():
    call_info = {'DP': 35, 'DP4': [13, 11, 6, 3]}

    info_mapper = find(call_info.keys())
    assert info_mapper is not None

    obj = info_mapper(call_info, 1, "T")
    assert obj['ref_depth'] == 24
    assert obj['alt_depth'] == 9
    assert obj['total_depth'] == 35
    assert obj['vaf'] == pytest.approx(9.0 / 35)
    assert obj['vaf'] == pytest.approx(0.2571428571428571)
    assert obj['vaf_alt'] == pytest.approx(0.2727272727272727)


def test_fao_fdp():
    call_info = {'FAO': 173, 'FDP': 1858}

    info_mapper = find(call_info.keys())
    assert info_mapper is not None

    obj = info_mapper(call_info, 1, "T")
    assert obj['ref_depth'] == 1858 - 173
    assert obj['alt_depth'] == 173
    assert obj['total_depth'] == 1858
    assert obj['vaf'] == pytest.approx(173 / 1858)
    assert obj['vaf'] == pytest.approx(0.09311087190527449)
    assert obj['vaf_alt'] == pytest.approx(0.09311087190527449)


def test_fao_fdp_fro():
    call_info = {'FAO': [0, 173], 'FDP': 1858, 'FRO': 1600}

    info_mapper = find(call_info.keys())
    assert info_mapper is not None

    obj = info_mapper(call_info, 2, "T")
    assert obj['ref_depth'] == 1600
    assert obj['alt_depth'] == 173
    assert obj['total_depth'] == 1858
    assert obj['vaf'] == pytest.approx(173 / 1858)
    assert obj['vaf_alt'] == pytest.approx(173 / (1600 + 173))
