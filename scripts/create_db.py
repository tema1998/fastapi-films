from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session

from api.config import DATABASE_URL


def main():
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())
    # engine = create_async_engine(DATABASE_URL, future=True, echo=True)
    # async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    session.execute(text("""create table users(
    id integer not null primary key,
    email varchar(256),
    password varchar(256),
    first_name varchar(256),
    last_name varchar(256),
    nickname varchar(256),
    created_at varchar(256)
    );"""))

    session.execute(text("""create table auth_token(
    id integer not null primary key,
    user_id integer references users,
    token varchar(256),
    created_at varchar(256)
    );"""))

    session.execute(text("""create table films(
    id integer not null primary key,
    user_id integer references users,
    title varchar(256),
    description varchar(256),
    created_at varchar(256)
    );"""))

    session.close()


if __name__ == '__main__':
    main()