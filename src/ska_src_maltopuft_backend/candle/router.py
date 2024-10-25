"""Routers for Candidate Handler endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.core.database.database import get_db
from ska_src_maltopuft_backend.core.factory import Factory
from ska_src_maltopuft_backend.core.schemas import (
    ForeignKeyQueryParams,
    RaDecPositionQueryParameters,
)

from .controller import CandidateController, SPCandidateController
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
    q_foreign_key: ForeignKeyQueryParams = Depends(),
    q_pos: RaDecPositionQueryParameters = Depends(),
    db: Session = Depends(get_db),
    sp_candidate_controller: SPCandidateController = Depends(
        Factory().get_sp_candidate_controller,
    ),
) -> Any:
    """Get all single pulse candidates.

    When no query parameters are specified, the default behaviour is to fetch
    single pulse candidates from the earliest observation in ascending time
    order.

    If query parameters are specified, those single pulse candidates are
    selected and ordered by descending observeration time in order to return
    the *most recent* candidates to users by default.

    If the ``latest`` query parameter is set to true, only candidates from
    the most recent observation are returned (in ascending time order).
    """
    params = [q, q_foreign_key, q_pos]
    logger.info(
        f"Getting all single pulse candidates with query parameters {params}",
    )
    return await sp_candidate_controller.get_all(
        db=db,
        join_=["candidate", "beam", "host", "observation", "schedule_block"],
        order_={"asc": ["candidate.observed_at"]},
        q=params,
    )


@candle_router.get("/sp/count", response_model=int)
async def get_sp_candidates_count(
    q: GetSPCandidateQueryParams = Depends(),
    q_foreign_key: ForeignKeyQueryParams = Depends(),
    q_pos: RaDecPositionQueryParameters = Depends(),
    db: Session = Depends(get_db),
    sp_candidate_controller: SPCandidateController = Depends(
        Factory().get_sp_candidate_controller,
    ),
) -> int:
    """Count single pulse candidates."""
    return await sp_candidate_controller.count(
        db=db,
        join_=["candidate", "beam", "host", "observation", "schedule_block"],
        q=[q, q_foreign_key, q_pos],
    )


@candle_router.get(
    "/sp/{sp_candidate_id}",
    response_model=SPCandidate,
)
async def get_sp_candidate(
    sp_candidate_id: PositiveInt,
    db: Session = Depends(get_db),
    sp_candidate_controller: SPCandidateController = Depends(
        Factory().get_sp_candidate_controller,
    ),
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
    sp_candidate_controller: SPCandidateController = Depends(
        Factory().get_sp_candidate_controller,
    ),
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
    sp_candidate_controller: SPCandidateController = Depends(
        Factory().get_sp_candidate_controller,
    ),
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
    candidate_controller: CandidateController = Depends(
        Factory().get_candidate_controller,
    ),
) -> Any:
    """Get all candidates."""
    logger.info(f"Getting all candidates with query parameters {q}")
    return await candidate_controller.get_all(db=db, q=[q])


@candle_router.get(
    "/{candidate_id}",
    response_model=Candidate,
)
async def get_candidate(
    candidate_id: PositiveInt,
    db: Session = Depends(get_db),
    candidate_controller: CandidateController = Depends(
        Factory().get_candidate_controller,
    ),
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
    candidate_controller: CandidateController = Depends(
        Factory().get_candidate_controller,
    ),
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
    candidate_controller: CandidateController = Depends(
        Factory().get_candidate_controller,
    ),
) -> None:
    """Delete candidate by id."""
    logger.info(f"Deleting candidate with id={candidate_id}")
    return await candidate_controller.delete(db=db, id_=candidate_id)
