import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class MultiServidor(calculator_pb2_grpc.MultiplyServiceServicer):
    def MultiplicarNumeros(self, request, context):
        resultado = request.num1 * request.num2
        print(f"Servidor de Multiplicacion: {request.num1} * {request.num2} = {resultado}")
        return calculator_pb2.Resultado(result=resultado)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_MultiplyServiceServicer_to_server(
        MultiServidor(), server)
    server.add_insecure_port('0.0.0.0:50053')
    server.start()
    print("Servidor de Multiplicacion iniciado en puerto 50053...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()