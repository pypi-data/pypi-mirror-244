import vegacandle4

def test_say_hello():
    try:
        vegacandle4.addfunc.sayHello()
        assert True
    except:
        assert False