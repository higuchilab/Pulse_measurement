from sqlalchemy import (
    Integer,
    Text,
    Uuid,
    ForeignKey,
    DateTime,
    Float,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )
    samples: Mapped[list["Sample"]] = relationship(
        back_populates="material",
    )


class Sample(Base):
    __tablename__ = "samples"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )
    material_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("materials.id"),
        nullable=False
    )
    material: Mapped["Material"] = relationship(back_populates="samples")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )


class PulseTemplete(Base):
    __tablename__ = "pulse_templetes"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    top_voltage: Mapped[float] = mapped_column(Float, nullable=False)
    top_time: Mapped[float] = mapped_column(Float, nullable=False)
    base_voltage: Mapped[float] = mapped_column(Float, nullable=False)
    base_time: Mapped[float] = mapped_column(Float, nullable=False)
    loop: Mapped[int] = mapped_column(Integer, nullable=False)
    interval_time: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "top_voltage", "top_time", "base_voltage", "base_time", "loop", "interval_time"
        ),
        CheckConstraint("top_time >= 0"),
        CheckConstraint("base_time >= 0"),
        CheckConstraint("loop > 0"),
        CheckConstraint("interval_time >= 0"),
    )


class SweepTemplete(Base):
    __tablename__ = "sweep_templetes"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    top_voltage: Mapped[float] = mapped_column(Float, nullable=False)
    bottom_voltage: Mapped[float] = mapped_column(Float, nullable=False)
    voltage_step: Mapped[float] = mapped_column(Float, nullable=False)
    loop: Mapped[int] = mapped_column(Integer, nullable=False)
    tick_time: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "top_voltage", "bottom_voltage", "voltage_step", "loop", "tick_time"
        ),
        CheckConstraint("voltage_step > 0"),
        CheckConstraint("loop > 0"),
        CheckConstraint("tick_time >= 0"),
    )


class MeasureType(Base):
    __tablename__ = "measure_types"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )


class History(Base):
    """
    測定履歴\n
    測定者、物質名、試料名、測定名、備考を記録する
    """
    __tablename__ = "history"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    sample_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("samples.id"), nullable=False)
    measure_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("measure_types.id"), nullable=False)
    discription: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )


class TwoTerminalResult(Base):
    __tablename__ = "two_terminal_results"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    history_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("history.id"), nullable=False)
    elapsed_time: Mapped[float] = mapped_column(Float, nullable=True)
    voltage: Mapped[float] = mapped_column(Float, nullable=True)
    current: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )


class FourTerminalResult(Base):
    __tablename__ = "four_terminal_results"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    history_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("history.id"), nullable=False)
    elapsed_time: Mapped[float] = mapped_column(Float, nullable=True)
    voltage_1: Mapped[float] = mapped_column(Float, nullable=True)
    current_1: Mapped[float] = mapped_column(Float, nullable=True)
    voltage_2: Mapped[float] = mapped_column(Float, nullable=True)
    current_2: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )

class EchoStateResult(Base):
    """
    echo state測定結果
    """
    __tablename__ = "echo_state_results"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    history_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("history.id"), nullable=False)
    elapsed_time: Mapped[float] = mapped_column(Float, nullable=True)
    discrete_time: Mapped[int] = mapped_column(Integer, nullable=True)
    node_id: Mapped[int] = mapped_column(Integer, nullable=True)
    voltage: Mapped[float] = mapped_column(Float, nullable=True)
    current: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )


class NarmaTemplete(Base):
    __tablename__ = "narma_templetes"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    tot_discrete_time: Mapped[int] = mapped_column(Integer, nullable=False)
    top_voltage: Mapped[float] = mapped_column(Float, nullable=False)
    bottom_voltage: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("tot_discrete_time", "top_voltage", "bottom_voltage"),
    )


class NarmaInputArray(Base):
    __tablename__ = "narma_input_array"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    narma_templete_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("narma_templetes.id"), nullable=False)
    discrete_time: Mapped[int] = mapped_column(Integer, nullable=False)
    input_voltage: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")),
        nullable=False,
    )
