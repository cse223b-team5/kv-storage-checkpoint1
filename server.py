import logging
import grpc
import storage_service_pb2
import storage_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class StorageServer(helloworld_pb2_grpc.GreeterServicer):
	def Get(self, request, context):

	def Put(self, request, context):

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage_service_pb2_grpc.add_KeyValueStoreServicer_to_server(StorageServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig()
    serve()