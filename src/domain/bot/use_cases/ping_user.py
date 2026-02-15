from asyncio import gather
from datetime import timedelta
from uuid import UUID

from src.common.models.mixins import utcnow
from src.domain.bot.use_cases.send_message import BotSendMessage
from src.domain.completed_standards.dto.filter import CompletedStandardFilterSchema
from src.domain.completed_standards.use_cases.list import ListCompletedStandards
from src.domain.credits.use_cases.get_active import GetActiveCredit
from src.domain.llm.use_cases.generate import LLMGenerate


class PingUser:
    def __init__(
        self,
        list_completed_standards: ListCompletedStandards,
        get_active_credit: GetActiveCredit,
        llm_generate: LLMGenerate,
        bot_send_message: BotSendMessage,
        config: dict,
    ):
        self.list_completed_standards = list_completed_standards
        self.get_active_credit = get_active_credit
        self.llm_generate = llm_generate
        self.bot_send_message = bot_send_message
        self.config = config

    async def __call__(self, user_id: UUID, chat_id: int) -> None:
        params = CompletedStandardFilterSchema(
            user_id=user_id,
            created_at_gte=utcnow().date() - timedelta(days=3),
        )
        completed_standards, active_credit = await gather(
            self.list_completed_standards(params),
            self.get_active_credit(user_id),
        )
        credit_data = active_credit.count - active_credit.completed_count if active_credit else 'Нет зачета'
        completed_standards_data = ' '.join(
            f'{c_standard.created_at} - {c_standard.count} {c_standard.standard.name}' for c_standard in completed_standards
        ).strip() or 'Нет данных'
        prompt = self.config['llm_model']['activity_prompt'] % (completed_standards_data, credit_data)
        llm_response = await self.llm_generate(
            model_name=self.config['llm_model']['name'],
            prompt=prompt
        )
        await self.bot_send_message(llm_response, chat_id)
