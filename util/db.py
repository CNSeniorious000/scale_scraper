try:
    from ..secret import host, port, db, user, password, dialct, driver
except ImportError:
    from sys import path

    path.append("..")
    from secret import host, port, db, user, password, dialct, driver

from sqlmodel import create_engine, Session, SQLModel, Field

url = f"{dialct}+{driver}://{user}:{password}@{host}:{port}/{db}"

# url = "sqlite:///database.db"
# url = f"{dialct}+{driver}://root@localhost:{port}/mysql"

engine = create_engine(url)


def create_all():
    return SQLModel.metadata.create_all(engine)


__all__ = ["engine", "create_all", "SQLModel", "Field", "Session"]

if __name__ == '__main__':
    from random import randrange


    class RandomPerson(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
        random: int


    create_all()

    with Session(engine, future=True, expire_on_commit=True) as session:
        import time

        t = time.perf_counter()
        n = 200
        for i in range(n):
            session.add(RandomPerson(name=f"name_{i}", random=randrange(12345)))
        session.commit()
        print(n / (time.perf_counter() - t))
        print("|", end="", flush=True)
