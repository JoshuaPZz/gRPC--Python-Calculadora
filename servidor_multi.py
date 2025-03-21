import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class MultiServidor(calculator_pb2_grpc.MultiplyServiceServicer):
    def MultiplicarNumeros(self, request, context):
        print("📥 SERVIDOR DE MULTIPLICACIÓN - DATOS RECIBIDOS:")
        print(f"   Número 1 (resultado de suma): {request.num1}")
        print(f"   Número 2 (tercer número): {request.num2}")
        resultado = request.num1 * request.num2
        print("\n🧮 OPERACIÓN REALIZADA:")
        print(f"   {request.num1} * {request.num2} = {resultado}")
        print(f"Servidor de Multiplicacion: {request.num1} * {request.num2} = {resultado}")
        print("\n📤 ENVIANDO RESULTADO:")
        return calculator_pb2.Resultado(result=resultado)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_MultiplyServiceServicer_to_server(
        MultiServidor(), server)
    server.add_insecure_port('[::]:50053')
    print("🚀 INICIANDO SERVIDOR DE MULTIPLICACIÓN")
    print(f"📡 Escuchando en: 10.43.96.14:50053")
    server.start()
    print("Servidor de Multiplicacion iniciado en puerto 50053...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()