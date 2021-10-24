import nox


@nox.session
def test(session):
    session.install("-e", ".[testing]")
    session.run("pytest", "--cov=rebecca.apispec", "--cov-report=term-missing")


@nox.session
def lint(session):
    session.install("-e", ".[dev]")
    session.run("flake8", "rebecca/apispec")
    session.run("black", "--check", "--diff", "rebecca/apispec")
