import core.utils.Logger

import atexit
from concurrent import futures

import grpc

from settings import SETTINGS
from core.bases import CONNECTION_DATABASE
from core.helpers.KeyManagerHelper import KEY_MANAGER_HELPER
from apps.protobufs.keys_pairs_pb2_grpc import add_KeysPairsServiceServicer_to_server



def main() -> None:
    """
        Main function to start the gRPC server.
        Starts the gRPC server and configures it to handle incoming requests.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_KeysPairsServiceServicer_to_server(KEY_MANAGER_HELPER, server)

    # Configure the port on which the server will listen for gRPC requests.
    server.add_insecure_port('[::]:50051')
    server.start()  # Start the gRPC server.

    # Confirmation message that the server is running.
    print("gRPC persistor server working")

    # Create tables if they do not exist yet.
    if SETTINGS.EXISTS_TABLES:
        CONNECTION_DATABASE.create_all()

    # Wait until the gRPC server finishes its execution.
    server.wait_for_termination()



def disconnect() -> None:
    """
        Closes the connection to the database at
        the end of program execution.
    """
    CONNECTION_DATABASE.close()



if __name__ == "__main__":
    atexit.register(lambda: disconnect())
    main()