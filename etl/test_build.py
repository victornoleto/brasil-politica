"""ETL sanity: seat-equivalents per year match the size of each institution."""
import pytest

import build


@pytest.fixture(scope="module")
def comp():
    return build.composition([*build.presidency(), *build.chamber(), *build.senate()])


def total(comp, inst, year):
    return sum(comp[inst][year].values())


@pytest.mark.parametrize("year", build.YEARS)
def test_presidency_one_per_year(comp, year):
    assert total(comp, "presidency", year) == pytest.approx(1, abs=0.01)


@pytest.mark.parametrize("year", build.YEARS)
def test_chamber_513(comp, year):
    assert 490 <= total(comp, "chamber", year) <= 525


@pytest.mark.parametrize("year", build.YEARS)
def test_senate_81(comp, year):
    assert 76 <= total(comp, "senate", year) <= 84


def test_president_2025_pt(comp):
    assert comp["presidency"][2025] == {"PT": pytest.approx(1)}


def test_aliases():
    assert build.canon("PMDB") == "MDB"
    assert build.canon("PFL") == "DEM"
    assert build.canon("PL*") == build.canon("PR") == "PL"
    assert build.canon("PSD*") != build.canon("PSD")
    assert build.canon(None) == "NO_PARTY"


@pytest.fixture(scope="module")
def comp_state():
    return build.composition(list(build.state_level()))


# 1994 has no data: the mandate in force came from the 1990 election, outside the time range
@pytest.mark.parametrize("year", range(1995, 2027))
def test_governors_27(comp_state, year):
    assert total(comp_state, "governors", year) == pytest.approx(27, abs=0.05)


@pytest.mark.parametrize("year", range(1996, 2027))
def test_assemblies_1059(comp_state, year):
    assert 1040 <= total(comp_state, "assemblies", year) <= 1065


def test_special_election_to_2018(comp_state):
    # Carlesse (PHS) won the TO special election on 2018-06-24: ~52% of the year
    assert comp_state["governors"][2018]["PHS"] == pytest.approx(191 / 365, abs=0.01)
