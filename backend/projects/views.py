# # views.py
# from rest_framework import generics
# from rest_framework import viewsets
# from yaml import serialize
# from django.db import transaction
from django.core.mail import EmailMessage
import logging
from django.core.files.uploadedfile import InMemoryUploadedFile


from django.shortcuts import get_object_or_404

from .models import Project, Project_detail
from .serializers import ProjectSerializer, ProjectDetailSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView


from rest_framework.decorators import api_view
from .models import Project, Contract, Insurance, Bond,  Submittals, ShopDrawing, Safity, Schedule, Sub_Contractors, LaborRate,  HDS_system, Buget,Delay_Notice,RFI,PCO,Schedule_of_Value,RFI_Log,Delay_Log,Qualification,Debited_Material,Credited_Material,Labor,Miscellaneous
from .serializers import (ProjectSerializer, ContractSerializer,  InsuranceSerializer, BondSerializer,QualificationSerializer,DebitedMaterialSerializer,CreditedMaterialSerializer,LaborSerializer,MiscellaneousSerializer,
                           SubmittalsSerializer, ShopDrawingSerializer, SafitySerializer, ScheduleSerializer,PCO_Log,
                          SubContractorsSerializer, LaborRateSerializer,HDSSystemSerializer,
                          BugetSerializer,Delay_NoticeSerializer,RFISerializer,PCOSerializer,ScheduleOfValueSerializer,RFI_LogSerializer,Delay_LogSerializer,PCO_LogSerializer)



class ProjectDetailListCreateView(APIView):
    def get(self, request, prjct_id):
        # Filter details based on the prjct_id
        project_details = Project_detail.objects.filter(prjct_id=prjct_id ,prnt_id__isnull=True)

        # Serialize the data
        serializer = ProjectDetailSerializer(project_details, many=True)

        # Return the serialized data
        return Response(serializer.data)

    # def get(self,request,id=None,format=None):
    #     if id:
    #         try:
    #             if(project)
    #         except:
    #             pass
# class ProjectDetailListCreateView(viewsets.ReadOnlyModelViewSet):
#     queryset = Project_detail.objects.filter(prnt_id__isnull=True)  # This fetches top-level directories
#     serializer_class = ProjectDetailSerializer


@api_view(['GET', 'POST','PUT'])
def create_project(request, id=None):

    related_data_models = [
            ('contract', Contract, ContractSerializer),
            ('schedule_of_value', Schedule_of_Value, ScheduleOfValueSerializer),
            ('insurance', Insurance, InsuranceSerializer),
            ('bond', Bond, BondSerializer),
            ('submittals', Submittals, SubmittalsSerializer),
            ('shop_drawing', ShopDrawing, ShopDrawingSerializer),
            ('safity', Safity, SafitySerializer),
            ('schedule', Schedule, ScheduleSerializer),
            ('sub_contractors', Sub_Contractors, SubContractorsSerializer),
            ('labor_rate', LaborRate, LaborRateSerializer),
            ('hds_system', HDS_system, HDSSystemSerializer),
            ('buget', Buget, BugetSerializer),
        ]



    if request.method == 'GET':
        if id:
            try:
                project = Project.objects.get(id=id)
                serializer = ProjectSerializer(project)
            except Project.DoesNotExist:
                return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        if isinstance(data, list):
            data = data[0]

        # Handle Project data
        project_serializer = ProjectSerializer(data=data)
        if not project_serializer.is_valid():
            return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        project = project_serializer.save()

        # Handle related models
        for key, model, serializer_class in related_data_models:
            related_data_list = data.get(key)
            if related_data_list:
                for related_data in related_data_list:
                    related_serializer = serializer_class(data=related_data)
                    if not related_serializer.is_valid():
                        return Response(related_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    related_serializer.save(project=project)

        return Response({"message": "Project and related data created successfully"}, status=status.HTTP_201_CREATED)

    if request.method == 'PUT':
        data = request.data
        if isinstance(data, list):
            data = data[0]
        project_id = id 

        if not project_id:
            return Response({"error": "Project id is required for update"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        project_serializer = ProjectSerializer(project, data=data)
        if not project_serializer.is_valid():
            return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        related_serializers = []
        for key, model, serializer_class in related_data_models:
            related_data = data.get(key)
            if related_data:
                # Check if related_data is a dictionary or a list
                if isinstance(related_data, dict):
                    related_data_list = [related_data]
                elif isinstance(related_data, list):
                    related_data_list = related_data
                else:
                    return Response({key: "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

                # Delete previous related records and create new ones (assuming a simple replacement strategy)
                model.objects.filter(project=project).delete()

                for related_data_item in related_data_list:
                    serializer = serializer_class(data=related_data_item)
                    if not serializer.is_valid():
                        return Response({key: serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    related_serializers.append(serializer)

        project_serializer.save()

        # Now save all related data with the project id
        for serializer in related_serializers:
            serializer.validated_data['project'] = project
            serializer.save()

        return Response({"message": "Project and related data updated successfully"}, status=status.HTTP_200_OK)


class RFIViews(APIView):
    def get(self, request, id=None):
        if id:
            rfi = get_object_or_404(RFI, id=id)
            serializer = RFISerializer(rfi)
        else:
            rfi = RFI.objects.all()
            serializer = RFISerializer(rfi, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RFISerializer(data=request.data)
        if serializer.is_valid():
            project_id = request.data.get('project_id')
            if project_id:
                project = get_object_or_404(Project, id=project_id)
                rfi_instance = serializer.save(project=project)

                # Create and save RFI_Log instance
                rfi_log_data = {
                    'rfi_id': rfi_instance.id, # type: ignore
                    'project_id':rfi_instance.project.id,#type:ignore
                }
                rfi_log_serializer = RFI_LogSerializer(data=rfi_log_data)
                if rfi_log_serializer.is_valid():
                    rfi_log_serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "project_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        rfi = get_object_or_404(RFI, id=id)
        serializer = RFISerializer(rfi, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        rfi = get_object_or_404(RFI, id=id)
        rfi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RFILogViews(APIView):
    def get(self, request, id=None):
        if id:
            rfi_log = get_object_or_404(RFI_Log, id=id)
            serializer = RFI_LogSerializer(rfi_log)
        else:
            rfi_log = RFI_Log.objects.all()
            serializer = RFI_LogSerializer(rfi_log, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RFI_LogSerializer(data=request.data)
        if serializer.is_valid():
            rfi_id = request.data.get('rfi_id')
            if rfi_id:
                rfi = get_object_or_404(RFI, id=rfi_id)
                serializer.save(rfi=rfi)
            else:
                serializer.save()  # Save without rfi_id
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        rfi_log = get_object_or_404(RFI_Log, id=id)
        serializer = RFI_LogSerializer(rfi_log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        rfi_log = get_object_or_404(RFI_Log, id=id)
        rfi_log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Delay_NoticeViews(APIView):

    def get(self, request,id=None):
        if id:
            try:
                delay_notice=Delay_Notice.objects.get(id=id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serialize=Delay_NoticeSerializer(delay_notice)
        else:
            delay_notice=Delay_Notice.objects.all()
            serialize=Delay_NoticeSerializer(delay_notice,many=True)
            
        return Response(serialize.data)
    
    
    

    def post(self, request):
        serialize = Delay_NoticeSerializer(data=request.data)
        if serialize.is_valid():
            delay_notice_instance = serialize.save()

            delay_log_data = {
                'dly_ntc_id': delay_notice_instance.id, # type: ignore
            }
            delay_log_serializer = Delay_LogSerializer(data=delay_log_data)
            if delay_log_serializer.is_valid():
                delay_log_serializer.save()

            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self,request,id=None):
        dly_ntc=get_object_or_404(Delay_Notice,id=id)
        serializer=Delay_NoticeSerializer(dly_ntc,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
    def delete(self,request,id=None):
        dly_ntc=get_object_or_404(Delay_Notice,id=id)
        dly_ntc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class Delay_LogViews(APIView):

    def get(self, request,id=None):
        if id:
            try:
                delay_log=Delay_Log.objects.get(id=id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serialize=Delay_LogSerializer(delay_log)
        else:
            delay_log=Delay_Log.objects.all()
            serialize=Delay_LogSerializer(delay_log,many=True)
            
        return Response(serialize.data)
    
    def post(self,request):
        serialize=Delay_LogSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.data,status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self,request,id=None):
        dly_log=get_object_or_404(Delay_Log,id=id)
        serializer=Delay_LogSerializer(dly_log,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id=None):
        dly_log=get_object_or_404(Delay_Log,id=id)
        dly_log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def create_pco(request, id=None):
    if request.method == 'GET':
        if id:
            try:
                pco = PCO.objects.get(pk=id)
                serializer = PCOSerializer(pco)
            except PCO.DoesNotExist:
                return Response({'message': 'The PCO does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            pcos = PCO.objects.all()
            serializer = PCOSerializer(pcos, many=True)
        return Response(serializer.data)

    # POST: Create a new PCO instance
    if request.method == 'POST':
        serializer = PCOSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PUT' and id is not None:
        try:
            pco = PCO.objects.get(pk=id)
        except PCO.DoesNotExist:
            return Response({'message': 'The PCO does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PCOSerializer(pco, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            update_nested_objects(request.data, pco)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE' and id is not None:
        try:
            pco = PCO.objects.get(pk=id)
            pco.delete()
            return Response({'message': 'PCO was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except PCO.DoesNotExist:
            return Response({'message': 'The PCO does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
def update_nested_objects(data, pco_instance):
    for nested_model, data_key in [
        (Qualification, 'qualifications'),
        (Debited_Material, 'debited_materials'),
        (Credited_Material, 'credited_materials'),
        (Miscellaneous, 'miscellaneous'),
        (Labor, 'labor')
    ]:
        provided_ids = set()
        for item_data in data.get(data_key, []):
            item_id = item_data.pop('id', None)
            
            if item_id:
                provided_ids.add(item_id)
                nested_model.objects.filter(id=item_id, pco=pco_instance).update(**item_data)
            else:
                nested_model.objects.create(pco=pco_instance, **item_data)

        nested_model.objects.filter(pco=pco_instance).exclude(id__in=provided_ids).delete()



class Pco_LogView(APIView):
    def get(self, request,id=None):
        if id:
            try:
                pco_log=PCO_Log.objects.get(id=id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serialize=PCO_LogSerializer(pco_log)
        else:
            pco_logs=PCO_Log.objects.all()
            serialize=PCO_LogSerializer(pco_logs,many=True)
            
        return Response(serialize.data)
    
    def post(self,request):
        serialize=PCO_LogSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data,status=status.HTTP_201_CREATED)
        return Response(serialize.data,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,id=None):
        pco_log=get_object_or_404(PCO_Log,id=id)
        serializer=PCO_LogSerializer(pco_log,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id=None):
        pco_log=get_object_or_404(PCO_Log,id=id)
        pco_log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SendRFIEmailView(APIView):
    def post(self, request, rfi_id, format=None):
        logger = logging.getLogger(__name__)

        try:
            rfi = RFI.objects.get(id=rfi_id)
            project = rfi.project

            recipient_email = project.attn_email  #type: ignore
            if not recipient_email:
                return Response({'error': 'Recipient email not found'}, status=status.HTTP_400_BAD_REQUEST)

            subject = 'RFI Details'
            message = """
            Hello,
            Here are the details of the RFI for project:
            ...
            Please review and let us know if there are any questions.
            Thank you
            """
            email = EmailMessage(subject, message, 'mubeenjutt9757@gmail.com', [recipient_email])
            email.content_subtype = 'html'

            pdf_file = request.FILES.get('pdf')
            if pdf_file:
                email.attach(pdf_file.name, pdf_file.read(), 'application/pdf')

            cc_emails = request.data.get('cc_emails')
            if cc_emails:
                cc_email_list = cc_emails.split(',')
                email.cc = [email.strip() for email in cc_email_list]

            email.send()
            return Response({'message': 'RFI email sent successfully!'})
        except RFI.DoesNotExist:
            return Response({'error': 'RFI not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Failed to send email', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)