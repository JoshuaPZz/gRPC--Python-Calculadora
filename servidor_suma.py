import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class SumarServidor (calculator_pb2_grpc.SumServiceServicer):
    def SumarNumeros(self, request, context):
        print("📥 SERVIDOR DE SUMA - DATOS RECIBIDOS:")
        print(f"   Número 1: {request.num1}")
        print(f"   Número 2: {request.num2}")
        resultado = request.num1 + request.num2
        print("\n🧮 OPERACIÓN REALIZADA:")
        print(f"   {request.num1} + {request.num2} = {resultado}")
        print(f"Servidor de Suma: {request.num1} + {request.num2} = {resultado}")

        print("\n📤 ENVIANDO RESULTADO:")
        return calculator_pb2.Resultado(result=resultado)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_SumServiceServicer_to_server(
        SumarServidor(), server)
    server.add_insecure_port('[::]:50052')

    print("🚀 INICIANDO SERVIDOR DE SUMA")
    print(f"📡 Escuchando en: 10.43.96.14:50052")
    
    server.start()
    print("Servidor de Suma iniciado en puerto 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()