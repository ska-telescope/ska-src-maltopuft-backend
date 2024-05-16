"""Routers for Candidate Handler endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.ska_src_maltopuft_backend.candle.controller import (
    candidate_controller,
    sp_candidate_controller,
)
from src.ska_src_maltopuft_backend.candle.requests import (
    CreateCandidate,
    CreateSPCandidate,
    GetCandidateQueryParams,
    GetSPCandidateQueryParams,
)
from src.ska_src_maltopuft_backend.candle.responses import (
    Candidate,
    SPCandidate,
)
from src.ska_src_maltopuft_backend.core.database import get_db

logger = logging.getLogger(__name__)
candle_router = APIRouter()


@candle_router.get("/", response_model=list[Candidate])
async def get_candidates(
    q: GetCandidateQueryParams = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """Get all candidates."""
    return await candidate_controller.get_all(db=db, q=q)


@candle_router.get("/{candidate_id}")
async def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
) -> Candidate:
    """Get candle by id."""
    return await candidate_controller.get_by_id(db=db, id_=candidate_id)


@candle_router.post("/")
async def post_candidate(
    candidate: CreateCandidate,
    db: Session = Depends(get_db),
) -> Candidate:
    """Create a new candidate."""
    return await candidate_controller.create(
        db=db,
        attributes=candidate.model_dump(),
    )


@candle_router.delete("/{candidate_id}")
async def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete candidate by id."""
    return await candidate_controller.delete(db=db, id_=candidate_id)


@candle_router.get("/sp", response_model=list[SPCandidate])
async def get_sp_candidates(
    q: GetSPCandidateQueryParams = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """Get all single pulse candidates."""
    return await sp_candidate_controller.get_all(db=db, q=q)


@candle_router.get("/sp/{sp_candidate_id}")
async def get_sp_candidate(
    candle_id: int,
    db: Session = Depends(get_db),
) -> Candidate:
    """Get candle by id."""
    return await candidate_controller.get_by_id(db=db, id_=candle_id)


@candle_router.post("/sp")
async def post_sp_candidate(
    sp_candidate: CreateSPCandidate,
    db: Session = Depends(get_db),
) -> SPCandidate:
    """Create a new single pulse candidate."""
    return await sp_candidate_controller.create(
        db=db,
        attributes=sp_candidate.model_dump(),
    )


@candle_router.delete("/{sp_candidate_id}")
async def delete_sp_candidate(
    sp_candidate_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete single pulse candidate by id."""
    return await sp_candidate_controller.delete(db=db, id_=sp_candidate_id)
