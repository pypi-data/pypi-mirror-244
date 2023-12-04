from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTableUUID, SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Table, text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from syndb_api import IN_CLUSTER
from syndb_api.database.base_model import Base
from syndb_api.neurodata.model import (
    dataset_collection_group_association_table,
    dataset_group_association_table,
    user_publication_association_table,
)

if TYPE_CHECKING:
    from syndb_api.neurodata.model import Dataset, DatasetCollection, Publication

user_group_association_table = Table(
    "user_group_association_table",
    Base.metadata,
    Column("group_name", ForeignKey("owner_group.name"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("is_executive", Boolean(), default=False, nullable=False),
    Column("is_moderator", Boolean(), default=False, nullable=False),
)


class OwnerGroup(Base):
    __tablename__ = "owner_group"

    name: Mapped[str] = mapped_column(primary_key=True)

    admin_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    admin: Mapped["User"] = relationship(back_populates="admin_groups")

    members: Mapped[list["User"]] = relationship(
        back_populates="groups",
        secondary=user_group_association_table,
        primaryjoin=user_group_association_table.c.group_name == name,
        secondaryjoin="user_group_association_table.c.user_id == User.id",
    )

    institution: Mapped[Optional[str]] = mapped_column(nullable=True)

    authorized_datasets: Mapped[list["Dataset"]] = relationship(
        back_populates="authorized_groups",
        secondary=dataset_group_association_table,
    )
    authorized_dataset_collections: Mapped[list["DatasetCollection"]] = relationship(
        back_populates="authorized_groups",
        secondary=dataset_collection_group_association_table,
    )


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    __tablename__ = "oauth_account"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    scientist_tag: Mapped[Optional[str]] = mapped_column(unique=True, index=True)
    has_profile_picture: Mapped[bool] = mapped_column(default=False)

    admin_groups: Mapped[list[OwnerGroup]] = relationship(back_populates="admin")

    owned_datasets: Mapped[list["Dataset"]] = relationship(back_populates="owner")
    owned_dataset_collections: Mapped[list["DatasetCollection"]] = relationship(back_populates="owner")
    total_uploaded_units: Mapped[int] = mapped_column(Integer(), default=0)

    publications: Mapped[list["Publication"]] = relationship(
        back_populates="authors", secondary=user_publication_association_table
    )

    excommunicated: Mapped[bool] = mapped_column(default=False)
    created_on: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_on: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    groups: Mapped[list[OwnerGroup]] = relationship(back_populates="members", secondary=user_group_association_table)

    has_academic: Mapped[bool] = mapped_column(Boolean(), default=False)
    academic_accounts: Mapped[list["AcademicAccount"]] = relationship(back_populates="user", lazy="select")

    oauth_accounts: Mapped[list[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")

    if IN_CLUSTER:

        @hybrid_property
        def may_upload(self) -> bool:
            return self.has_academic and self.scientist_tag and not self.excommunicated

    else:

        @hybrid_property
        def may_upload(self) -> bool:
            return True


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


class AcademicAccount(Base):
    __tablename__ = "academic_account"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="academic_accounts")

    institution: Mapped[str] = mapped_column(String(length=150), index=True)

    role_name: Mapped[str] = mapped_column(ForeignKey("academic_role.name"))
    role: Mapped["AcademicRole"] = relationship(back_populates="academic_accounts")


class AcademicRole(Base):
    __tablename__ = "academic_role"

    name: Mapped[str] = mapped_column(String(length=100), primary_key=True)

    syndb_access_level: Mapped[int] = mapped_column(default=0)
    academic_accounts: Mapped[list[AcademicAccount]] = relationship(back_populates="role")
