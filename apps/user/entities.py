from core.database.entity import DBModel


class User(DBModel):
    __tablename__ = "user"

    # first_name: Mapped[str] = mapped_column(
    #     String(20), nullable=False
    # )
    # last_name: Mapped[str] = mapped_column(
    #     String(20), nullable=False
    # )
    # description: Mapped[Optional[str]] = mapped_column(
    #     Text,
    #     nullable=True,
    #     default=None,
    # )
    # content: Mapped[Optional[str]]

    # winner_uid: Mapped[bigint] = mapped_column(
    #     ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    # )
    # winner: Mapped[User] = relationship(
    #     User, lazy="joined", foreign_keys=[winner_id])
    ...
