import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class CentralServidor (calculator_pb2_grpc.CentralService):
    def ProcessNumbers (self,request,context):
        
        with grpc.insecure_channel('localhost:50052') as channel_suma:
            stub_suma = calculator_pb2_grpc.SumServiceStub(channel_suma)
            respuesta_suma = stub_suma.SumarNumeros(calculator_pb2.DosNumeros(
                num1=request.num1,
                num2=request.num2
            ))
        
        with grpc.insecure_channel('localhost:50053') as channel_multi:
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
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor Central iniciando en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()