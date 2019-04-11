import logging
import grpc
import storage_service_pb2
import storage_service_pb2_grpc

def get(config, key):
	with grpc.insecure_channel('localhost:50051') as channel:
        stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.Get(storage_service_pb2.GetRequest(key=key))
     	print(response.message)

def put(config, key, value):
	with grpc.insecure_channel('localhost:50051') as channel:
        stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.Put(storage_service_pb2.PutRequest(key=key, value=value))
     	print(response.message)

if __name__ == '__main__':
    logging.basicConfig()
    config = sys.argv[1]
    operation = sys.argv[2]
    if operation == 'get':
    	key = sys.argv[3]
    	get(config, key)
    elif operation == 'put':
        key = sys.argv[3]
        value = sys.argv[4]
    	get(config, key, value)
    else:
        print("Invalid operation")