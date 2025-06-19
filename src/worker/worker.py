from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from src.containers.container import container
from src.data.models.completed_standard import CompletedStandardCreate
from src.domain.classifier.dto.enums import TextClass
from src.domain.user.dto.enums import CompletedType


# mapping_classifier = {
#     TextClass.completed_standards: container.use_cases.create_completed_standards_from_text(),
# }
create_completed_standards_from_text = container.use_cases.create_completed_standards_from_text()

async def conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO authorization
    # TODO training ner model + распознавать текстовые числа
    # TODO classification
    input_message = update.message.text

    user_id = 'a89b9123-436e-456e-956e-dbeff62e18d9'  # TODO
    completed_type = CompletedType.count  # TODO
    classifier_model = container.gateways.classifier_model()
    predictions = classifier_model.predict([input_message])
    if predictions[0] == TextClass.completed_standards.value:
        created_standards = await create_completed_standards_from_text(
            input_message, user_id, completed_type
        )
        result = (
            ("Записываю:\n" + "\n".join((f"{k}: {v}" for k, v in created_standards.items())))
            if created_standards
            else "Нифига не понял"
        )
        await update.message.reply_text(result)

def main() -> None:
    container.init_resources()
    application = Application.builder().token(container.config()["telegram"]["token"]).build()
    application.add_handler(MessageHandler(filters.ALL, conversation))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
