from fastapi import APIRouter
from sqlmodel import select

from app.database.connection import SessionDep, OxfordDictionary

oxford_router = APIRouter(tags=["oxford"])


@oxford_router.get("/{word}")
async def retrieve_content(word: str, session: SessionDep):
    statement = select(OxfordDictionary.content).where(OxfordDictionary.word == word)
    return session.exec(statement).first()


@oxford_router.post("/new")
def create_dictionary(
    dictionary: OxfordDictionary, session: SessionDep
) -> OxfordDictionary:
    session.add(dictionary)
    session.commit()
    session.refresh(dictionary)
    return dictionary
