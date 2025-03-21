import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    # Conectar con el servidor principal
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CentralServiceStub(channel)
        
        num1 = int(input("Ingrese el primer número: "))
        num2 = int(input("Ingrese el segundo número: "))
        num3 = int(input("Ingrese el tercer número: "))
        
        response = stub.ProcessNumbers(calculator_pb2.ClientRequest(
            num1=num1,
            num2=num2,
            num3=num3
        ))
        
        print(f"Resultado: {response.result}")

if __name__ == '__main__':
    run()