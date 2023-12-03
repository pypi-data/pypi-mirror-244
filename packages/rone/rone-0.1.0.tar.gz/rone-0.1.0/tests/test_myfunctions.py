from mypythonlib import myfunctions


def test_square():
    assert myfunctions.square(2) == 4
    assert myfunctions.square(0) == 0
    assert myfunctions.square(123.456) == 15241.383936
    assert myfunctions.square(-54.321) == 2950.771041
