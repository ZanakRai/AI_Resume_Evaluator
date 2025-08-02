from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import JobSerializer,ResumeSerializer
from rest_framework.response import Response
from .models import JobDescription,Resume
from .analyzer import process_resume



# Create your views here.

class JobDescriptionView(APIView):
    def get(self,request):
        objs=JobDescription.objects.all()
        serializer=JobSerializer(objs, many=True)
        return Response(serializer.data)



    def post(self,request):
        data=request.data
        serializer=JobSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors)
    
class ResumeAPIView(APIView):
    def post(self,request):
        try:
            data=request.data
            if not data.get('job_description'):
                return Response({
                    'status':False,
                    'message':'job_description is required'
                })
            
            serializer=ResumeSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    "status":False,
                    "message":"Invalid data",
                    "data":serializer.errors
                })
            
            serializer.save()
            _data=serializer.data
            resume_instance=Resume.objects.get(id=_data['id'])
            resume_path=resume_instance.resume.path
            data=process_resume(resume_path,JobDescription.objects.get(id=data.get('job_description')).job_description)

            return Response({
                "status":True,
                "data":data
            })

        
        except Exception as e:
            return str(e)
        
    
            


