from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    _tablename_ = 'heroes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    super_name = Column(String)

    hero_powers = relationship('HeroPower', back_populates='hero')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }

    def _repr_(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    _tablename_ = 'powers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column (String)

    hero_powers = relationship('HeroPower', back_populates='power')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return description

    def _repr_(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    _tablename_ = 'hero_powers'

    id = Column(Integer, primary_key=True)
    strength = Column(String, nullable=False)
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    power_id = Column(Integer, ForeignKey('powers.id'))

    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    def serialize(self):
        return {
            'id': self.id,
            'strength': self.strength,
            'hero_id': self.hero_id,
            'power_id': self.power_id
        }

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError(f'Strength must be one of {", ".join(valid_strengths)}')
        return strength

    def _repr_(self):
        return f'<HeroPower {self.id}>'
    