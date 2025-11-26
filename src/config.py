import os

from pydantic import field_validator, PostgresDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

project_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class JwtConfig(BaseSettings):
    secret_key: str = "d2a73573-da3a-44d2-bb4e-5a9dceae01a2"
    refresh_secret_key: str = "68b94237-fd46-4ae7-b71f-afb7b6c5dd82"

    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_prefix='jwt_'
    )

class BotAuthConfig(BaseSettings):
    url: str = "http://127.0.0.1:8000/auth/"

    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_prefix='bot_auth_'
    )

class PostgresConfig(BaseSettings):
    scheme: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "postgres"
    db: str = "standard"
    pool_size: int = 10
    pool_overflow_size: int = 10
    echo: bool = False
    dsn: str | None = None

    @field_validator('dsn')
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> str:
        values = values.data
        if isinstance(v, str):
            return v
        return str(
            PostgresDsn.build(
                scheme=values.get("scheme"),
                username=values.get("user"),
                password=values.get("password"),
                host=values.get("host"),
                port=int(values.get("port")),
                path=f"{values.get('db')}",
            )
        )

    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_prefix='postgres_'
    )

class TelegramSettings(BaseSettings):
    token: str = ""

    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_prefix='telegram_'
    )

class ClassifierModelSettings(BaseSettings):
    path: str = os.path.join(project_dir, 'models/text_classifier7.joblib')

    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_prefix='classifier_model_'
    )

class NERModelSettings(BaseSettings):
    path: str = os.path.join(project_dir, 'models/ner_model')

    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_prefix='ner_model_'
    )

class LLMModelSettings(BaseSettings):
    name: str = 'qwen3-coder:30b'
    host: str = '192.168.0.11:11434'
    activity_prompt: str = '''Ты — чат-бот спортивного приложения.
Твоя миссия — мотивировать пользователя тренироваться, используя юмор и дружеский тон.
Пользователь сам записывает свои упражнения. 
Упражнения только со своим собственным весом, например: подтягивания. приседания, скручивания, бег и т.п.
В приложении есть месячный зачет(действует с первого числа месяца до последнего включительно): 
число в нормах(в приложении используется как условная единица), которое означает, 
что пользователю необходимо выполнить определенное количество повторений. Например:
если зачет равен 100 нормам(в приложении используется как условная единица), 
то для его выполнения пользователю нужно выполнить либо 100 подтягивания, либо 300 отжиманий, 
либо 400 приседаний(У каждого упражнения свой коэффициент). 
Упражнения можно комбинировать(50 подтягиваний, 120 отжиманий, 40 приседаний).
Приложение само считает сколько осталось выполнить пользователю до конца месяца. 
Если до первого числа следующего месяца зачет больше нуля - он считается не выполненным.
Твоя задача: проанализировать активность пользователя за последние три дня и выдать короткое сообщение.
Если активностей нет — поругай его, с юмором.
Если активности есть — похвали, подбодри, отметь прогресс.
Стиль:
дружеский, как будто вы знакомы давно;
юмор — лёгкий без абсурдных метафор;
никаких странных выражений (например, “пикник в пустыне” или “прерывистый фейерверк”);
текст должен быть простым, современным и естественным.
Формат ответа:
2–5 коротких предложений (до 400 символов);
без вступлений вроде “о боже”, “как говорится”;
не повторяй одни и те же мысли.
Примеры:
“Эй, куда пропал? Иди и поработай в зале, иначе так и будешь дрыщем. 
Чтобы закрыть текущий зачет необходимо делать по {зачет/количество дней до конца месяца} норм каждый день!”
“Хорош! 200 приседаний и 70 подтягиваний — машина, скоро станешь ходячей горой мышц! Продолжай в том же духе”
При указании количества упражнений в день для закрытия зачета считай максимально точно 
деление зачета на оставшееся количество дней до конца месяца(от текущей даты) с округлением в большую сторону!
Не предлагай пользователю сделать всё за один день, если зачет больше 50 и сегодня не последний день месяца.
Если пользователь выполнил меньше 50 норм(50 подтягиваний или 150 отжиманий и т.п.) за 3 дня - это плохо. 
Больше 100 норм - очень хорошо.
Если значение зачета меньше нуля - зачет считается выполненным.
Данные пользователя за последние три дня: %s
Оставшийся зачет: %s
Выведи только готовый текст для пользователя, без пояснений.'''
# TODO add standards
    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_prefix='llm_model_'
    )

class Settings(BaseSettings):
    jwt: JwtConfig = JwtConfig()
    bot_auth: BotAuthConfig = BotAuthConfig()
    database: PostgresConfig = PostgresConfig()
    telegram: TelegramSettings = TelegramSettings()
    classifier_model: ClassifierModelSettings = ClassifierModelSettings()
    ner_model: NERModelSettings = NERModelSettings()
    llm_model: LLMModelSettings = LLMModelSettings()
