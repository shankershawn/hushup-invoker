import oracledb

from com.shankarsan.secrets.vault import Vault


class Connection:
    connection_pool = None

    @classmethod
    def create_pool(cls, token):
        if cls.connection_pool is None:
            print('creating pool')
            password, wallet_password = Vault.get_database_credentials(token)
            cls.connection_pool = oracledb.create_pool(min=2,
                                                       max=4,
                                                       wallet_location='./Wallet_S5YMGS75R488XP8R',
                                                       dsn='s5ymgs75r488xp8r_high',
                                                       config_dir='./Wallet_S5YMGS75R488XP8R',
                                                       user='admin',
                                                       password=password,
                                                       wallet_password=wallet_password,
                                                       port=1522)

    @classmethod
    def get_connection_from_pool(cls, token):
        cls.create_pool(token)
        return cls.connection_pool.acquire()
