
import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class Department(myBase):
    __tablename__ = 'departments'

    department_id = sa.Column(
        sa.Integer, sa.Identity(always=True), primary_key=True
    )

    name = sa.Column(sa.Text, nullable=False)
    
    faculty_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('faculties.faculty_id', ondelete='CASCADE'),
        nullable=False
    )

    faculty = orm.relationship('Faculty', back_populates='departments')
    
    specialties = orm.relationship(
        'Specialty', back_populates='department', passive_deletes=True
    )

    __table_args__ = (
        sa.UniqueConstraint('faculty_id', 'name'),
    )