from emcpy.utils.utils import float10Power, roundNumber

float10Power_values = [
    (1.0, -1.),
    (10.1, 1.),
    (100.2, 2.),
    (1000.3, 3.),
    (10000.4, 4.),
]

roundNumber_values = [
    (0.01231, 0.01),
    (0.0164, 0.02),
    (2.3, 2.0),
    (2.8, 3.0),
    (6.2, 6.0),
    (12.8, 10.0),
    (16.8, 20.0),
    (59, 60),
    (141, 100),
    (161, 200),
]


def evaluate_float10Power(index):
    assert float10Power_values[index][1] == float10Power(
        float10Power_values[index][0])


def test_float10Power_00():
    evaluate_float10Power(0)


def test_float10Power_01():
    evaluate_float10Power(1)


def test_float10Power_02():
    evaluate_float10Power(2)


def test_float10Power_03():
    evaluate_float10Power(3)


def test_float10Power_04():
    evaluate_float10Power(4)


def evaluate_roundNumber(index):
    assert roundNumber_values[index][1] == roundNumber(
        roundNumber_values[index][0])


def test_roundNumber_00():
    evaluate_roundNumber(0)


def test_roundNumber_01():
    evaluate_roundNumber(1)


def test_roundNumber_02():
    evaluate_roundNumber(2)


def test_roundNumber_03():
    evaluate_roundNumber(3)


def test_roundNumber_04():
    evaluate_roundNumber(4)


def test_roundNumber_05():
    evaluate_roundNumber(5)


def test_roundNumber_06():
    evaluate_roundNumber(6)


def test_roundNumber_07():
    evaluate_roundNumber(7)


def test_roundNumber_08():
    evaluate_roundNumber(8)


def test_roundNumber_09():
    evaluate_roundNumber(9)
