from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests

# Sandbox API Configuration
SANDBOX_API_KEY = "key_live_ActHU7QgqxUJ82vwSZCwoDAOeujDUjgR"
SANDBOX_BASE_URL = "https://api.sandbox.co.in/kyc/aadhaar/okyc"
AUTH_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJhdWQiOiJBUEkiLCJyZWZyZXNoX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpVeE1pSjkuZXlKaGRXUWlPaUpCVUVraUxDSnpkV0lpT2lKbGJHOXlZVzFoZEhKcGJXOXVlVUJuYldGcGJDNWpiMjBpTENKaGNHbGZhMlY1SWpvaWEyVjVYMnhwZG1WZlFXTjBTRlUzVVdkeGVGVktPREoyZDFOYVEzZHZSRUZQWlhWcVJGVnFaMUlpTENKcGMzTWlPaUpoY0drdWMyRnVaR0p2ZUM1amJ5NXBiaUlzSW1WNGNDSTZNVGMzTURrMk1Ea3lOeXdpYVc1MFpXNTBJam9pVWtWR1VrVlRTRjlVVDB0RlRpSXNJbWxoZENJNk1UY3pPVFF5TkRreU4zMC5VUlhIdmtQRkx5ckdGWnRQUG50VHM4TFZZbWhVOHNnd3dMU05lRkQ5TUpvMWRBaUdxeXNtTjF6TDJVTUVueHR0VjU5eEh4WGJ5eVdEWVFScy1MT1VvZyIsInN1YiI6ImVsb3JhbWF0cmltb255QGdtYWlsLmNvbSIsImFwaV9rZXkiOiJrZXlfbGl2ZV9BY3RIVTdRZ3F4VUo4MnZ3U1pDd29EQU9ldWpEVWpnUiIsImlzcyI6ImFwaS5zYW5kYm94LmNvLmluIiwiZXhwIjoxNzM5NTExMzI3LCJpbnRlbnQiOiJBQ0NFU1NfVE9LRU4iLCJpYXQiOjE3Mzk0MjQ5Mjd9.S6Dprs7NgszWIhvVxCURepXau7oC--Px4IAN9mvlqcPWCBI5cMP2CozPMGI69vIu2ntvf19nH4Utzbilh5SWRA"


class SendOtpView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            aadhaar_number = request.data.get("aadhaar_number")
            print(aadhaar_number)
            if not aadhaar_number or len(aadhaar_number) != 12:
                return Response({"message": "Invalid Aadhaar number"}, status=400)
            
            url = f"{SANDBOX_BASE_URL}/otp"
            headers = {
                "Authorization": AUTH_TOKEN,
                "Content-Type": "application/json",
                "x-api-key": SANDBOX_API_KEY
            }
            payload = {
                "@entity": "in.co.sandbox.kyc.aadhaar.okyc.otp.request",
                "reason": "For KYC",
                "consent": "Y",
                "aadhaar_number": aadhaar_number
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
                
            if response.status_code == 200:
                result = response.json()
                return Response({"message": "OTP sent", "result": result})
            else:
                return Response({"message": "Failed to send OTP", "details": response.text}, status=response.status_code)
        except Exception as e:
            return Response({"message": "Error sending OTP", "error": str(e)}, status=500)

class VerifyOtpView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            ref_id = request.data.get("referenceId")
            otp = request.data.get("otp")
            
            print(ref_id,"ref id ")
            print(otp,"otp ")
            
            if not ref_id or not otp:
                return Response({"message": "Missing referenceId or OTP"}, status=400)
            
            url = f"{SANDBOX_BASE_URL}/otp/verify"
            
            payload = {
                "@entity": "in.co.sandbox.kyc.aadhaar.okyc.request",
                "otp": str(otp),
                "reference_id": str(ref_id)
            }
            
            headers = {
                "accept": "application/json",
                "authorization": AUTH_TOKEN,
                "x-api-key": SANDBOX_API_KEY,
                "x-api-version": "2.0",
                "content-type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            

            result = response.json()
            
            if response.status_code == 200:
                return Response({"message": "OTP verified successfully", "aadhaar_data": result.get("data")})
            else:
                return Response({"message": result.get("message", "Invalid OTP")}, status=400)
        
        except Exception as e:
            return Response({"message": "Error verifying OTP", "error": str(e)}, status=500)