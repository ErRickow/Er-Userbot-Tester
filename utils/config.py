import os
import environs

try:
    env = environs.Env()
    env.read_env("./.env")
except FileNotFoundError:
    print("No .env file found, using os.environ.")

api_id = int(os.getenv("API_ID", env.int("API_ID")))
api_hash = os.getenv("API_HASH", env.str("API_HASH"))

STRINGSESSION = os.getenv("STRINGSESSION", env.str("STRINGSESSION"))

db_type = os.getenv("DATABASE_TYPE", env.str("DATABASE_TYPE"))
db_url = os.getenv("DATABASE_URL", env.str("DATABASE_URL", ""))
db_name = os.getenv("DATABASE_NAME", env.str("DATABASE_NAME"))

apiflash_key = os.getenv("APIFLASH_KEY", env.str("APIFLASH_KEY"))
rmbg_key = os.getenv("RMBG_KEY", env.str("RMBG_KEY"))
vt_key = os.getenv("VT_KEY", env.str("VT_KEY"))
gemini_key = os.getenv("GEMINI_KEY", env.str("GEMINI_KEY"))
vca_api_key = os.getenv("VCA_API_KEY", env.str("VCA_API_KEY"))
cohere_key = os.getenv("COHERE_KEY", env.str("COHERE_KEY"))

pm_limit = int(os.getenv("PM_LIMIT", env.int("PM_LIMIT")))

test_server = bool(os.getenv("TEST_SERVER", env.bool("TEST_SERVER", False)))
modules_repo_branch = os.getenv("MODULES_REPO_BRANCH", env.str("MODULES_REPO_BRANCH", "master"))

class ENV_TEMPLATE:
    airing_template = "AIRING_TEMPLATE"
    airpollution_template = "AIRPOLLUTION_TEMPLATE"
    alive_pic = "ALIVE_PIC"
    alive_template = "ALIVE_TEMPLATE"
    anilist_user_template = "ANILIST_USER_TEMPLATE"
    anime_template = "ANIME_TEMPLATE"
    btn_in_help = "BUTTONS_IN_HELP"
    character_template = "CHARACTER_TEMPLATE"
    chat_info_template = "CHAT_INFO_TEMPLATE"
    climate_api = "CLIMATE_API"
    climate_template = "CLIMATE_TEMPLATE"
    command_template = "COMMAND_TEMPLATE"
    currency_api = "CURRENCY_API"
    custom_pmpermit = "CUSTOM_PMPERMIT"
    gban_template = "GBAN_TEMPLATE"
    github_user_template = "GITHUB_USER_TEMPLATE"
    help_emoji = "HELP_EMOJI"
    help_template = "HELP_TEMPLATE"
    is_logger = "IS_LOGGER"
    log_id = "LOG_ID"
    lyrics_api = "LYRICS_API"
    manga_template = "MANGA_TEMPLATE"
    ocr_api = "OCR_API"
    cohere_api_key = "COHERE_API_KEY"
    face_clients_name = "FACE_CLIENTS_NAME"
    face_token_key = "FACE_TOKEN"
    system_prompt = "SYSTEM_PROMPT"
    asupan_username = "ASUPAN_USERNAME"
    fedban_api_key = "FEDBAN_API_KEY"
    ping_pic = "PING_PIC"
    ping_template = "PING_TEMPLATE"
    pm_logger = "PM_LOGGER"
    pm_max_spam = "PM_MAX_SPAM"
    pmpermit = "PMPERMIT"
    pmpermit_pic = "PMPERMIT_PIC"
    remove_bg_api = "REMOVE_BG_API"
    thumbnail_url = "THUMBNAIL_URL"
    statistics_template = "STATISTICS_TEMPLATE"
    sticker_packname = "STICKER_PACKNAME"
    tag_logger = "TAG_LOGGER"
    telegraph_account = "TELEGRAPH_ACCOUNT"
    time_zone = "TIME_ZONE"
    unload_plugins = "UNLOAD_PLUGINS"
    unsplash_api = "UNSPLASH_API"
    usage_template = "USAGE_TEMPLATE"
    user_info_template = "USER_INFO_TEMPLATE"

