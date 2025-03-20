import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class CentralServidor (calculator_pb2_grpc.CentralService):
    def ProcesarNumeros (self,request,context):
        