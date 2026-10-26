import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class Faculty(myBase):
    __tablename__ = 'faculties'

    faculty_id = sa.Column(
        sa.Integer, sa.Identity(always=True), primary_key=True
    )
    name = sa.Column(sa.Text, nullable=False, unique=True)

    departments = orm.relationship(
        'Department', back_populates='faculty', passive_deletes=True
    )