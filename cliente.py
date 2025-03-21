import grpc
import calculator_pb2
import calculator_pb2_grpc
import argparse

def run(ip_central):
    # Conectar con el servidor principal usando la IP proporcionada
    with grpc.insecure_channel(f'{ip_central}:50051') as channel:
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
    parser = argparse.ArgumentParser(description='Cliente gRPC')
    parser.add_argument('--ip-central', type=str, required=True, help='Dirección IP del servidor central')
    args = parser.parse_args()
    
    run(args.ip_central)