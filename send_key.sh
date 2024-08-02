
chat_id="$1"
token="$2"
file_path="./ovpn_keys/$3.ovpn"

curl -v -F \"chat_id="$chat_id"\" -F document=@"$file_path" https://api.telegram.org/bot"$token"/sendDocument
