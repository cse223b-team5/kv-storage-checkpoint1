import logging
import grpc
import storage_service_pb2
import storage_service_pb2_grpc

def run():
	channel = grpc.insecure_channel('localhost:50051')
	stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)

if __name__ == '__main__':
    logging.basicConfig()
    run()