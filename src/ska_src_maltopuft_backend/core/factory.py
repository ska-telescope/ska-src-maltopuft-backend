"""Controller Factory."""

from functools import partial

from ska_src_maltopuft_backend.app.controllers import (
    CandidateController,
    EntityController,
    LabelController,
    ObservationController,
    SPCandidateController,
    UserController,
)
from ska_src_maltopuft_backend.app.models import (
    Candidate,
    Entity,
    Label,
    Observation,
    SPCandidate,
    User,
)
from ska_src_maltopuft_backend.app.repositories import (
    CandidateRepository,
    EntityRepository,
    LabelRepository,
    ObservationRepository,
    SPCandidateRepository,
    UserRepository,
)


class Factory:
    """Instantiates all controllers and ensures that they are accessible
    throughout the application.
    """

    # Repositories
    user_repository = partial(UserRepository, User)
    candidate_repository = partial(CandidateRepository, Candidate)
    sp_candidate_repository = partial(SPCandidateRepository, SPCandidate)
    entity_repository = partial(EntityRepository, Entity)
    label_repository = partial(LabelRepository, Label)
    observation_repository = partial(ObservationRepository, Observation)

    def get_user_controller(self) -> UserController:
        """UserController factory."""
        return UserController(repository=self.user_repository())

    def get_observation_controller(self) -> ObservationController:
        """ObservationController factory."""
        return ObservationController(repository=self.observation_repository())

    def get_candidate_controller(self) -> CandidateController:
        """CandidateController factory."""
        return CandidateController(repository=self.candidate_repository())

    def get_sp_candidate_controller(self) -> SPCandidateController:
        """SPCandidateController factory."""
        return SPCandidateController(
            repository=self.sp_candidate_repository(),
            observation_controller=self.get_observation_controller(),
        )

    def get_entity_controller(self) -> EntityController:
        """EntityController factory."""
        return EntityController(repository=self.entity_repository())

    def get_label_controller(self) -> LabelController:
        """LabelController factory."""
        return LabelController(repository=self.label_repository())
