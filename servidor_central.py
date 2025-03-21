import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc
import argparse

class CentralServidor (calculator_pb2_grpc.CentralServiceServicer):
    def __init__(self, ip_suma, ip_multi):
        self.ip_suma = ip_suma
        self.ip_multi = ip_multi
        
    def ProcessNumbers(self, request, context):
        
        with grpc.insecure_channel(f'{self.ip_suma}:50052') as channel_suma:
            stub_suma = calculator_pb2_grpc.SumServiceStub(channel_suma)
            respuesta_suma = stub_suma.SumarNumeros(calculator_pb2.DosNumeros(
                num1=request.num1,
                num2=request.num2
            ))
        
        with grpc.insecure_channel(f'{self.ip_multi}:50053') as channel_multi:
            stub_multi = calculator_pb2_grpc.MultiplyServiceStub(channel_multi)
            respuesta_final = stub_multi.MultiplicarNumeros(calculator_pb2.DosNumeros(
                num1=respuesta_suma.result,
                num2=request.num3
            ))
            
        print(f"Servidor central: ({request.num1} + {request.num2}) * {request.num3} = {respuesta_final.result}")
        
        return calculator_pb2.ClientResponse(result=respuesta_final.result)

def serve(ip_suma, ip_multi):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CentralServiceServicer_to_server(
        CentralServidor(ip_suma, ip_multi), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print(f"Servidor Central iniciando en el puerto 50051...")
    print(f"Conectado al servidor de suma en {ip_suma}:50052")
    print(f"Conectado al servidor de multiplicación en {ip_multi}:50053")
    server.wait_for_termination()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Servidor Central gRPC')
    parser.add_argument('--ip-suma', type=str, required=True, help='Dirección IP del servidor de suma')
    parser.add_argument('--ip-multi', type=str, required=True, help='Dirección IP del servidor de multiplicación')
    args = parser.parse_args()
    
    serve(args.ip_suma, args.ip_multi)