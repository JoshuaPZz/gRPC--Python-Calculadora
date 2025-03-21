import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

IP_SERVIDOR_SUMA = "10.43.96.14"
IP_SERVIDOR_MULTI = "10.43.96.14"

class CentralServidor (calculator_pb2_grpc.CentralServiceServicer):
    def ProcessNumbers(self, request, context):
        
        with grpc.insecure_channel(f'{IP_SERVIDOR_SUMA}:50052') as channel_suma:
            stub_suma = calculator_pb2_grpc.SumServiceStub(channel_suma)
            respuesta_suma = stub_suma.SumarNumeros(calculator_pb2.DosNumeros(
                num1=request.num1,
                num2=request.num2
            ))
        
        with grpc.insecure_channel(f'{IP_SERVIDOR_MULTI}:50053') as channel_multi:
            stub_multi = calculator_pb2_grpc.MultiplyServiceStub(channel_multi)
            respuesta_final = stub_multi.MultiplicarNumeros(calculator_pb2.DosNumeros(
                num1=respuesta_suma.result,
                num2=request.num3
            ))
            
        print(f"Servidor central: ({request.num1} + {request.num2}) * {request.num3} = {respuesta_final.result}")
        
        return calculator_pb2.ClientResponse(result=respuesta_final.result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CentralServiceServicer_to_server(
        CentralServidor(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print(f"Servidor Central iniciando en el puerto 50051...")
    print(f"Conectado al servidor de suma en {IP_SERVIDOR_SUMA}:50052")
    print(f"Conectado al servidor de multiplicación en {IP_SERVIDOR_MULTI}:50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()