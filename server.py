from concurrent import futures
import time
import sys
import logging
import grpc
import storage_service_pb2
import storage_service_pb2_grpc
from utils import load_config

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
global configs

class StorageServer(storage_service_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.storage = {}

    def Get(self, request, context):
        if request.key in self.storage:
            return storage_service_pb2.GetResponse(value=str(self.storage[request.key]), ret=1)
        else:
            return storage_service_pb2.GetResponse(ret=0)

    def Put(self, request, context):
        self.storage[request.key] = request.value
        self.broadcast_to_all_nodes(request)
        return storage_service_pb2.PutResponse(ret=1)

    def broadcast_to_all_nodes(self, request):
        for ip, port in all_nodes:
            with grpc.insecure_channel(ip+':'+port) as channel:
                stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)
                stub.Put(request)


def serve():
    configs = load_config()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage_service_pb2_grpc.add_KeyValueStoreServicer_to_server(StorageServer(), server)
    server.add_insecure_port(ip+':'+port)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    config = sys.argv[1]
    ip = sys.argv[2]
    port = sys.argv[3]
    serve()