import logging
import sys
import grpc
import random
import storage_service_pb2
import storage_service_pb2_grpc
from utils import load_config

global configs


def pickANodeRandomly():
    n = len(configs['nodes'])
    index = random.randint(0, n-1)
    print('response from server #:' + str(index))
    return configs['nodes'][index]


def get(key):
    ip, port = pickANodeRandomly()
    with grpc.insecure_channel(ip+':'+port) as channel:
        stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.Get(storage_service_pb2.GetRequest(key=key))
        if response.ret == 0:
            print(response.value)
        else:
            print('Failed!')


def put(key, value):
    ip, port = pickANodeRandomly()
    with grpc.insecure_channel(ip+':'+port) as channel:
        stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)
        try:
            response = stub.Put(storage_service_pb2.PutRequest(key=key, value=value))
            if response.ret == 0:
                print('Success!')
        except Exception as e:
            print('RPC call failed!\n' + str(e))


if __name__ == '__main__':
    logging.basicConfig()
    config_path = sys.argv[1]
    configs = load_config(config_path)
    operation = sys.argv[2]
    if operation == 'get':
        key = sys.argv[3]
        get(key)
    elif operation == 'put':
        key = sys.argv[3]
        value = sys.argv[4]
        put(key, value)
    else:
        print("Invalid operation")