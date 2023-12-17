import pytz
import base64
from datetime import datetime, timedelta

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from settings import SETTINGS
from core.bases import CONNECTION_DATABASE
from core.databases.Models import KeyPair
import apps.protobufs.keys_pairs_pb2 as keys_pairs_pb2
from apps.protobufs.keys_pairs_pb2_grpc import KeysPairsServiceServicer



class KeyManagerHelper(KeysPairsServiceServicer):
    """
        Class implementing a gRPC service to manage cryptographic key pairs.
    """


    def __init__(self, encryption_key: str = SETTINGS.VAULT_SECRET_KEY) -> None:
        """
            Initializes an instance of KeyManagerHelper.

            Args:
                encryption_key (str): Encryption key used to protect the data.
        """
        self.encryption_key = encryption_key


    def key_is_expired(self, key_pair):
        """
            Checks if a key pair has expired.

            Args:
                key_pair: The key pair to check.

            Returns:
                bool: True if the key pair has expired, False otherwise.
        """
        expiration_date = key_pair.created_at + timedelta(days=1)
        expiration_date = expiration_date.replace(tzinfo=pytz.UTC)
        return datetime.now(pytz.UTC) > expiration_date


    def keysPairs(self, request, context):
        """
            Implements the gRPC service to get key pairs.

            Args:
                request: gRPC request.
                context: gRPC context.

            Returns:
                keys_pairs_pb2.EncryptKeysResponse: gRPC response containing encrypted data.
        """
        system_code = request.system_code
        latest_key_pair = self.get_latest_key_pair(system_code)

        if latest_key_pair and not self.key_is_expired(latest_key_pair):
            encrypted_data = self.encrypt_keys(
                latest_key_pair.private_key,
                latest_key_pair.public_key,
                latest_key_pair.refresh_private_key,
                latest_key_pair.refresh_public_key
            )
        else:
            encrypted_data = self.generate_and_encrypt_keys(system_code)

        response = keys_pairs_pb2.EncryptKeysResponse()
        response.encrypted_data = encrypted_data
        return response


    def generate_and_encrypt_keys(self, system_code):
        """
            Generates key pairs, stores them in the database, then encrypts and returns the encrypted data.

            Args:
                system_code (str): Code of the system for which keys are generated.

            Returns:
                str: Encrypted data in string format.
        """
        private_key, public_key, refresh_private_key, refresh_public_key = self.generate_keys()

        key_pair = KeyPair(
            system_code=system_code,
            private_key=private_key,
            public_key=public_key,
            refresh_private_key=refresh_private_key,
            refresh_public_key=refresh_public_key
        )
        with CONNECTION_DATABASE as session:
            session.add(key_pair)
            session.commit()

        return self.encrypt_keys(private_key, public_key, refresh_private_key, refresh_public_key)


    def encrypt_keys(self, private_key, public_key, refresh_private_key, refresh_public_key):
        """
            Encrypts key pair data and returns it as an encrypted string.

            Args:
                private_key (str): Private key.
                public_key (str): Public key.
                refresh_private_key (str): Refresh private key.
                refresh_public_key (str): Refresh public key.

            Returns:
                str: Encrypted data in string format.
        """
        data_to_encrypt = {
            "private_key": private_key,
            "public_key": public_key,
            "refresh_private_key": refresh_private_key,
            "refresh_public_key": refresh_public_key,
        }

        cipher_suite = Fernet(self.encryption_key)
        encrypted_data = cipher_suite.encrypt(str(data_to_encrypt).encode('utf-8'))

        return encrypted_data.decode('utf-8')


    def generate_keys(self):
        """
            Generates cryptographic key pairs and returns their base64 representations.

            Returns:
                Tuple[str, str, str, str]: Tuple with generated keys in base64.
        """
        private_key = ec.generate_private_key(ec.SECP256R1())
        refresh_private_key = ec.generate_private_key(ec.SECP256R1())

        public_key = private_key.public_key()
        refresh_public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        refresh_private_key_pem = refresh_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        refresh_public_key_pem = refresh_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        private_key_base64 = base64.b64encode(private_key_pem).decode("utf-8")
        refresh_private_key_base64 = base64.b64encode(refresh_private_key_pem).decode("utf-8")
        public_key_base64 = base64.b64encode(public_key_pem).decode("utf-8")
        refresh_public_key_base64 = base64.b64encode(refresh_public_key_pem).decode("utf-8")

        return private_key_base64, public_key_base64, refresh_private_key_base64, refresh_public_key_base64


    def get_latest_key_pair(self, system_code):
        """
            Gets the latest key pair for a specific system from the database.

            Args:
                system_code (str): Code of the system for which the key pair is sought.

            Returns:
                KeyPair: The latest key pair or None if none is found.
        """
        with CONNECTION_DATABASE as session:
            return session.query(
                KeyPair
            ).filter_by(
                system_code=system_code
            ).order_by(
                KeyPair.created_at.desc()
            ).first()



KEY_MANAGER_HELPER: KeyManagerHelper = KeyManagerHelper()
