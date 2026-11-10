from itertools import combinations

import pytest

import core
import data


def _pairs(rounds):
    return [frozenset(pair) for pairs in rounds for pair in pairs]


@pytest.mark.parametrize("n", [2, 4, 6, 8, 10, 12, 16, 20])
def test_full_schedule_is_a_complete_round_robin(n):
    teams = [str(i) for i in range(1, n + 1)]
    rounds = core.build_schedule(teams, n - 1)

    pairs = _pairs(rounds)

    # Nobody meets twice, and everybody meets everybody
    assert len(pairs) == len(set(pairs))
    assert set(pairs) == {frozenset(p) for p in combinations(teams, 2)}


@pytest.mark.parametrize("n", [4, 10, 16])
def test_each_team_plays_once_per_round(n):
    teams = [str(i) for i in range(1, n + 1)]

    for pairs in core.build_schedule(teams, n - 1):
        playing = [team for pair in pairs for team in pair]
        assert sorted(playing) == sorted(teams)


def test_partial_schedule_has_no_duplicates():
    teams = [str(i) for i in range(1, 11)]

    for rounds_number in range(1, 10):
        pairs = _pairs(core.build_schedule(teams, rounds_number))
        assert len(pairs) == len(set(pairs))


def test_too_many_rounds_is_refused():
    teams = [str(i) for i in range(1, 9)]

    with pytest.raises(ValueError):
        core.build_schedule(teams, 8)


def test_odd_number_of_teams_is_refused():
    with pytest.raises(ValueError):
        core.build_schedule(["1", "2", "3"], 1)


def test_max_rounds():
    assert core.max_rounds(2) == 1
    assert core.max_rounds(10) == 9
    assert core.max_rounds(7) == 7  # "IMPAIR" team added: 8 teams
    assert core.max_rounds(0) == 0


def test_tables_needed():
    assert core.tables_needed(10) == 5
    assert core.tables_needed(7) == 3  # the "IMPAIR" team does not play


def _fake_tournament(monkeypatch, teams_number, rounds_number):
    stored = []
    cleared = []
    teams = [(i, "T", f"a{i}", f"b{i}") for i in range(1, teams_number + 1)]

    monkeypatch.setattr(data, "get_teams", lambda name: list(teams))
    monkeypatch.setattr(data, "get_rounds", lambda name: rounds_number)
    monkeypatch.setattr(data, "clear_repartition", lambda name: cleared.append(name))
    monkeypatch.setattr(data, "update_repartition", lambda name, r, t, pair: stored.append((r, t, pair)))

    return stored, cleared


def test_generate_repartition_never_repeats_a_match(monkeypatch):
    stored, _ = _fake_tournament(monkeypatch, teams_number=10, rounds_number=9)

    core.generate_repartition("T")

    pairs = [frozenset(eval(pair)) for _, _, pair in stored]
    assert len(pairs) == 9 * 5
    assert len(pairs) == len(set(pairs))


def test_generate_repartition_caps_rounds(monkeypatch):
    stored, _ = _fake_tournament(monkeypatch, teams_number=6, rounds_number=20)

    core.generate_repartition("T")

    assert {r for r, _, _ in stored} == {1, 2, 3, 4, 5}


def test_generate_repartition_only_clears_its_own_tournament(monkeypatch):
    _, cleared = _fake_tournament(monkeypatch, teams_number=4, rounds_number=3)

    core.generate_repartition("T")

    assert cleared == ["T"]
