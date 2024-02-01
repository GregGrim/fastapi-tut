import database


def update_db():
    return database.Base.metadata.create_all(bind=database.engine)


if __name__ == '__main__':
    update_db()
