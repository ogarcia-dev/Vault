from sqlalchemy.orm import (
    Mapped, 
    mapped_column
)

from sqlalchemy import (
    String, 
    Text
)

from core.bases.BaseModels import BaseModel



class KeyPair(BaseModel):
    __tablename__ = 'keys_pairs'

    system_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    private_key: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    public_key: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    refresh_private_key: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    refresh_public_key: Mapped[str] = mapped_column(Text, nullable=False, index=True)

    def __repr__(self) -> str:
        return self.system_code