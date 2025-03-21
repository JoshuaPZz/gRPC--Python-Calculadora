import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc
import time

IP_SERVIDOR_SUMA = "10.43.96.14"
IP_SERVIDOR_MULTI = "10.43.96.14"

class CentralServidor(calculator_pb2_grpc.CentralServiceServicer):
    def ProcessNumbers(self, request, context):        
        suma_resultado = None
        resultado_final = None
        
        try:
            with grpc.insecure_channel(f'{IP_SERVIDOR_SUMA}:50052') as channel_suma:
                
                options = [('grpc.timeout_ms', 2000)]  # 2 segundos de timeout
                channel_suma = grpc.insecure_channel(f'{IP_SERVIDOR_SUMA}:50052', options=options)
                
                
                stub_suma = calculator_pb2_grpc.SumServiceStub(channel_suma)
                respuesta_suma = stub_suma.SumarNumeros(
                    calculator_pb2.DosNumeros(num1=request.num1, num2=request.num2),
                    timeout=2 
                )
                suma_resultado = respuesta_suma.result
                print(f"Usando servidor de suma externo: {request.num1} + {request.num2} = {suma_resultado}")
                
        except grpc.RpcError as e:
            suma_resultado = request.num1 + request.num2
            print(f"Fallback: Calculando suma localmente: {request.num1} + {request.num2} = {suma_resultado}")
                
        try:
            with grpc.insecure_channel(f'{IP_SERVIDOR_MULTI}:50053') as channel_multi:
                
                options = [('grpc.timeout_ms', 2000)] 
                channel_multi = grpc.insecure_channel(f'{IP_SERVIDOR_MULTI}:50053', options=options)
                
                
                stub_multi = calculator_pb2_grpc.MultiplyServiceStub(channel_multi)
                respuesta_multi = stub_multi.MultiplicarNumeros(
                    calculator_pb2.DosNumeros(num1=suma_resultado, num2=request.num3),
                    timeout=2 
                )
                resultado_final = respuesta_multi.result
                print(f"Usando servidor de multiplicación externo: {suma_resultado} * {request.num3} = {resultado_final}")
                
        except grpc.RpcError as e:
            
            resultado_final = suma_resultado * request.num3
            print(f"Fallback: Calculando multiplicación localmente: {suma_resultado} * {request.num3} = {resultado_final}")
        
        
        print(f"Servidor central: ({request.num1} + {request.num2}) * {request.num3} = {resultado_final}")
        
        
        return calculator_pb2.ClientResponse(result=resultado_final)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CentralServiceServicer_to_server(
        CentralServidor(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print(f"Servidor Central iniciando en el puerto 50051...")
    print(f"Configurado para conectarse al servidor de suma en {IP_SERVIDOR_SUMA}:50052")
    print(f"Configurado para conectarse al servidor de multiplicación en {IP_SERVIDOR_MULTI}:50053")
    print("Modo fallback: Si algún servidor no responde, se realizarán los cálculos localmente")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()