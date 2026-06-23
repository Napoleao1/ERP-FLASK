from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    def set_senha(self, senha_limpa):
        self.senha_hash = generate_password_hash(senha_limpa)

    
    def checar_senha(self, senha_limpa):
        return check_password_hash(self.senha_hash, senha_limpa)
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email
        }