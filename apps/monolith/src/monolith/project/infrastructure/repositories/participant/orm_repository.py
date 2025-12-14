from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from monolith.project.domain.interfaces.repositories.participant import IParticipantRepository
from monolith.project.domain.model import Participant
from monolith.project.infrastructure.models import Participant as ORMParticipant


class ParticipantRepository(IParticipantRepository):
    """Реализация репозитория для участников проекта."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, participant: Participant) -> Participant:
        orm_participant = ORMParticipant(
            auth_user_id=participant.auth_user_id,
            project_id=participant.project_id,

        )
        self.session.add(orm_participant)
        await self.session.commit()
        await self.session.refresh(orm_participant)
        # Обновление полей доменной модели
        participant.id = orm_participant.id
        participant.created_at = orm_participant.created_at
        participant.updated_at = orm_participant.updated_at
        return participant

    async def _get_by_id(self, participant_id: int) -> ORMParticipant | None:
        return await self.session.get(ORMParticipant, participant_id)

    async def get_by_id(self, participant_id: int) -> Participant | None:
        orm_participant = await self._get_by_id(participant_id)
        if not orm_participant:
            return None
        return Participant(
            auth_user_id=orm_participant.auth_user_id,
            project_id=orm_participant.project_id,
            participant_id=orm_participant.id,
            created_at=orm_participant.created_at,
            updated_at=orm_participant.updated_at
        )

    async def get_all(self) -> list[Participant]:
        statement = select(ORMParticipant).order_by(ORMParticipant.id)
        result = await self.session.scalars(statement)
        orm_participants = result.all()
        return [
            Participant(
                auth_user_id=orm_participant.auth_user_id,
                project_id=orm_participant.project_id,
                participant_id=orm_participant.id,
                created_at=orm_participant.created_at,
                updated_at=orm_participant.updated_at
            )
            for orm_participant in orm_participants
        ]

    async def get_all_by_project_id(self, project_id) -> list[Participant]:
        statement = (
            select(ORMParticipant)
            .where(ORMParticipant.project_id==project_id)
            .order_by(ORMParticipant.id)
        )
        result = await self.session.scalars(statement)
        orm_participants = result.all()
        return [
            Participant(
                auth_user_id=orm_participant.auth_user_id,
                project_id=orm_participant.project_id,
                participant_id=orm_participant.id,
                created_at=orm_participant.created_at,
                updated_at=orm_participant.updated_at
            )
            for orm_participant in orm_participants
        ]

    async def remove_by_id(self, participant_id: int) -> bool:
        orm_participant = await self._get_by_id(participant_id)
        if not orm_participant:
            return False
        await self.session.delete(orm_participant)
        await self.session.commit()
        return True

    async def remove_by_auth_user_and_project(self, auth_user_id: int, project_id: int) -> bool:
        statement = (
            delete(ORMParticipant).
            where(
                ORMParticipant.auth_user_id == auth_user_id,
                ORMParticipant.project_id == project_id
            )
        )
        result = await self.session.execute(statement)
        await self.session.commit()
        return True
