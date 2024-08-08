"""Controller Factory."""

from functools import partial

from ska_src_maltopuft_backend.app import controllers, models, repositories


class Factory:
    """Instantiates all controllers and ensures that they are accessible
    throughout the application.
    """

    # Repositories
    user_repository = partial(repositories.UserRepository, models.User)
    candidate_repository = partial(
        repositories.CandidateRepository,
        models.Candidate,
    )
    sp_candidate_repository = partial(
        repositories.SPCandidateRepository,
        models.SPCandidate,
    )
    entity_repository = partial(repositories.EntityRepository, models.Entity)
    label_repository = partial(repositories.LabelRepository, models.Label)
    observation_repository = partial(
        repositories.ObservationRepository,
        models.Observation,
    )
    known_pulsar_repository = partial(
        repositories.KnownPulsarRepository,
        models.KnownPulsar,
    )

    def get_user_controller(self) -> controllers.UserController:
        """UserController factory."""
        return controllers.UserController(repository=self.user_repository())

    def get_observation_controller(self) -> controllers.ObservationController:
        """ObservationController factory."""
        return controllers.ObservationController(
            repository=self.observation_repository(),
            known_pulsar_controller=self.get_known_pulsar_controller(),
        )

    def get_candidate_controller(self) -> controllers.CandidateController:
        """CandidateController factory."""
        return controllers.CandidateController(
            repository=self.candidate_repository(),
        )

    def get_sp_candidate_controller(self) -> controllers.SPCandidateController:
        """SPCandidateController factory."""
        return controllers.SPCandidateController(
            repository=self.sp_candidate_repository(),
            observation_controller=self.get_observation_controller(),
        )

    def get_entity_controller(self) -> controllers.EntityController:
        """EntityController factory."""
        return controllers.EntityController(
            repository=self.entity_repository(),
        )

    def get_label_controller(self) -> controllers.LabelController:
        """LabelController factory."""
        return controllers.LabelController(repository=self.label_repository())

    def get_known_pulsar_controller(self) -> controllers.KnownPulsarController:
        """KnownPulsarController factory."""
        return controllers.KnownPulsarController(
            repository=self.known_pulsar_repository(),
        )
