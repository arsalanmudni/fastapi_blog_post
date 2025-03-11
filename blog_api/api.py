from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache
from sqlmodel import select

from blog_api.model import Blog
from blog_api.schema import BlogCreate, BlogUpdate
from db.session import SessionDep

blog_router = APIRouter(prefix="/blogs", tags=["blogs"])

@blog_router.get("/")
@cache(expire=300)
async def get_blogs(session: SessionDep):
    return session.exec(select(Blog)).all()


@blog_router.get("/{blog_id}")
@cache(expire=60)
async def get_blog(blog_id: int, session: SessionDep):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} not found")
    return blog


@blog_router.post("/create")
async def create_blog(blog: BlogCreate, session: SessionDep):
    data = blog.model_dump()
    blog_obj = Blog(**data)
    session.add(blog_obj)
    session.commit()
    session.refresh(blog_obj)
    return blog_obj


@blog_router.put("/update/{blog_id}")
async def update_blog(blog_id: int, blog_patch: BlogUpdate, session: SessionDep):
    blog = session.get(Blog, blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} not found")

    data = blog_patch.model_dump(exclude_unset=True)  # Only update provided fields
    for key, value in data.items():
        setattr(blog, key, value)

    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog


@blog_router.delete("/delete/{blog_id}")
async def delete_blog(blog_id: int, session: SessionDep):
    blog = session.get(Blog,blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} not found")
    session.delete(blog)
    session.commit()
    return {"success": True}


