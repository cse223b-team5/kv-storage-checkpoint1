from concurrent import futures
import time
import sys
import logging
import random
import grpc
import storage_service_pb2
import storage_service_pb2_grpc
from utils import load_config

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class StorageServer(storage_service_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, config_path, myIp, myPort):
        self.configs = load_config(config_path)
        self.myIp = myIp
        self.myPort = myPort
        self.storage = {}

        self.node_index = 0
        for t in self.configs['nodes']:
            if t[0] == myIp and t[1] == myPort:
                self.node_index += 1

    def Get(self, request, context):
        if request.key in self.storage:
            return storage_service_pb2.GetResponse(value=str(self.storage[request.key]), ret=1)
        else:
            return storage_service_pb2.GetResponse(ret=0)

    def Put(self, request, context):
        self.storage[request.key] = request.value
        self.broadcast_to_all_nodes(request)
        return storage_service_pb2.PutResponse(ret=1)

    def Put_from_broadcast(self, request, context):
        print('node #' + str(self.node_index) + ' receives rpc call from node #' + request.from_node)

        # read threshold from conn_mat
        i = request.from_node
        j = self.node_index
        threshold = float(self.conn_mat.rows[i].vals[j])

        if random.random() > threshold:
            time_to_sleep = random.randint(5, 10) / 10  # sleep for random duration between 0.5-1 sec
            time.sleep(time_to_sleep)
        else:
            self.storage[request.key] = request.value
            return storage_service_pb2.PutResponse(ret=1)

    def broadcast_to_all_nodes(self, request):
        print('start broadcast to other nodes')
        for ip, port in self.configs['nodes']:
            if ip != self.myIp or port != self.myPort:
                print('addr to connect: ' + ip + ":" + port)
                with grpc.insecure_channel(ip+':'+port) as channel:
                    stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)
                    response = stub.Put_from_broadcast(storage_service_pb2.PutRequestToOtherServer(
                        key=request.key, value=request.value, from_node=str(self.node_index)))
                    print('response from port' + str(port) + ":" + str(response.ret))


def serve(config_path, myIp, myPort):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage_service_pb2_grpc.add_KeyValueStoreServicer_to_server(StorageServer(config_path, myIp, myPort), server)
    server.add_insecure_port(myIp+':'+myPort)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    config_path = sys.argv[1]
    myIp = sys.argv[2]
    myPort = sys.argv[3]
    serve(config_path, myIp, myPort)