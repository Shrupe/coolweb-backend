import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pgvector.sqlalchemy import Vector
from app.models.website_m import Website
import numpy as np


async def search_websites_by_embedding(
    db: AsyncSession,
    query_embedding: list[float],
    limit: int = 10,
) -> list[Website]:
    query_embedding = np.array(query_embedding, dtype=np.float32).tolist()
    
    stmt = (
        select(Website)
        .order_by(Website.embedding.l2_distance(query_embedding))
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
