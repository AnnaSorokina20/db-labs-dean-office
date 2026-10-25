import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class Student(myBase):
    __tablename__ = 'students'

    student_id = sa.Column(
        sa.Integer, sa.Identity(always=True), primary_key=True
    )
    record_book_number = sa.Column(
        sa.Text, nullable=False, unique=True
    )
    group_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('student_groups.group_id', ondelete='CASCADE'),
        nullable=False
    )

    last_name = sa.Column(sa.Text, nullable=False)
    first_name = sa.Column(sa.Text, nullable=False)
    patronymic = sa.Column(sa.Text)

    permanent_city = sa.Column(sa.Text, nullable=False)
    permanent_street = sa.Column(sa.Text, nullable=False)
    permanent_building = sa.Column(sa.Text, nullable=False)

    current_city = sa.Column(sa.Text, nullable=False)
    current_street = sa.Column(sa.Text, nullable=False)
    current_building = sa.Column(sa.Text, nullable=False)

    scholarship_percent = sa.Column(
        sa.Integer, nullable=False, server_default=sa.text('0')
    )

    group = orm.relationship(
        'StudentGroup', back_populates='students'
    )
    session_results = orm.relationship(
        'SessionResult', back_populates='student', passive_deletes=True
    )

    __table_args__ = (
        sa.CheckConstraint('scholarship_percent IN (0, 100, 150, 200)'),
    )