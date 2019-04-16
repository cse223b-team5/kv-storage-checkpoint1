from concurrent import futures
import time
import sys
import logging
import random
import grpc
import storage_service_pb2
import storage_service_pb2_grpc
import chaosmonkey_pb2
import chaosmonkey_pb2_grpc
from utils import load_config
from chaos_server import ChaosServer

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
                break
            self.node_index += 1

    def Get(self, request, context):
        if request.key in self.storage:
            return storage_service_pb2.GetResponse(value=str(self.storage[request.key]), ret=0)
        else:
            return storage_service_pb2.GetResponse(ret=1)

    def Put(self, request, context):
        global conn_mat
        try:
            conn_mat
            print('ConnMax exists')
        except Exception as e:
            print('ConnMax does not exist')
        self.storage[request.key] = request.value
        self.broadcast_to_all_nodes(request)
        return storage_service_pb2.PutResponse(ret=0)

    def Put_from_broadcast(self, request, context):
        print('Node #' + str(self.node_index) + ' receives rpc call from node #' + request.from_node)

        global conn_mat
        try:
            conn_mat
        except Exception as e:
            print('ConnMat hasn\'t been uploaded. No msg is ignored')
            self.storage[request.key] = request.value
            return storage_service_pb2.PutResponse(ret=0)

        # read threshold from conn_mat
        i = int(request.from_node)
        j = int(self.node_index)
        threshold = float(conn_mat.rows[i].vals[j])

        if random.random() > threshold:
            # drop this request
            time_to_sleep = random.randint(5, 10) / 10  # sleep for random duration between 0.5-1 sec
            time.sleep(time_to_sleep)
            print('broadcast from node #' + str(request.from_node) + 'to node #' + str(self.node_index) + ' was ignored')
            return storage_service_pb2.PutResponse(ret=1)
        else:
            self.storage[request.key] = request.value
            return storage_service_pb2.PutResponse(ret=0)

    def broadcast_to_all_nodes(self, request):
        print('Start broadcast to other nodes')
        for ip, port in self.configs['nodes']:
            if ip != self.myIp or port != self.myPort:
                print('Addr to connect: ' + ip + ":" + port)
                with grpc.insecure_channel(ip+':'+port) as channel:
                    stub = storage_service_pb2_grpc.KeyValueStoreStub(channel)
                    try:
                        response = stub.Put_from_broadcast(storage_service_pb2.PutRequestToOtherServer(
                            key=request.key, value=request.value, from_node=str(self.node_index)))
                        print('Response from port' + str(port) + ":" + str(response.ret))
                    except Exception as e:
                        print('RPC call failed! (broadcast)')


class ChaosServer(chaosmonkey_pb2_grpc.ChaosMonkeyServicer):
    def UploadMatrix(self, request, context):
        global conn_mat
        conn_mat = request
        print('New ConnMat uploaded')
        return chaosmonkey_pb2.Status(ret=0)

    def UpdateValue(self, request, context):
        global conn_mat
        if request.row >= len(conn_mat.rows) or request.col >= len(conn_mat.rows[request.row].vals):
            return chaosmonkey_pb2.Status(ret=1)
        conn_mat.rows[request.row].vals[request.col] = request.val
        print('New edit to ConnMat')
        return chaosmonkey_pb2.Status(ret=0)


def serve(config_path, myIp, myPort):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage_service_pb2_grpc.add_KeyValueStoreServicer_to_server(StorageServer(config_path, myIp, myPort), server)
    chaosmonkey_pb2_grpc.add_ChaosMonkeyServicer_to_server(ChaosServer(), server)

    server.add_insecure_port(myIp+':'+myPort)
    try:
        server.start()
    except Exception as e:
        print('Server start failed!')
        print(str(e))

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