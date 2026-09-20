from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


# ============================================================
# BATCH
# ============================================================

class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    program: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # Relationship
    # One Batch -> Many Students
    # --------------------------------------------------------

    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="batch",
        cascade="all, delete-orphan",
    )


# ============================================================
# COURSE
# ============================================================

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # Relationship
    # One Course -> Many Attendance Records
    # --------------------------------------------------------

    attendance: Mapped[list["Attendance"]] = relationship(
        "Attendance",
        back_populates="course",
        cascade="all, delete-orphan",
    )


# ============================================================
# STUDENT
# ============================================================

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    usn: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    branch: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    semester: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    batch_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "batches.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # Relationship
    # Student -> Batch
    # --------------------------------------------------------

    batch: Mapped["Batch | None"] = relationship(
        "Batch",
        back_populates="students",
    )

    # --------------------------------------------------------
    # Relationship
    # Student -> Attendance
    # One Student -> Many Attendance Records
    # --------------------------------------------------------

    attendance: Mapped[list["Attendance"]] = relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    # --------------------------------------------------------
    # Relationship
    # Student -> Activity Submissions
    # One Student -> Many Submissions
    # --------------------------------------------------------

    submissions: Mapped[list["ActivitySubmission"]] = relationship(
        "ActivitySubmission",
        back_populates="student",
        cascade="all, delete-orphan",
    )


# ============================================================
# ATTENDANCE
# ============================================================

class Attendance(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    course_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "courses.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    subject: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # Relationship
    # Attendance -> Student
    # --------------------------------------------------------

    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="attendance",
    )

    # --------------------------------------------------------
    # Relationship
    # Attendance -> Course
    # --------------------------------------------------------

    course: Mapped["Course | None"] = relationship(
        "Course",
        back_populates="attendance",
    )

    # --------------------------------------------------------
    # Constraints and Indexes
    # --------------------------------------------------------

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "course_id",
            "attendance_date",
            name="uq_student_course_attendance_date",
        ),

        Index(
            "ix_attendance_student_date",
            "student_id",
            "attendance_date",
        ),
    )


# ============================================================
# ACTIVITY
# ============================================================

class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    activity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    max_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    activity_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # Relationship
    # Activity -> Submissions
    # One Activity -> Many Student Submissions
    # --------------------------------------------------------

    submissions: Mapped[list["ActivitySubmission"]] = relationship(
        "ActivitySubmission",
        back_populates="activity",
        cascade="all, delete-orphan",
    )


# ============================================================
# ACTIVITY SUBMISSION
# ============================================================

class ActivitySubmission(Base):
    __tablename__ = "activity_submissions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    activity_id: Mapped[int] = mapped_column(
        ForeignKey(
            "activities.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    score: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    submission_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # --------------------------------------------------------
    # Relationship
    # Submission -> Student
    # --------------------------------------------------------

    student: Mapped["Student"] = relationship(
        "Student",
        back_populates="submissions",
    )

    # --------------------------------------------------------
    # Relationship
    # Submission -> Activity
    # --------------------------------------------------------

    activity: Mapped["Activity"] = relationship(
        "Activity",
        back_populates="submissions",
    )

    # --------------------------------------------------------
    # Constraint
    #
    # One student can have only one submission
    # for a particular activity.
    # --------------------------------------------------------

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "activity_id",
            name="uq_student_activity_submission",
        ),
    )
