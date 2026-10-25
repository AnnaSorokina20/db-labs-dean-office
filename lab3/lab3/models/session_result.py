import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class SessionResult(myBase):
    __tablename__ = 'session_results'

    result_id = sa.Column(
        sa.Integer, sa.Identity(always=True), primary_key=True
    )
    student_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('students.student_id', ondelete='CASCADE'),
        nullable=False
    )
    group_subject_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('group_subjects.group_subject_id', ondelete='CASCADE'),
        nullable=False
    )
    grade = sa.Column(sa.Integer)
    credit_passed = sa.Column(sa.Boolean)

    student = orm.relationship(
        'Student', back_populates='session_results'
    )
    group_subject = orm.relationship(
        'GroupSubject', back_populates='session_results'
    )

    __table_args__ = (
        sa.UniqueConstraint('student_id', 'group_subject_id'),
        sa.CheckConstraint('grade BETWEEN 2 AND 5'),
        sa.CheckConstraint(
            '(grade IS NOT NULL AND credit_passed IS NULL) OR '
            '(grade IS NULL AND credit_passed IS NOT NULL)'
        ),
    )