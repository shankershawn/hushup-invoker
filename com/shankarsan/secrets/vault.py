import hvac


class Vault:
    client = None

    @classmethod
    def get_database_credentials(cls, token):
        client = hvac.Client(
            url='http://144.24.128.195:8200',
            token=token,
        )
        read_response = client.secrets.kv.read_secret(path='com-shankarsan')
        password = read_response['data']['data']['oci_db_password']
        wallet_password = read_response['data']['data']['oci_db_wallet_password']
        return password, wallet_password
