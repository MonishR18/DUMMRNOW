from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.social import Post, Comment, Like, Bookmark, Follow
from models.user import User
from schemas.social import PostCreate, PostResponse, CommentBase, CommentCreate, CommentResponse

router = APIRouter(prefix="/api", tags=["social"])

from core.security import get_current_active_user

@router.get("/feed", response_model=List[PostResponse])
def get_feed(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    return posts

@router.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    user_id = current_user.id
    db_post = Post(content=post.content, author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.post("/posts/{post_id}/like")
def toggle_like(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    user_id = current_user.id
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    existing_like = db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    if existing_like:
        db.delete(existing_like)
        db.commit()
        return {"status": "unliked"}
    else:
        new_like = Like(post_id=post_id, user_id=user_id)
        db.add(new_like)
        db.commit()
        return {"status": "liked"}

@router.post("/posts/{post_id}/bookmark")
def toggle_bookmark(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    user_id = current_user.id
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    existing_bookmark = db.query(Bookmark).filter(Bookmark.post_id == post_id, Bookmark.user_id == user_id).first()
    if existing_bookmark:
        db.delete(existing_bookmark)
        db.commit()
        return {"status": "unbookmarked"}
    else:
        new_bookmark = Bookmark(post_id=post_id, user_id=user_id)
        db.add(new_bookmark)
        db.commit()
        return {"status": "bookmarked"}

@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.asc()).all()
    return comments

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(post_id: int, comment: CommentBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    user_id = current_user.id
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    db_comment = Comment(content=comment.content, author_id=user_id, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
