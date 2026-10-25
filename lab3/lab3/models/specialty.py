import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class Specialty(myBase):
    __tablename__ = 'specialties'

    specialty_id = sa.Column(
        sa.Integer, sa.Identity(always=True), primary_key=True
    )
    department_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('departments.department_id', ondelete='CASCADE'),
        nullable=False
    )
    code = sa.Column(sa.Text, nullable=False, unique=True)
    name = sa.Column(sa.Text, nullable=False)

    department = orm.relationship(
        'Department', back_populates='specialties'
    )
    groups = orm.relationship(
        'StudentGroup', back_populates='specialty', passive_deletes=True
    )