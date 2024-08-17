if ! command -v termux-setup-storage; then
  echo This script can be executed only on Termux
  exit 1
fi

termux-wake-lock

pkg update -y && pkg upgrade -y
pkg install python3 git clang ffmpeg wget libjpeg-turbo libcrypt ndk-sysroot zlib openssl -y || exit 2


LDFLAGS="-L${PREFIX}/lib/" CFLAGS="-I${PREFIX}/include/" pip3 install --upgrade wheel pillow

if [[ -d "Er-Userbot-Tester" ]]; then
  cd Moon-Userbot
elif [[ -f ".env.dist" ]] && [[ -f "erbanget.py" ]] && [[ -d "plugins" ]]; then
  :
else
  git clone https://github.com/ErRickow/Er-Userbot-Tester || exit 2
  cd Er-Userbot-Tester || exit 2
fi

if [[ -f ".env" ]] && [[ -f "akun_ku.session" ]]; then
  echo "Er Userbot Tester telah terinstall..."
  exit
fi

python3 -m pip install -U -r requirements.txt || exit 2

echo
echo "Pencet API_ID dan API_HASH"
echo "Lu bisa ambil disini -> https://my.telegram.org/apps"
echo "Kosongkan kalo gamau ribet  (tetapi kemungkinan terbannednya tinggi)"
read -r -p "API_ID > " api_id

if [[ $api_id = "" ]]; then
  api_id="2040"
  api_hash="b18441a1ff607e10a989891a5462e627"
else
  read -r -p "API_HASH > " api_hash
fi

echo
echo "SET PM PERMIT limit warn nya"
read -r -p "PM_LIMIT warn limit > " pm_limit

if [[ $pm_limit = "" ]]; then
  pm_limit="3"
  echo "limit not provided by user set to default"
fi

echo
echo "Masukkan APIFLASH_KEY untuk webshot plugins"
echo "Lu bisa dapetin disini -> https://apiflash.com/dashboard/access_keys"
read -r -p "APIFLASH_KEY > " apiflash_key

if [[ $apiflash_key = "" ]]; then
  echo "NOTE: API tidak di set, jadi lunya gabisa menggunakan .webshot plugin"
fi

echo
echo "Masukkan RMBG_KEY untuk remove background module"
echo "Lu bisa dapetin disini -> https://www.remove.bg/dashboard#api-key"
read -r -p "RMBG_KEY > " rmbg_key

if [[ $rmbg_key = "" ]]; then
  echo "NOTE: API Tidak di set, Lu tidak akan bisa menggunakan remove background modules"
fi

echo
echo "Masukkan GEMINI_KEY jika lu ingin menggunakan AI"
echo "NOTE: Jangan gunakan, Kecuali lu punya cukup penyimpanannya"
echo "MIN. REQ. STORAGE: 128GB"
echo "Lu bisa dapetin disini -> https://makersuite.google.com/app/apikey"
read -r -p "GEMINI_KEY > " gemini_key

if [[ $gemini_key = "" ]]; then
  echo "NOTE: API Tidak di set, Lu tidak akan bisa menggunakan Gemini AI modules"
fi

echo
echo "Masukkan COHERE_KEY jika lu pengen menggunakan AI"
echo "Lu bisa dapetin disini -> https://dashboard.cohere.com/api-keys"
read -r -p "COHERE_KEY > " cohere_key

if [[ $cohere_key = "" ]]; then
  echo "NOTE: API Tidak di set, Lu tidak akan bisa menggunakan Coral AI modules"
fi

echo
echo "Masukkan VT_KEY untuk VirusTotal"
echo "Lu bisa dapetin disini -> https://www.virustotal.com/"
read -r -p "VT_KEY > " vt_key

if [[ $vt_key = "" ]]; then
  echo "NOTE: API Tidak di set, Lu tidak akan bisa menggunakan VirusTotal module"
fi

echo
echo "Masukkan VCA_API_KEY for aiutils"
echo "Learn How to Get One --> https://github.com/VisionCraft-org/VisionCraft?tab=readme-ov-file#obtaining-an-api-key"
read -r -p "VCA_API_KEY > " vca_api_key

if [[ $vca_api_key = "" ]]; then
  echo "NOTE: API Tidak di set, Lu tidak akan bisa menggunakan aiutils module/pligins"
fi

echo "Choose database type:"
echo "[1] MongoDB (your url)"
echo "[2] Sqlite"
read -r -p "> " db_type

if [[ $db_type = 1 ]]; then
  echo "Please Masukkan db_url"
  echo "Lu bisa dapetin disini -> https://telegra.ph/How-to-get-Mongodb-URL-and-login-in-telegram-08-01"
  read -r -p "> " db_url
  db_name=Moon_Userbot
  db_type=mongodb
else
  db_name=db.sqlite3
  db_type=sqlite3
fi

cat > .env << EOL
API_ID=${api_id}
API_HASH=${api_hash}

STRINGSESSION=

# sqlite/sqlite3 or mongo/mongodb
DATABASE_TYPE=${db_type}
# file name for sqlite3, database name for mongodb
DATABASE_NAME=${db_name}

# only for mongodb
DATABASE_URL=${db_url}

APIFLASH_KEY=${apiflash_key}
RMBG_KEY=${rmbg_key}
VT_KEY=${vt_key}
GEMINI_KEY=${gemini_key}
COHERE_KEY=${cohere_key}
VCA_API_KEY=${vca_api_key}
PM_LIMIT=${pm_limit}
EOL

python3 install.py 3 || exit 3

echo
echo "============================"
echo "Great! Moon-Userbot installed successfully!"
echo "Start with: \"cd Moon-Userbot && python3 main.py\""
echo "============================"