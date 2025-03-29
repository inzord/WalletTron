from datetime import date

from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class WalletInfo(Base):
    __tablename__ = "wallet_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String, index=True)
    bandwidth: Mapped[int] = mapped_column(Integer)
    energy: Mapped[int] = mapped_column(Integer)
    trx_balance: Mapped[int] = mapped_column(Integer)
    time_created: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)

    def __repr__(self) -> str:
        return f"<WalletInfo(address={self.address}, \bandwidth={self.bandwidth}, \
            energy={self.energy}, trx_balance={self.trx_balance}, time_created={self.time_created})>"
