import main

def test_get_distance():
    start = 334,200
    end = 200,102

    assert int(main.get_distance(start, end)) == 166