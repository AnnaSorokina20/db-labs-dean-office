import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class Subject(myBase):
    __tablename__ = 'subjects'

    subject_id = sa.Column(
        sa.Integer, sa.Identity(always=True), primary_key=True
    )
    name = sa.Column(sa.Text, nullable=False, unique=True)

    group_subjects = orm.relationship(
        'GroupSubject', back_populates='subject', passive_deletes=True
    )