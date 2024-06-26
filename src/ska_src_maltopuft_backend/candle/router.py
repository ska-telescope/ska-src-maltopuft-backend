"""Routers for Candidate Handler endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.core.database.database import get_db

from .controller import candidate_controller, sp_candidate_controller
from .requests import (
    CreateCandidate,
    CreateSPCandidate,
    GetCandidateQueryParams,
    GetSPCandidateQueryParams,
)
from .responses import (
    Candidate,
    CandidateNested,
    SPCandidate,
    SPCandidateNested,
)

logger = logging.getLogger(__name__)
candle_router = APIRouter()


@candle_router.get(
    "/sp",
    response_model=list[SPCandidateNested],
)
async def get_sp_candidates(
    q: GetSPCandidateQueryParams = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """Get all single pulse candidates."""
    logger.info(
        f"Getting all single pulse candidates with query parameters {q}",
    )
    return await sp_candidate_controller.get_all(db=db, q=q)


@candle_router.get(
    "/sp/{sp_candidate_id}",
    response_model=SPCandidate,
)
async def get_sp_candidate(
    sp_candidate_id: PositiveInt,
    db: Session = Depends(get_db),
) -> Candidate:
    """Get single pulse candidate by id."""
    logger.info(f"Getting single pulse candidate with id={sp_candidate_id}")
    return await sp_candidate_controller.get_by_id(db=db, id_=sp_candidate_id)


@candle_router.post(
    "/sp",
    response_model=SPCandidate,
    status_code=status.HTTP_201_CREATED,
)
async def post_sp_candidate(
    sp_candidate: CreateSPCandidate,
    db: Session = Depends(get_db),
) -> SPCandidate:
    """Create a new single pulse candidate."""
    logger.info(
        "Creating single pulse candidate with "
        f"candidate_id={sp_candidate.candidate_id}",
    )
    return await sp_candidate_controller.create(
        db=db,
        attributes=sp_candidate.model_dump(),
    )


@candle_router.delete(
    "/sp/{sp_candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_sp_candidate(
    sp_candidate_id: PositiveInt,
    db: Session = Depends(get_db),
) -> None:
    """Delete single pulse candidate by id."""
    logger.info(f"Deleting single pulse candidate with id={sp_candidate_id}")
    return await sp_candidate_controller.delete(db=db, id_=sp_candidate_id)


@candle_router.get(
    "/",
    response_model=list[CandidateNested],
)
async def get_candidates(
    q: GetCandidateQueryParams = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """Get all candidates."""
    logger.info(f"Getting all candidates with query parameters {q}")
    return await candidate_controller.get_all(db=db, q=q)


@candle_router.get(
    "/{candidate_id}",
    response_model=Candidate,
)
async def get_candidate(
    candidate_id: PositiveInt,
    db: Session = Depends(get_db),
) -> Candidate:
    """Get candidate by id."""
    logger.info(f"Getting candidate with id={candidate_id}")
    return await candidate_controller.get_by_id(db=db, id_=candidate_id)


@candle_router.post(
    "/",
    response_model=Candidate,
    status_code=status.HTTP_201_CREATED,
)
async def post_candidate(
    candidate: CreateCandidate,
    db: Session = Depends(get_db),
) -> Candidate:
    """Create a new candidate."""
    logger.info("Creating candidate")
    return await candidate_controller.create(
        db=db,
        attributes=candidate.model_dump(),
    )


@candle_router.delete(
    "/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_candidate(
    candidate_id: PositiveInt,
    db: Session = Depends(get_db),
) -> None:
    """Delete candidate by id."""
    logger.info(f"Deleting candidate with id={candidate_id}")
    return await candidate_controller.delete(db=db, id_=candidate_id)
