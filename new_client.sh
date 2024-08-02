# Generates the custom client.ovpn

new_client()
{
       { cat /etc/openvpn/server/client-common.txt
        echo "<ca>"
        cat /etc/openvpn/server/easy-rsa/pki/ca.crt
        echo "</ca>"
        echo "<cert>"
        sed -ne '/BEGIN CERTIFICATE/,$ p' /etc/openvpn/server/easy-rsa/pki/issued/"$client".crt
        echo "</cert>"
        echo "<key>"
        cat /etc/openvpn/server/easy-rsa/pki/private/"$client".key
        echo "</key>"
        echo "<tls-crypt>"
        sed -ne '/BEGIN OpenVPN Static key/,$ p' /etc/openvpn/server/tc.key
        echo "</tls-crypt>"
        } > "$old_path"/ovpn_keys/"$client".ovpn
}

client="$1"

old_path="$PWD"
cd /etc/openvpn/server/easy-rsa/
./easyrsa --batch --days=3650 build-client-full "$client" nopass

new_client

