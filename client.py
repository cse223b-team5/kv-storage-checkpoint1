import logging
import sys
import grpc
import random
import storage_service_pb2
import storage_service_pb2_grpc


def pickANodeRandomly():
    n = len(configs['nodes'])
    index = random.randint(n)
    return configs['nodes'][index]


def get(key):
    ip, port = pickANodeRandomly()
    with grpc.insecure_channel(ip+':'+port) as channel:
        stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.Get(storage_service_pb2.GetRequest(key=key))
        if response.ret == 1:
            print(response.value)
        else:
            print('Failed!')


def put(key, value):
    ip, port = pickANodeRandomly()
    with grpc.insecure_channel(ip+':'+port) as channel:
        stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.Put(storage_service_pb2.PutRequest(key=key, value=value))
        if response.ret == 1:
            print('Success!')


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
        put(config, key, value)
    else:
        print("Invalid operation")