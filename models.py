from config import db

class usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    lastname = db.Column(db.String(100), unique=False, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "nombre": self.nombre,  
            "email": self.email,
        }
