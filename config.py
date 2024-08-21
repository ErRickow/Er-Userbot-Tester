import os
import environs

# Load environment variables using environs
try:
    env = environs.Env()
    env.read_env("./.env")
except FileNotFoundError:
    print("No .env file found, using os.environ.")

# Load configurations
api_id = int(os.getenv("API_ID", env.int("API_ID")))
api_hash = os.getenv("API_HASH", env.str("API_HASH"))

STRINGSESSION = os.getenv("STRINGSESSION", env.str("STRINGSESSION"))
second_session = os.getenv("SECOND_SESSION", env.str("SECOND_SESSION", ""))

db_type = os.getenv("DATABASE_TYPE", env.str("DATABASE_TYPE"))
db_url = os.getenv("DATABASE_URL", env.str("DATABASE_URL", ""))
db_name = os.getenv("DATABASE_NAME", env.str("DATABASE_NAME"))

apiflash_key = os.getenv("APIFLASH_KEY", env.str("APIFLASH_KEY"))
rmbg_key = os.getenv("RMBG_KEY", env.str("RMBG_KEY", ""))
vt_key = os.getenv("VT_KEY", env.str("VT_KEY", ""))
gemini_key = os.getenv("GEMINI_KEY", env.str("GEMINI_KEY", ""))
vca_api_key = os.getenv("VCA_API_KEY", env.str("VCA_API_KEY", ""))
cohere_key = os.getenv("COHERE_KEY", env.str("COHERE_KEY", ""))

pm_limit = int(os.getenv("PM_LIMIT", env.int("PM_LIMIT", 5)))

test_server = bool(os.getenv("TEST_SERVER", env.bool("TEST_SERVER", False)))
modules_repo_branch = os.getenv("MODULES_REPO_BRANCH", env.str("MODULES_REPO_BRANCH", "master"))

# Default common parameters for MultiSessionBot
common_params = {
    "api_id": api_id,
    "api_hash": api_hash,
    "hide_password": True,
    "app_version": "ErUserbotBeta",
    "device_model": "MultiSessionBot",
    "system_version": platform.version() + " " + platform.machine(),
    "sleep_threshold": 30,
    "test_mode": test_server,
    "parse_mode": "HTML",
}

class MultiSessionBot:
    def __init__(self):
        self.clients = []
        self.plugins = []
        self.pending_phone_numbers = {}

    def add_client(self, name, session_string=None, phone_number=None):
        params = common_params.copy()
        if session_string:
            params["session_string"] = session_string
        else:
            params["session_name"] = f"{name}.session"
        
        client = Client(name, **params)
        self.clients.append(client)
        
        if phone_number:
            asyncio.create_task(self.register_phone(client, phone_number))

    async def register_phone(self, client, phone_number):
        try:
            await client.connect()
            sent_code = await client.send_code(phone_number)
            code = input(f"Masukkan kode yang dikirim ke {phone_number}: ")
            await client.sign_in(phone_number, sent_code.phone_code_hash, code)
            logging.info(f"Registrasi berhasil untuk {phone_number}")
        except errors.RPCError as e:
            logging.error(f"Gagal registrasi dengan nomor {phone_number}: {e}")
            raise
        finally:
            await client.disconnect()

    async def start_clients(self):
        for client in self.clients:
            try:
                await client.start()
                logging.info(f"Client {client.session_name} dimulai.")
            except Exception as e:
                logging.error(f"Gagal memulai client {client.session_name}: {e}")
                raise

    async def stop_clients(self):
        for client in self.clients:
            try:
                await client.stop()
                logging.info(f"Client {client.session_name} dihentikan.")
            except Exception as e:
                logging.error(f"Gagal menghentikan client {client.session_name}: {e}")

    def load_plugins(self):
        """Memuat plugin secara dinamis dari direktori plugins."""
        for path in Path("plugins").rglob("*.py"):
            try:
                spec = importlib.util.spec_from_file_location(path.stem, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.plugins.append(module)
                logging.info(f"Plugin {path.stem} dimuat")
            except Exception as e:
                logging.warning(f"Gagal memuat plugin {path.stem}: {e}")

    def register_handlers(self):
        """Mendaftarkan handler untuk setiap plugin di semua client."""
        for client in self.clients:
            for plugin in self.plugins:
                if hasattr(plugin, 'register_handlers'):
                    plugin.register_handlers(client)

            @client.on_message(filters.command("addprem") & filters.private)
            async def add_premium_user(bot_client, message: Message):
                user_id = message.from_user.id
                if user_id not in self.pending_phone_numbers:
                    await message.reply_text("Silakan masukkan nomor telepon untuk menambahkan ke userbot:")
                    self.pending_phone_numbers[user_id] = None  # Menandai bahwa user menunggu input nomor telepon
                else:
                    await message.reply_text("Anda sudah diminta untuk memasukkan nomor telepon. Mohon tunggu.")

            @client.on_message(filters.text & filters.private)
            async def handle_phone_number(bot_client, message: Message):
                user_id = message.from_user.id
                if user_id in self.pending_phone_numbers and self.pending_phone_numbers[user_id] is None:
                    phone_number = message.text.strip()
                    if phone_number.isdigit():
                        bot.add_client(f"userbot_{user_id}", phone_number=phone_number)
                        await message.reply_text(f"Nomor telepon {phone_number} sedang didaftarkan.")
                        del self.pending_phone_numbers[user_id]
                    else:
                        await message.reply_text("Nomor telepon tidak valid. Silakan masukkan nomor telepon yang benar.")
                else:
                    await message.reply_text("Tidak ada perintah yang menunggu nomor telepon.")

async def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("moonlogs.txt"), logging.StreamHandler()],
        level=logging.INFO,
    )

    bot = MultiSessionBot()

    # Menambahkan beberapa client dengan sesi yang berbeda atau dengan nomor telepon
    bot.add_client("userbot1", STRINGSESSION)
    if second_session:
        bot.add_client("userbot2", second_session)

    await bot.start_clients()
    bot.load_plugins()
    bot.register_handlers()

    if info := db.get("core.updater", "restart_info"):
        text = {
            "restart": "<blockquote>Restart Selesai Sayangkuh!</blockquote>",
            "update": "<blockquote>Proses Update Sukses Sayangku!</blockquote>",
        }[info["type"]]
        try:
            for client in bot.clients:
                await client.edit_message_text(info["chat_id"], info["message_id"], text)
        except errors.RPCError:
            pass
        db.remove("core.updater", "restart_info")

    if db.get("core.sessionkiller", "enabled", False):
        for client in bot.clients:
            db.set(
                "core.sessionkiller",
                "auths_hashes",
                [
                    auth.hash
                    for auth in (
                        await client.invoke(GetAuthorizations())
                    ).authorizations
                ],
            )

    logging.info("Er Userbot Beta dimulai!")
    await idle()
    await bot.stop_clients()

if __name__ == "__main__":
    asyncio.run(main())
