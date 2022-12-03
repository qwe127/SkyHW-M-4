from app.dao.models.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, did):
        return self.session.query(Director).get(did)

    def get_all(self):
        return self.session.query(Director).all()

    def get_12(self, pid: int):
        if pid == 1:
            return self.session.query(Director).limit(12).all()
        if pid >= 2:
            return self.session.query(Director).limit(12).offset((pid - 1) * 12).all()

    def create(self, data):
        director = Director(**data)

        self.session.add(director)
        self.session.commit()

        return director

    def update(self, director):
        self.session.add(director)
        self.session.commit()

        return director

    def delete(self, did):
        director = self.get_one(did)

        self.session.delete(director)
        self.session.commit()

        return director
