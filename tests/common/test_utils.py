import common

def test_repartition_ast():
    repartition = [
        (1, 1, 1, "('1', '2')"),
        (1, 1, 2, "('3', '4')"),
    ]

    result = common.repartition_ast(repartition)

    assert result == [
        {"tournament": 1, "round": 1, "table": 1, "team1": "1", "team2": "2"},
        {"tournament": 1, "round": 1, "table": 2, "team1": "3", "team2": "4"},
    ]