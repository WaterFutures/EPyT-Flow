import nox


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"])
def test(session):
    session.install(".")
    session.install("-rREQUIREMENTS-DEV.txt")

    session.run("pytest", "tests/")
