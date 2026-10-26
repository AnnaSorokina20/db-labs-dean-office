import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class StudentGroup(myBase):
    __tablename__ = 'student_groups'

    group_id = sa.Column(
        sa.Integer, sa.Identity(always=True), primary_key=True
    )
    specialty_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('specialties.specialty_id', ondelete='CASCADE'),
        nullable=False
    )
    group_number = sa.Column(sa.Text, nullable=False, unique=True)
    formation_year = sa.Column(sa.Integer, nullable=False)

    specialty = orm.relationship(
        'Specialty', back_populates='groups'
    )
    students = orm.relationship(
        'Student', back_populates='group', passive_deletes=True
    )
    group_subjects = orm.relationship(
        'GroupSubject', back_populates='group', passive_deletes=True
    )

    __table_args__ = (
        sa.CheckConstraint('formation_year > 2000'),
    )