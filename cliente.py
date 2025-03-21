import grpc
import calculator_pb2
import calculator_pb2_grpc

IP_SERVIDOR_CENTRAL = "10.43.103.221"

def run():
    with grpc.insecure_channel(f'{IP_SERVIDOR_CENTRAL}:50051') as channel:
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