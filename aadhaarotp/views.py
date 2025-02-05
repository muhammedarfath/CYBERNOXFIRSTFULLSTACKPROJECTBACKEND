from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests

# Sandbox API Configuration
SANDBOX_API_KEY = "key_live_ActHU7QgqxUJ82vwSZCwoDAOeujDUjgR"
SANDBOX_BASE_URL = "https://api.sandbox.co.in/kyc/aadhaar/okyc"
AUTH_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJhdWQiOiJBUEkiLCJyZWZyZXNoX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpVeE1pSjkuZXlKaGRXUWlPaUpCVUVraUxDSnpkV0lpT2lKbGJHOXlZVzFoZEhKcGJXOXVlVUJuYldGcGJDNWpiMjBpTENKaGNHbGZhMlY1SWpvaWEyVjVYMnhwZG1WZlFXTjBTRlUzVVdkeGVGVktPREoyZDFOYVEzZHZSRUZQWlhWcVJGVnFaMUlpTENKcGMzTWlPaUpoY0drdWMyRnVaR0p2ZUM1amJ5NXBiaUlzSW1WNGNDSTZNVGMzTURFek5EWXpOQ3dpYVc1MFpXNTBJam9pVWtWR1VrVlRTRjlVVDB0RlRpSXNJbWxoZENJNk1UY3pPRFU1T0RZek5IMC5VRjc5eFBRVnZiaENDMjA2ZWN6bVEyZXlGZ3llcm0ycEE4SnhZSmRsSDlNT3luc2dWbEFpYzQxNnBwTVdLYjYzSVZ5SDg3WVh4Q1BRaWN1dkV2dGJ6USIsInN1YiI6ImVsb3JhbWF0cmltb255QGdtYWlsLmNvbSIsImFwaV9rZXkiOiJrZXlfbGl2ZV9BY3RIVTdRZ3F4VUo4MnZ3U1pDd29EQU9ldWpEVWpnUiIsImlzcyI6ImFwaS5zYW5kYm94LmNvLmluIiwiZXhwIjoxNzM4Njg1MDM0LCJpbnRlbnQiOiJBQ0NFU1NfVE9LRU4iLCJpYXQiOjE3Mzg1OTg2MzR9.4Q4pNP7p_xgb5bWZc7Y3bslQwUlqlK_ZcyaLFq2XNRdExxp7ro-U_cyT92ucDAuAqiyIC_wghAwusU9YmoY2vg"


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
                "otp": otp,
                "reference_id": ref_id
            }
            
            headers = {
                "accept": "application/json",
                "authorization": AUTH_TOKEN,
                "x-api-key": SANDBOX_API_KEY,
                "x-api-version": "2.0",
                "content-type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            print(response,"check this")
            
            result = response.json()
            
            if response.status_code == 200 and result.get("success"):
                return Response({"message": "OTP verified successfully", "aadhaar_data": result.get("data")})
            else:
                return Response({"message": result.get("message", "Invalid OTP")}, status=400)
        
        except Exception as e:
            return Response({"message": "Error verifying OTP", "error": str(e)}, status=500)