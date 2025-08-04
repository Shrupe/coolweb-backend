import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from uuid import UUID
import uuid
import httpx

from app.services.embedding import get_embedding
from app.schemas.website_s import WebsiteCreate, WebsiteRead, WebsiteListResponse
from app.models.website_m import Website
from app.core.db import get_db
from app.schemas.search import WebsiteSearchRequest
from app.crud.website_c import search_websites_by_embedding

router = APIRouter(prefix="/api/v1/websites")

# @router.post(
#         "/", 
#         response_model=WebsiteRead,
#         status_code=status.HTTP_201_CREATED
#         )
# async def create_website(
#     website_data: WebsiteCreate, 
#     db: AsyncSession = Depends(get_db)
#     ):
#     # Check for duplicates by URL
#     result = await db.execute(
#                         select(Website).where(Website.url == str(website_data.url))
#                         )
#     existing = result.scalar_one_or_none()
#     if existing:
#         raise HTTPException(status_code=400, detail="Website already exists.")
    

#     combined_text = f"\
#             {website_data.name} - \
#             {website_data.description} - \
#             {', '.join(website_data.tags)}"
#     embedding = await get_embedding(combined_text)


#     new_website = Website(
#         id=uuid.uuid4(),
#         name=website_data.name,
#         url=str(website_data.url),
#         description=website_data.description,
#         tags=website_data.tags,
#         screenshot_url=website_data.screenshot_url,
#         embedding=embedding
#     )

#     db.add(new_website)
#     await db.commit()
#     await db.refresh(new_website)

#     return new_website

@router.post(
    "/", 
    response_model=WebsiteRead,
    status_code=status.HTTP_201_CREATED
)
async def create_or_update_website(
    website_data: WebsiteCreate, 
    db: AsyncSession = Depends(get_db)
):
    # Check for existing website by URL
    result = await db.execute(select(Website).where(Website.url == str(website_data.url)))
    existing = result.scalar_one_or_none()

    # Generate embedding for updated/new data
    combined_text = f"{website_data.name} - {website_data.description} - {', '.join(website_data.tags)}"
    embedding = await get_embedding(combined_text)

    if existing:
        # Update existing website
        existing.name = website_data.name
        existing.description = website_data.description
        existing.tags = website_data.tags
        existing.screenshot_url = website_data.screenshot_url
        existing.embedding = embedding

        await db.commit()
        await db.refresh(existing)
        return existing

    # Create new website
    new_website = Website(
        id=uuid.uuid4(),
        name=website_data.name,
        url=str(website_data.url),
        description=website_data.description,
        tags=website_data.tags,
        screenshot_url=website_data.screenshot_url,
        embedding=embedding
    )

    db.add(new_website)
    await db.commit()
    await db.refresh(new_website)

    return new_website

@router.post("/search", response_model=list[WebsiteRead])
async def search_websites(
    request: WebsiteSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    embedding = await get_embedding(request.query)
    results = await search_websites_by_embedding(db, embedding, limit=request.limit)
    return results

@router.get("/", response_model=WebsiteListResponse)
async def list_websites(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("created_at", pattern="^(created_at|name)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    tag: str = None,
    search: str = None
):
    query = select(Website)

    # Filter by tag if specified
    if tag:
        query = query.where(Website.tags.any(tag))

    # Search filter
    if search:
        query = query.where(
            Website.name.ilike(f"%{search}%") |
            Website.description.ilike(f"%{search}%")
        )

    # Total count for pagination
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Sorting
    sort_column = getattr(Website, sort_by)
    if sort_order == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    # Apply sorting and pagination
    result = await db.execute(
        query.order_by(sort_column).offset(offset).limit(limit)
    )
    websites = result.scalars().all()

    return WebsiteListResponse(total=total, items=websites)

@router.get("/{website_id}", response_model=WebsiteRead)
async def get_website_by_id(
    website_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Website).where(Website.id == website_id))
    website = result.scalar_one_or_none()

    if website is None:
        raise HTTPException(status_code=404, detail="Website not found.")

    return website