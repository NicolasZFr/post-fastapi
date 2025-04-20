from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlmodel import select

from app.infrastructure.model import Vote, User, Post
from app.schemas.vote import VoteBase, VoteResponse
from app.schemas.user import *
from .. import oauth2


from .. import utils
from app.infrastructure.databases.database import SessionDep


router = APIRouter(prefix="/api/votes", tags=["Vote"], dependencies=[Depends(oauth2.get_current_user)])

# ------------------- Endpoints -------------------

# POST Votes
@router.post("/", response_model=VoteResponse)
async def post_users(vote: VoteBase, session: SessionDep, user: User = Depends(oauth2.get_current_user)):
    query = select(Post).where(Post.id == vote.post_id)
    if not session.exec(query).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} doesn't exist")
    query = select(Vote).where(vote.post_id == Vote.post_id,Vote.user_id == user.id)
    vote_query = session.exec(query).first()
    if vote.dir == 1:
        if vote_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {user.id} already voted for this post on post {vote.post_id}')
        new_vote = Vote(user_id = user.id, post_id = vote.post_id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        return VoteResponse(
            response="Vote was added succesfully",
            data=vote
        )

    else:
        if not vote_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{vote.post_id} not found')

# GET Votes
@router.get("/")
async def get_users(session: SessionDep):
    votes = session.exec(select(Vote).order_by(Vote.post_id.asc())).all()
    return votes
