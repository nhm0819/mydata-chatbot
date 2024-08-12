from pydantic import BaseModel


class AccountBase(BaseModel):
    id: int
    uid: str

    class Config:
        from_attributes = True


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    pass
