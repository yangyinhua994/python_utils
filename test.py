def test(s: str):
    str = ""
    for e in s.split("_"):
        str += e.capitalize()
    return str


print(test("s_ss"))
