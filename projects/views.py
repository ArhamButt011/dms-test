# # views.py
# from rest_framework import generics
# from rest_framework import viewsets
# from yaml import serialize
# from django.db import transaction
from django.core.mail import EmailMessage
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import transaction

from email.mime.image import MIMEImage 
import logging
from django.db.models import Sum
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from django.http import Http404
from django.conf import settings

from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from backend import Estimating

from .models import Attached_Pdf_Delay, Attached_Pdf_Rfi_log, Project, Project_detail, WageRate
from BIM.serializers import BimSerializer
from .serializers import ProjectSerializer, ProjectDetailSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
import base64

from rest_framework.decorators import api_view,parser_classes
from .models import Project, Contract, Insurance, Bond,  Submittals, ShopDrawing, Safity, Schedule, Sub_Contractors, LaborRate,  HDS_system, Buget,Delay_Notice,RFI,PCO,Schedule_of_Value,RFI_Log,Delay_Log,Qualification,Debited_Material,Credited_Material,Labor,Miscellaneous,Attached_Pdf_Rfi,Attached_Pdf_Delay,Attached_Pdf_Pco,BadgingProject,WageRate
from .serializers import (ProjectSerializer, ContractSerializer,  InsuranceSerializer, BondSerializer,Attache_PDF_RFISerializer,Attache_PDF_DelaySerializer,QualificationSerializer,DebitedMaterialSerializer,CreditedMaterialSerializer,LaborSerializer,MiscellaneousSerializer,Attache_PDF_PCOSerializer,TM,Attached_Pdf_TM,Material,
                           SubmittalsSerializer, ShopDrawingSerializer, SafitySerializer, ScheduleSerializer,PCO_Log,
                          SubContractorsSerializer, LaborRateSerializer,HDSSystemSerializer,AddMoreSerializer,BadgingSerializer,WageRateSerializer,
                          BugetSerializer,Delay_NoticeSerializer,RFISerializer,PCOSerializer,ScheduleOfValueSerializer,RFI_LogSerializer,Delay_LogSerializer,PCO_LogSerializer,MetrialTMSerializers,LaborTMSerializers,MiscellaneousTM,TMSerializer)

from Estimating.models import DMS_Dertory,AttachedLogoCompany

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



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes((JSONParser, MultiPartParser))
def tm_view(request, id=None):
    if request.method == 'GET':
        if id:
            try:
                tm = TM.objects.get(pk=id)
                serializer = TMSerializer(tm)
                return Response(serializer.data)  # Make sure to return a response here
            except TM.DoesNotExist:
                return Response({'message': 'TM not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            tms = TM.objects.all()
            serializer = TMSerializer(tms, many=True)
            return Response(serializer.data)  # And here, return a response for all TMs if no id is provided

    elif request.method == 'POST':
        serializer = TMSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            tm_instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not id:
            return Response({"message": "ID is required for PUT request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tm = TM.objects.get(pk=id)
            serializer = TMSerializer(tm, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                tm_instance = serializer.save()
                Attached_Pdf_TM.objects.filter(tm=tm).delete()
                files = request.FILES.getlist('attached_pdfs')
                for file in files:
                    Attached_Pdf_TM.objects.create(
                        file_name=file.name,
                        tm=tm_instance,
                        binary=file.read(),
                        typ=file.content_type,
                    )
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TM.DoesNotExist:
            return Response({'message': 'TM not found'}, status=status.HTTP_404_NOT_FOUND)






@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def createBadging(request, id=None, project_id=None):
    if request.method == 'GET':
        # Specific entry by id
        if id and not project_id:
            badging = get_object_or_404(BadgingProject, id=id)
            serializer = BadgingSerializer(badging)
            return Response(serializer.data)
        
        # Filter by project_id (can be all if project_id is None)
        badging_query = BadgingProject.objects.all()
        if project_id:
            badging_query = badging_query.filter(project__id=project_id)

        # If both id and project_id are provided, filter accordingly
        if id and project_id:
            badging_query = badging_query.filter(id=id, project__id=project_id)

        serializer = BadgingSerializer(badging_query, many=True)
        return Response(serializer.data)
        

    elif request.method == 'POST':
        serializer = BadgingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        update_context = {}
        if id:
            badging = get_object_or_404(BadgingProject, id=id)
        # Decide the update context based on provided IDs
            if project_id:
            # Updating all instances under the same project
                update_context = {'update_type': 'project', 'project_id': project_id}
            else:
            # Updating only the single specified instance
                update_context = {'update_type': 'single'}

            serializer = BadgingSerializer(badging, data=request.data, context=update_context, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Method PUT requires an 'id'."}, status=status.HTTP_400_BAD_REQUEST)


    
    elif request.method == 'DELETE':
        if not id:
            return Response({"error": "Method DELETE requires an 'id'."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            badging = BadgingProject.objects.get(id=id)
        except BadgingProject.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        badging.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
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
            ('wagerate', WageRate, WageRateSerializer),

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
        # Automatically create a BIM entry for the new project
        bim_data = {
            'project_id': project.id,#type:ignore  # Set the project ID to link the BIM entry with the newly created project
            # Set other BIM fields as needed, or leave them with default values
            # For example:
            # 'bimRequirement': False,
            # 'materialDeadline': None,
            # Add other fields as required
        }
        bim_serializer = BimSerializer(data=bim_data)
        if bim_serializer.is_valid():
            bim_serializer.save()
        else:
            # In case BIM data is not valid, you can decide how to handle this.
            # For simplicity, I'm just logging it here, but you could roll back project creation, or handle differently.
            print("BIM data is not valid", bim_serializer.errors)

        # Handle related models
        for key, model, serializer_class in related_data_models:
            related_data_list = data.get(key,[])
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
    parser_classes = (MultiPartParser, FormParser,JSONParser)

    def get(self, request, id=None):
        if id:
            rfi = get_object_or_404(RFI, id=id)
            serializer = RFISerializer(rfi)
            # Fetch associated files
            attached_files = Attached_Pdf_Rfi.objects.filter(rfi=rfi)
            files_serializer = Attache_PDF_RFISerializer(attached_files, many=True)
            return Response(serializer.data)
        else:
            rfi = RFI.objects.all()
            serializer = RFISerializer(rfi, many=True)
            return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = RFISerializer(data=request.data)
        if serializer.is_valid():
            rfi_instance = serializer.save()

            # Your original code seems to assume 'attached_pdf' is part of request.FILES, but it's not clear from your JSON
            # If you're expecting file uploads, ensure the request includes them and the field name matches here.
            files = request.FILES.getlist('attached_pdfs')  # Adjust field name if necessary
            for file in files:
                Attached_Pdf_Rfi.objects.create(
                    file_name=file.name ,
                    rfi=rfi_instance,
                    typ=file.content_type,
                    binary=file.read(),  # Adjust for base64 if needed
                    
                )

            # If you're handling RFI_Log here, ensure RFI_LogSerializer and related model are correctly defined
            # Assuming 'rfi_id' and 'project_id' are correctly targeted fields in your RFI_Log model
            rfi_log_data = {
                'rfi_id': rfi_instance.id,#type:ignore
                'project_id': rfi_instance.project.id,#type: ignore
            }
            rfi_log_serializer = RFI_LogSerializer(data=rfi_log_data)
            if rfi_log_serializer.is_valid():
                rfi_log_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # This prints out the serializer errors if the data is not valid
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id=None):
        rfi = get_object_or_404(RFI, id=id)
        serializer = RFISerializer(rfi, data=request.data)
        if serializer.is_valid():
            rfi_instance = serializer.save()
            # If updating with new files, clear existing ones or add to them based on your logic
            Attached_Pdf_Rfi.objects.filter(rfi=rfi).delete()  # Optional: adjust this logic as needed
            files = request.FILES.getlist('attached_pdfs')  # Adjust field name if necessary
            for file in files:
                Attached_Pdf_Rfi.objects.create(
                    file_name=file.name,
                    rfi=rfi_instance,
                    typ=file.content_type,
                    binary=file.read(),  # Adjust for base64 if needed

                )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        rfi = get_object_or_404(RFI, id=id)
        rfi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
class RFILogViews(APIView):
    parser_classes = (MultiPartParser, FormParser,JSONParser)

    def get(self, request, id=None):
        if id:
            rfi_log = get_object_or_404(RFI_Log, id=id)
            serializer = RFI_LogSerializer(rfi_log)
        else:
            rfi_log = RFI_Log.objects.all()
            serializer = RFI_LogSerializer(rfi_log, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RFI_LogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            rfi_log_instance=serializer.save()
            
            files = request.FILES.getlist('attached_pdfs')  # Adjust field name if necessary
            for file in files:
                Attached_Pdf_Rfi_log.objects.create(
                    file_name=file.name,
                    rfi_log=rfi_log_instance,
                    typ=file.content_type,
                    binary=file.read(),  # Adjust for base64 if needed
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            rfi_log = RFI_Log.objects.get(pk=id)
        except RFI_Log.DoesNotExist:
            raise Http404

        serializer = RFI_LogSerializer(rfi_log, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            # Handle file updates
            if 'attached_pdfs' in request.FILES:
                attached_files = request.FILES.getlist('attached_pdfs')
                for uploaded_file in attached_files:
                    # This example overwrites existing files. Adjust as needed.
                    Attached_Pdf_Rfi_log.objects.update_or_create(
                        rfi_log=rfi_log,
                        defaults={
                            'typ': uploaded_file.content_type,
                            'binary': base64.b64encode(uploaded_file.read()),
                        }
                    )

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        rfi_log = get_object_or_404(RFI_Log, id=id)
        rfi_log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Delay_NoticeViews(APIView):

    def get(self, request,id=None):
        if id:
            delay_notice=Delay_Notice.objects.get(id=id)
            serializer=Delay_NoticeSerializer(delay_notice)
            attached_files = Attached_Pdf_Delay.objects.filter(delay=delay_notice)
            files_serializer = Attache_PDF_DelaySerializer(attached_files, many=True)
            return Response(serializer.data,)
        else:
            delay_notice=Delay_Notice.objects.all()
            serializer=Delay_NoticeSerializer(delay_notice,many=True)
            return Response(serializer.data)
    
    
    

    def post(self, request,*args,**kwargs):
        serialize = Delay_NoticeSerializer(data=request.data)
        if serialize.is_valid():
            delay_notice_instance = serialize.save()
            files = request.FILES.getlist('attached_pdfs')
            for file in files:
                Attached_Pdf_Delay.objects.create(
                    file_name=file.name,
                    delay=delay_notice_instance,
                    binary=file.read(),  # This stores the binary directly; adjust for base64 if needed
                    typ=file.content_type,
                )
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
            delay_instance=serializer.save()
            Attached_Pdf_Delay.objects.filter(delay=dly_ntc).delete()
            files=request.FILES.getlist('attached_pdfs')
            for file in files:
                Attached_Pdf_Delay.objects.create(
                    file_name=file.name ,

                    delay=delay_instance,
                    binary=file.read(),
                    typ=file.content_type,
                )
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
@parser_classes((JSONParser, MultiPartParser))
def pco_view(request, id=None):
    if request.method == 'GET':
        if id:
            try:
                pco = PCO.objects.get(pk=id)
                serializer = PCOSerializer(pco)
            except PCO.DoesNotExist:
                return Response({'message': 'PCO not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            pcos = PCO.objects.all()
            serializer = PCOSerializer(pcos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
            serializer = PCOSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                pco_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        if not id:
            return Response({"message": "ID is required for PUT request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pco = PCO.objects.get(pk=id)
            serializer = PCOSerializer(pco, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                pco_instance=serializer.save()
                Attached_Pdf_Pco.objects.filter(pco=pco).delete()
                files=request.FILES.getlist('attached_pdfs')
                for file in files:
                    Attached_Pdf_Pco.objects.create(
                        file_name=file.name,
                        pco=pco_instance,
                        binary=file.read(),
                        typ=file.content_type,
                    )
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PCO.DoesNotExist:
            return Response({'message': 'PCO not found'}, status=status.HTTP_404_NOT_FOUND)


    elif request.method == 'DELETE':
        if not id:
            return Response({"message": "ID is required for DELETE request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pco = PCO.objects.get(pk=id)
            pco.delete()
            return Response({'message': 'PCO was deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PCO.DoesNotExist:
            return Response({'message': 'PCO not found'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({"message": "HTTP method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    


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
    
class SendDocumentEmailView(APIView):
    def post(self, request, document_id, format=None):
        document_type = request.data.get('document_type')  # 'RFI' or 'Delay'
        custom_message = request.data.get('custom_message', '')
        subject = request.data.get('subject', 'From DMS CMS')
        dms_user_id = request.data.get('dms_user_id')

        
        try:
            # Fetch the document and prepare the message based on type
            if document_type == 'PCO':
                document = PCO.objects.get(id=document_id)  # Replace with your actual model and query
            elif document_type == 'RFI':
                document = RFI.objects.get(id=document_id)
            elif document_type == 'Delay':
                document = Delay_Notice.objects.get(id=document_id)
            else:
                return Response({'error': 'Invalid document type'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch the DMS user and the logo
            dms_user = DMS_Dertory.objects.get(id=dms_user_id)
            attachment = AttachedLogoCompany.objects.filter(company=dms_user.company).first()
            project = document.project
            attn_email = project.attn_email#type: ignore  # Attention email from the project
            if attachment:
                company_logo_binary = attachment.binary
                file_type = attachment.typ 
                logo_image = ContentFile(base64.b64decode(company_logo_binary), name=f"company_logo.{file_type.split('/')[-1]}") #type: ignore
            else:
                logo_image = None
            
            # Create the email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=custom_message,  # Fallback for email clients that don't support HTML
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[attn_email],  # Recipient's email #type: ignore
                cc=request.data.get('cc_emails', '').split(','),  # Optional CC emails
                bcc=request.data.get('bcc_emails', '').split(','),  # Optional BCC emails
            )
            
            def format_phone_number(number):
                """Format the phone number into the desired format (123) 456-7890."""
                if not number:
                    return ""
                number_str = str(number)
                return f"({number_str[:3]}) {number_str[3:6]}-{number_str[6:]}"

# In your SendDocumentEmailView, before constructing the html_content:
            direct_number_formatted = format_phone_number(dms_user.direct_number)
            mobile_number_formatted = format_phone_number(dms_user.mobile_number)

            
            # Prepare the HTML body with the inline image
            html_content = f"""
            <html>
              <body>
              
                <p style="font-family: 'Times New Roman', serif; font-size: 16px">{custom_message}</p>
                <p style="color: black; font-size: 16px; font-family: 'Times New Roman', serif;">Thank You! </p>
                 <p style="color: grey; font-size: 18px; font-family: 'Times New Roman', serif;">
                 {dms_user.first_name} {dms_user.last_name}<br>
                {dms_user.job_title.name if dms_user.job_title else ''}
                </p>
                <img src="cid:company_logo" style="width: 200px; height: auto;">
                <p style="color: grey; font-size: 18px;  font-family: 'Times New Roman', serif;">{dms_user.company.adress if dms_user.company else ''}<br>
                {"Direct: " + direct_number_formatted if dms_user.direct_number else "Mobile: " + mobile_number_formatted if dms_user.mobile_number else ""}
                </p>
                
              </body>
            </html>
            """
            email.attach_alternative(html_content, "text/html")

            # Attach the company logo as an inline image
            if logo_image:
                file_type = logo_image.name.split('.')[-1].lower()
                if file_type == 'jpg':
                    file_type = 'jpeg'
                img = MIMEImage(logo_image.read(), _subtype=file_type)
                img.add_header('Content-ID', '<company_logo>')
                email.attach(img)#type: ignore

            # Attach the PDF file if provided
            pdf_file = request.FILES.get('pdf')
            if pdf_file:
                email.attach(f"{document_type} Attachment.pdf", pdf_file.read(), 'application/pdf')

            # Send the email
            email.send()

            return Response({'message': f'{document_type} email sent successfully!'}, status=status.HTTP_200_OK)

        except DMS_Dertory.DoesNotExist:
            return Response({'error': 'DMS user not found'}, status=status.HTTP_404_NOT_FOUND)

        except (RFI.DoesNotExist, Delay_Notice.DoesNotExist,PCO.DoesNotExist):
            return Response({'error': f'{document_type} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Failed to send email', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ProjectDashboardAPIView(APIView):
    def get(self, request):
        data = {}
        statuses = ['Pre-Construction', 'Construction Phase', 'Close out phase', 'Upcoming/Estimating phase', 'Complete']
        # rfis = RFI_Log.objects.filter(project=project,status='Open').select_related('rfi')
        for status in statuses:
            projects = Project.objects.filter(status=status)
            total_bid_amount = projects.aggregate(Sum('proposal__estimating__bid_amount'))['proposal__estimating__bid_amount__sum'] or 0
            total_projects = projects.count()
            total_open_rfi_count = RFI_Log.objects.filter(project__status=status, status='Open').count()
            total_pco_count = PCO_Log.objects.filter(pco__project__status=status).count()
            total_open_delay_count = Delay_Log.objects.filter(dly_ntc__project__status=status, status='Open').count()
            
            
            projects_data = []
            
            for project in projects:
                project_data = {
                    'project_name': project.proposal.estimating.prjct_name, #type:ignore
                    'project_id':project.id, #type:ignore
                    'job_num':project.job_num,
                    'prjct_mngr': project.prjct_mngr.first_name if project.prjct_mngr else None,
                    'RFI': self.get_rfi_data(project),
                    'PCO': self.get_pco_data(project),
                    'Delay': self.get_delay_data(project),
                }
                projects_data.append(project_data)

            data[status] = {
                'total_projects': total_projects,
                'total_bid_amount': total_bid_amount,
                
                'total_open_rfi_count': total_open_rfi_count,
                'total_pco_count': total_pco_count,
                'total_open_delay_count': total_open_delay_count,
                'projects': projects_data,
            }

        return Response(data)

    def get_rfi_data(self, project):
        rfis = RFI_Log.objects.filter(project=project,status='Open').select_related('rfi')
        total_rfi_num = rfis.count()
        rfi_details = rfis.values('rfi__id','rfi__rfi_num','gc_rfi_num','status','rfi__date','date_close','rfi__rply_by','received_date','rfi__dscrptn','cost_schdl')
        # dms_rfi=rfis.values()

        return {
            'total_rfi_num': total_rfi_num,
            'rfi_detail': list(rfi_details),
        }

    def get_pco_data(self, project):
        pcos = PCO_Log.objects.filter(pco__project=project).select_related('pco')
        total_pco_num = pcos.count()
        pco_details = pcos.values('pco__id','pco__pco_num','pco__totl_rqest','t_m','cor_amont','co_amont','co_num','auther_name','note','pco__dcrsbsn','pco__date')
        return {
            'total_pco_num': total_pco_num,
            'pco_detail': list(pco_details),
        }

    def get_delay_data(self, project):
        delays = Delay_Log.objects.filter(dly_ntc__project=project,status='Open').select_related('dly_ntc__rfi_log__rfi', 'dly_ntc__pco_log__pco')
        total_delay_num = delays.count()

        # Prepare delay details, including RFI number and PCO number from nested relations
        delay_details = []
        for delay in delays:
            detail = {
                'delay_notice_id':delay.dly_ntc.id, #type: ignore
                'delay_num': delay.dly_ntc.delay_num, # type: ignore
                'rfi_num': delay.dly_ntc.rfi_log.rfi.rfi_num if delay.dly_ntc.rfi_log and delay.dly_ntc.rfi_log.rfi else None, # type: ignore
                'pco_num': delay.dly_ntc.pco_log.pco.pco_num if delay.dly_ntc.pco_log and delay.dly_ntc.pco_log.pco else None,# type: ignore
                'status':delay.status,#type: ignore
                'type':delay.typ,
                'dly_rslov':delay.dly_rslov,
                'fnl_impct':delay.fnl_impct,
                'date':delay.date,
                'unResolvedDelayDays':delay.unResolvedDelayDays,
                
                
            }
            delay_details.append(detail)

        return {
            'total_delay_num': total_delay_num,
            'delay_detail': delay_details,
        }