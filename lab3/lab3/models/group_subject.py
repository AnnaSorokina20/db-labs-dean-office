import sqlalchemy as sa
from sqlalchemy import orm
from .base import myBase


class GroupSubject(myBase):
    __tablename__ = 'group_subjects'

    group_subject_id = sa.Column(
        sa.Integer, sa.Identity(always=True), primary_key=True
    )
    group_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('student_groups.group_id', ondelete='CASCADE'),
        nullable=False
    )
    subject_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('subjects.subject_id', ondelete='CASCADE'),
        nullable=False
    )
    assessment_type = sa.Column(sa.Text, nullable=False)

    group = orm.relationship(
        'StudentGroup', back_populates='group_subjects'
    )
    subject = orm.relationship(
        'Subject', back_populates='group_subjects'
    )
    session_results = orm.relationship(
        'SessionResult',
        back_populates='group_subject',
        passive_deletes=True
    )

    __table_args__ = (
        sa.UniqueConstraint('group_id', 'subject_id'),
        sa.CheckConstraint("assessment_type IN ('exam', 'credit')"),
    )