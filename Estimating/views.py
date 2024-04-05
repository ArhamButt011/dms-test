
from rest_framework.decorators import api_view
from django.http import JsonResponse
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,views
from .models import Company, Estimating,Estimating_detail, Proposal, Qualification,Location,UrlsTable,ProposalService,Addendum,DMS_Dertory,Specification,Spec_detail,Role,Dprtmnt,GC_detail,AttachedLogoCompany
from .serializers import EstimatingSerializer, ProposalSerializer, AddendumSerializer, QualificationSerializer, SpecificationDetailSerializer,SpecificationSerializer,LocationSerializer,EstimatingDetailSerializer,ProposalServiceSerializer,CompanySerializer,UrlsSerializers,DMS_DertorySezializers,Job_titleSerializers,DprtmentSerializers,GC_infoSerializers,Attache__LogoSerializer
from accounts.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser

from django.shortcuts import get_object_or_404

from .forms import EstimatingDetailAdminForm

from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
import base64
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,date
from django.db.models import Sum,Q





class DepartmentViews(APIView):
    def get(self,request):
        department=Dprtmnt.objects.all()
        serializer=DprtmentSerializers(department, many=True)
        return Response(serializer.data)


    def post(self,request):
        serializer=DprtmentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class Job_titleViews(APIView):
    def get(self,request):
        jobtile=Role.objects.all()
        serializer=Job_titleSerializers(jobtile, many=True)
        return Response(serializer.data)


    def post(self,request):
        serializer=Job_titleSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class DMS_DertoryView(APIView):
    
    def get(self, request, id=None):
        if id:
            try:
                dms_dertory = DMS_Dertory.objects.get(id=id)
                serializer = DMS_DertorySezializers(dms_dertory)
            except DMS_Dertory.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            dms_dertory = DMS_Dertory.objects.all()
            serializer = DMS_DertorySezializers(dms_dertory, many=True)

        return Response(serializer.data)
    def post(self,request):
        serializer=DMS_DertorySezializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, id, format=None):
        try:
            dms_dertory = DMS_Dertory.objects.get(id=id)
        except DMS_Dertory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DMS_DertorySezializers(dms_dertory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            dms_dertory_instance = DMS_Dertory.objects.get(id=id)  # Change the variable name
        except DMS_Dertory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        dms_dertory_instance.delete()  # Use the new variable name
        return Response(status=status.HTTP_204_NO_CONTENT)



# class SendEmailView(APIView):

#     def post(self, request, estimating_id, format=None):
#         logger = logging.getLogger(__name__)

#         try:
#             estimating = Estimating.objects.get(id=estimating_id)
#             if estimating.company is None:
#                 return Response({'error': 'Company not found'}, status=status.HTTP_400_BAD_REQUEST)

#             email_from = 'mubeenjutt9757@gmail.com'  # Default sender email

#             # Find the active proposal related to this estimating
#             active_proposal = Proposal.objects.filter(estimating=estimating, is_active=True).first()
#             if not active_proposal:
#                 return Response({'error': 'Active proposal not found'}, status=status.HTTP_400_BAD_REQUEST)

#             # Use the plane_date from the active proposal
#             plane_date = active_proposal.plane_date.strftime('%m-%d-%Y') if active_proposal.plane_date else "N/A"
#             architect_name=active_proposal.architect_name if active_proposal.architect_name else "N/A"
#             architect_firm=active_proposal.architect_firm if active_proposal.architect_firm else "N/A"


#             # Email message
#             subject = 'Proposal'
#             message = f"""
#             Hello,
#             <br>

#             Thank you for allowing <strong>{estimating.company.Cmpny_Name}</strong> the opportunity to bid on the <strong>{estimating.prjct_name}</strong>.

#             The plans used to formulate the bid proposal are dated <strong>{plane_date}</strong>, drafted by <strong>{architect_firm}</strong>, and approved by <strong>{architect_name}</strong>.
#             <br>
#             Let us know if there are any questions. <br><br>

#             Thank you
#             """

#             # Fetch all GC emails related to this estimating
#             gc_emails = [gc.gc_email for gc in GC_detail.objects.filter(estimating=estimating) if gc.gc_email]

#             if not gc_emails:
#                 return Response({'error': 'No valid GC emails found'}, status=status.HTTP_400_BAD_REQUEST)

#             email = EmailMessage(
#                 subject,
#                 message,
#                 email_from,
#                 gc_emails,
#             )
#             email.content_subtype = 'html'

#             # Attach the PDF if it's in the request
#             pdf_file = request.FILES.get('pdf')
#             if isinstance(pdf_file, InMemoryUploadedFile):
#                 email.attach(pdf_file.name, pdf_file.read(), 'application/pdf')

#             email.send()

#             return Response({'message': 'Email sent successfully!'})

#         except Estimating.DoesNotExist:
#             logger.error(f'Estimating ID {estimating_id} not found')
#             return Response({'error': 'Estimating not found'}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             logger.error(str(e))
#             logger.error(f'Request Data: {request.data}')  # Log the entire request data
#             return Response({'error': 'Failed to send email', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendEmailView(APIView):

    def post(self, request, estimating_id, gc_id, format=None):
        logger = logging.getLogger(__name__)

        try:
            estimating = Estimating.objects.get(id=estimating_id)
            proposal_id = request.POST.get('proposalId')
            if estimating.company is None:
                return Response({'error': 'Company not found'}, status=status.HTTP_400_BAD_REQUEST)


            if not proposal_id:
                return Response({'error': 'Proposal ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            

            try:
                proposal_id = int(proposal_id)
                active_proposal = Proposal.objects.get(id=proposal_id)
            except ValueError:
                return Response({'error': 'Invalid proposal ID'}, status=status.HTTP_400_BAD_REQUEST)
            except Proposal.DoesNotExist:
                return Response({'error': 'Active proposal not found'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            email_from = 'mubeenjutt9757@gmail.com'  # Default sender 
            
            
            # Use the plane_date from the active proposal
            plane_date = active_proposal.plane_date.strftime('%m-%d-%Y') if active_proposal.plane_date else "N/A"
            architect_name = active_proposal.architect_name if active_proposal.architect_name else "N/A"
            architect_firm = active_proposal.architect_firm if active_proposal.architect_firm else "N/A"

            # Email message
            subject = estimating.prjct_name
            message = f"""
            Hello,
            <br>
            Thank you for allowing <strong>{estimating.company.Cmpny_Name}</strong> the opportunity to bid on the <strong>{estimating.prjct_name}</strong>.
            The plans used to formulate the bid proposal are dated <strong>{plane_date}</strong>, drafted by <strong>{architect_firm}</strong>, and approved by <strong>{architect_name}</strong>.
            <br>
            Let us know if there are any questions. <br><br>
            Thank you
            """

            # Fetch the specific GC's email using gc_id
            try:
                gc_detail = GC_detail.objects.get(estimating=estimating, id=gc_id)
                gc_email = gc_detail.gc_email
                if not gc_email:
                    return Response({'error': 'GC email not found'}, status=status.HTTP_400_BAD_REQUEST)
            except GC_detail.DoesNotExist:
                return Response({'error': 'GC not found'}, status=status.HTTP_404_NOT_FOUND)

            email = EmailMessage(
                subject,#type: ignore
                message,
                email_from,
                [gc_email],  # Send email to the specific GC
            )
            email.content_subtype = 'html'

            # Attach the PDF if it's in the request
            pdf_file = request.FILES.get('pdf')
            if pdf_file:
                email.attach(pdf_file.name, pdf_file.read(), 'application/pdf')

            email.send()

            return Response({'message': 'Email sent successfully!'})

        except Estimating.DoesNotExist:
            logger.error(f'Estimating ID {estimating_id} not found')
            return Response({'error': 'Estimating not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(str(e))
            logger.error(f'Request Data: {request.data}')  # Log the entire request data
            return Response({'error': 'Failed to send email', 'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class UrlsListViews(APIView):
    
    def get(self, request, id=None):
        if id:
            try:
                url = UrlsTable.objects.get(id=id)
            except UrlsTable.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = UrlsSerializers(url)
        else:
            urls = UrlsTable.objects.all()
            serializer = UrlsSerializers(urls, many=True)

        return Response(serializer.data)
    
    def post(self,request):
        serializer=UrlsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, id, format=None):
        try:
            url = UrlsTable.objects.get(id=id)
        except UrlsTable.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UrlsSerializers(url, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            url = UrlsTable.objects.get(id=id)  # Change the variable name
        except UrlsTable.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        url.delete()  # Use the new variable name
        return Response(status=status.HTTP_204_NO_CONTENT)






class CompanyWonEstimates(APIView):

    def get(self, request):
        year = int(request.query_params.get('year', datetime.now().year))

        companies = Company.objects.filter(is_active=True)

        month_names = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]

        data = []

        for month_num, month_name in enumerate(month_names, start=1):
            month_data = {}

            for company in companies:
                won_estimates = Estimating.objects.filter(
                    company=company,
                    status='Won',
                    due_date__year=year,
                    due_date__month=month_num 
                )

                total_won_estimates = won_estimates.count()

                total_bid_amount = won_estimates.aggregate(sum=Sum('bid_amount'))['sum'] or 0

                month_data[company.Cmpny_Name] = {
                    "total_won": total_won_estimates,
                    "total_won_bid_amount": total_bid_amount
                }

            data.append({month_name: month_data})

        return Response(data)





class EstimatorSummaryView(views.APIView):

    def get(self, request, format=None):
        response_data = []
        total_data = {
            'Working': {'total': 0, 'bid_amount': 0},
            'Pending': {'total': 0, 'bid_amount': 0},
            'Won': {'total': 0, 'bid_amount': 0},
            'Lost': {'total': 0, 'bid_amount': 0},
            'Grand Total': {'total': 0, 'bid_amount': 0}
        }

        year = int(request.query_params.get('year', datetime.now().year))

        estimators = DMS_Dertory.objects.filter(
            Q(job_title__name='Estimator') | 
            Q(job_title__name='Estimating Manager') |
            Q(job_title__name='Field Management') |
            Q(job_title__name='Owner')
        )
        
        for estimator in estimators:
            estimates = Estimating.objects.filter(
                estimator=estimator,
                start_date__year=year  
            )
            # Serialize the estimator to get the full_name
            serialized_estimator = DMS_DertorySezializers(estimator).data
            estimator_full_name = serialized_estimator.get('full_name')# type: ignore
            
            if estimates.count() == 0:
                continue
            
            estimator_data = calculate_summary(estimates)
            estimator_data['estimator'] = estimator_full_name 
            
            response_data.append(estimator_data)

            for status in ['Working', 'Pending', 'Won', 'Lost']:
                total_data[status]['total'] += estimator_data['summary'][status]['total']
                total_data[status]['bid_amount'] += estimator_data['summary'][status]['bid_amount']
                total_data['Grand Total']['total'] += estimator_data['summary'][status]['total']
                total_data['Grand Total']['bid_amount'] += estimator_data['summary'][status]['bid_amount']

        unassigned_estimations = Estimating.objects.filter(
            estimator__isnull=True,
            status='Working',
            start_date__year=year  
        )

        unassigned_data = calculate_summary(unassigned_estimations, only_working=True)
        unassigned_data['estimator'] = 'Unassigned'

        total_data['Working']['total'] += unassigned_data['summary']['Working']['total']
        total_data['Working']['bid_amount'] += unassigned_data['summary']['Working']['bid_amount']
        total_data['Grand Total']['total'] += unassigned_data['summary']['Working']['total']
        total_data['Grand Total']['bid_amount'] += unassigned_data['summary']['Working']['bid_amount']

        response_data.append(unassigned_data)


        grand_totals = {
            'summary': total_data,  
            'ytd_total': total_data['Grand Total']['total'], 
            'ytd_total_bid_amount': total_data['Grand Total']['bid_amount'],
            'estimator': 'Grand Total'
        }
        response_data.append(grand_totals)


        return Response(response_data, status=200)

def calculate_summary(estimates, only_working=False):
    grand_total = estimates.count()
    grand_total_bid_amount = estimates.aggregate(Sum('bid_amount'))['bid_amount__sum'] or 0
    statuses = ['Working'] if only_working else ['Working', 'Pending', 'Won', 'Lost']

    summary = {}
    for status in statuses:
        total = estimates.filter(status=status).count()
        bid_amount = estimates.filter(status=status).aggregate(bid_amount=Sum('bid_amount'))['bid_amount'] or 0
        percentage = (total / grand_total * 100) if grand_total > 0 else 0

        summary[status] = {
            'total': total,
            'percentage': percentage,
            'bid_amount': bid_amount
        }

    return {
        'summary': summary,
        'ytd_total': grand_total,
        'ytd_total_bid_amount': grand_total_bid_amount
    }






class CompanyListView(APIView):
    parser_classes = (MultiPartParser, FormParser,JSONParser)

    def get(self, request, id=None):
        if id:
            company=get_object_or_404(Company,id=id)
            serializer=CompanySerializer(company)
        else:
            Cmpany = Company.objects.all()
            serializer = CompanySerializer(Cmpany, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = CompanySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        try:
            Cmpany = Company.objects.get(id=id)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(Cmpany, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            
            #handle File Update
            if 'attached_pdfs' in request.FILES:
                attached_files = request.FILES.getlist('attached_pdfs')
                for uploaded_file in attached_files:
                    # This example overwrites existing files. Adjust as needed.
                    AttachedLogoCompany.objects.update_or_create(
                        company=Cmpany,
                        defaults={
                            'typ': uploaded_file.content_type,
                            'binary': base64.b64encode(uploaded_file.read()), #type: ignore
                        }
                    )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            Cmpany = Company.objects.get(id=id)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        Cmpany.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






class EstimatingListView(APIView):

    def get(self, request, id=None, format=None):
        if id:
            try:
                estimating = Estimating.objects.get(id=id)
                serializer = EstimatingSerializer(estimating)
                return Response(serializer.data)
            except Estimating.DoesNotExist:
                return Response({'error': 'Estimating not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            estimatings = Estimating.objects.all() 
            serializer = EstimatingSerializer(estimatings, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        estimating_serializer = EstimatingSerializer(data=request.data)
        if estimating_serializer.is_valid():
            estimating = estimating_serializer.save()  # Save the Estimating instance first

            # Now handle the GC_detail data if present
            gc_details_data = request.data.get('gc_details')  # 'gc_details' should be the key in your request data
            if gc_details_data:
                # Ensure that we have a list of GC_details
                if not isinstance(gc_details_data, list):
                    gc_details_data = [gc_details_data]

                for gc_detail_data in gc_details_data:
                    # Set the estimating instance to the current estimating id
                    gc_detail_data['estimating'] = estimating.id # type: ignore
                    gc_detail_serializer = GC_infoSerializers(data=gc_detail_data)
                    if gc_detail_serializer.is_valid():
                        gc_detail_serializer.save()  # Save the GC_detail instance
                    else:
                        # If GC_detail is not valid, delete the estimating instance and return an error
                        estimating.delete() # type: ignore
                        return Response(gc_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(estimating_serializer.data, status=status.HTTP_201_CREATED)
        return Response(estimating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    def delete(self, request, id, format=None):
        try:
            estimating = Estimating.objects.get(id=id)
        except Estimating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        estimating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def put(self, request, id, format=None):
        try:
            estimating = Estimating.objects.get(id=id)
        except Estimating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        estimating_serializer = EstimatingSerializer(estimating, data=request.data)
        if estimating_serializer.is_valid():
            estimating_serializer.save()

            # Handle gc_details data
            gc_details_data = request.data.get('gc_details')
            if gc_details_data:
                if not isinstance(gc_details_data, list):
                    gc_details_data = [gc_details_data]

                existing_gc_detail_ids = [gc_detail.id for gc_detail in estimating.gc_details.all()] # type: ignore
                updated_gc_detail_ids = []

                for gc_detail_data in gc_details_data:
                    gc_detail_id = gc_detail_data.get('id')
                    if gc_detail_id:
                        # Update existing GC_detail
                        try:
                            gc_detail = GC_detail.objects.get(id=gc_detail_id, estimating=estimating)
                            gc_detail_serializer = GC_infoSerializers(gc_detail, data=gc_detail_data)
                            updated_gc_detail_ids.append(gc_detail_id)
                        except GC_detail.DoesNotExist:
                            return Response({'error': 'GC_detail not found'}, status=status.HTTP_404_NOT_FOUND)
                    else:
                        # Create new GC_detail
                        gc_detail_data['estimating'] = estimating.id # type: ignore
                        gc_detail_serializer = GC_infoSerializers(data=gc_detail_data)

                    if gc_detail_serializer.is_valid():
                        gc_detail_serializer.save()
                    else:
                        return Response(gc_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Optional: Delete GC_details that were not included in the request
                for gc_detail_id in existing_gc_detail_ids:
                    if gc_detail_id not in updated_gc_detail_ids:
                        GC_detail.objects.get(id=gc_detail_id).delete()

            return Response(estimating_serializer.data)
        return Response(estimating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class Estimating_detailView(APIView):


    def get(self,request):
        top_level_details = Estimating_detail.objects.filter(prnt_id__isnull=True)
        serializer = EstimatingDetailSerializer(top_level_details, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        form = EstimatingDetailAdminForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract the file binary data and file details
            file_field = form.cleaned_data.pop('file_field')
            file_binary_data = file_field.read()
            uploaded_file_name, uploaded_file_extension = os.path.splitext(file_field.name)
            
            # Update cleaned_data with file details
            cleaned_data = form.cleaned_data
            cleaned_data['file_type'] = uploaded_file_extension.lstrip('.')
            cleaned_data['file_name'] = uploaded_file_name
            
            # Ensure ForeignKeys are set to IDs
            cleaned_data['Estimating'] = cleaned_data['Estimating'].id if cleaned_data.get('Estimating') else None
            cleaned_data['prnt'] = cleaned_data['prnt'].id if cleaned_data.get('prnt') else None

            # Initialize the serializer with cleaned_data
            serializer = EstimatingDetailSerializer(data=cleaned_data)
            if serializer.is_valid():
                instance = serializer.save()
                instance.file_binary_data = file_binary_data # type: ignore
                instance.save() # type: ignore
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        try:
            estimating=Estimating_detail.objects.get(id=id)
        except Estimating_detail.DoesNotExist:
            return Response( status=status.HTTP_404_NOT_FOUND)
        estimating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class QualificationView(APIView):


    def get(self, request, format=None):
        qualification = Qualification.objects.all()
        serializer = QualificationSerializer(qualification, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QualificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        try:
            qualification = Qualification.objects.get(id=id)
        except Qualification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QualificationSerializer(qualification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            qualification = Qualification.objects.get(id=id)
        except Qualification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        qualification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)











class LocationViews(APIView):
    def get(self,request):
        location=Location.objects.all()
        serializer=LocationSerializer(location,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        try:
            location=Location.objects.get(id=id)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=LocationSerializer(location,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        try:
            location = Location.objects.get(id=id)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def create_proposal(request, proposal_id=None):
    if request.method == 'POST':
        data = request.data

        # Validate 'estimating_id' presence
        estimating_id = data.get('estimating_id')
        if not estimating_id:
            return Response({"error": "estimating_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            estimating_instance = Estimating.objects.get(id=estimating_id)
        except Estimating.DoesNotExist:
            return Response({"error": "Estimating instance not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Deactivate existing proposals for this estimating
        Proposal.objects.filter(estimating=estimating_instance).update(is_active=False)

        # Create new proposal
        proposal_serializer = ProposalSerializer(data=data)
        if proposal_serializer.is_valid():
          proposal_instance = proposal_serializer.save()
        else:
            return Response(proposal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handling nested data - services
        for service_data in data.get('services', []):
            service_data['proposal'] = proposal_instance.id # type: ignore
            proposal_service_serializer = ProposalServiceSerializer(data=service_data)
            if proposal_service_serializer.is_valid():
                proposal_service_serializer.save()
            else:
                return Response(proposal_service_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handling nested data - addendums
        for addendum_data in data.get('Addendums', []):
            addendum_data['proposal'] = proposal_instance.id # type: ignore
            proposal_addendum_serializer = AddendumSerializer(data=addendum_data)
            if proposal_addendum_serializer.is_valid():
                proposal_addendum_serializer.save()
            else:
                return Response(proposal_addendum_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
        total_budget = 0



        # Handling nested data - specific details
        for specific_data in data.get('spcifc', []):
            specific_data['proposal'] = proposal_instance.id # type: ignore
            specification_serializer = SpecificationSerializer(data=specific_data)
            if specification_serializer.is_valid():
                specification = specification_serializer.save()
                total_budget += float(specific_data['budget'])
                for detail_data in specific_data.get('sefic', []):
                    detail_data['sefic'] = specification.id # type: ignore
                    spec_detail_serializer = SpecificationDetailSerializer(data=detail_data)
                    if spec_detail_serializer.is_valid():
                        spec_detail_serializer.save()
                    else:
                        return Response(spec_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(specification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            if estimating_instance.bid_amount is None:
                estimating_instance.bid_amount = 0

                estimating_instance.bid_amount = total_budget # type: ignore
            else:
                estimating_instance.bid_amount = 0
                estimating_instance.bid_amount += total_budget # type: ignore
            estimating_instance.save()
        # qualifications_data = data.get('qualification', [])
        for qualification_data in data.get('qualification', []):
            qualification_data['proposal'] = proposal_instance.id # type: ignore
            qualification_serializer = QualificationSerializer(data=qualification_data)
            if qualification_serializer.is_valid():
                qualification_serializer.save()
            else:
                return Response(qualification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

            
        

        return Response({"message": "Proposal created successfully"}, status=status.HTTP_201_CREATED)



    elif request.method == 'GET':
        if proposal_id is not None:
            try:
                proposal = Proposal.objects.get(id=proposal_id)
                serializer = ProposalSerializer(proposal)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Proposal.DoesNotExist:
                return Response({"error": "Proposal not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            proposals = Proposal.objects.all()
            serializer = ProposalSerializer(proposals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    

    elif request.method == 'PUT':
        if not proposal_id:
            return Response({"error": "Proposal ID is required for updating"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            proposal = Proposal.objects.get(id=proposal_id)
        except Proposal.DoesNotExist:
            return Response({"error": "Proposal not found"}, status=status.HTTP_404_NOT_FOUND)

        proposal_serializer = ProposalSerializer(proposal, data=request.data, context={'request': request}, partial=True)
        if proposal_serializer.is_valid():
            proposal_serializer.save()

            # Update or create nested services, addendums, specifics, and qualification
            nested_entities = {
                'services': (ProposalServiceSerializer, ProposalService),
                'Addendums': (AddendumSerializer, Addendum),
                'spcifc': (SpecificationSerializer, Specification, Spec_detail),  # Added Spec_detail here
                'qualification': (QualificationSerializer, Qualification)
            }

            for entity_key, value in nested_entities.items():
                SerializerClass, ModelClass = value[:2]
                entity_data_list = request.data.get(entity_key, [])
                for entity_data in entity_data_list:
                    entity_id = entity_data.get('id')
                    context = {'request': request}
                    if entity_id:
                        # Update existing entity
                        try:
                            entity_instance = ModelClass.objects.get(id=entity_id, proposal=proposal)
                            entity_serializer = SerializerClass(entity_instance, data=entity_data, context=context, partial=True)
                        except ModelClass.DoesNotExist:
                            return Response({"error": f"{entity_key[:-1]} not found"}, status=status.HTTP_404_NOT_FOUND)
                    else:
                        # Create new entity
                        entity_data['proposal'] = proposal.id  # type: ignore
                        entity_serializer = SerializerClass(data=entity_data, context=context)

                    if entity_serializer.is_valid():
                        saved_instance = entity_serializer.save()

                        # Additional logic for Specification details
                        if entity_key == 'spcifc' and 'sefic' in entity_data:
                            SpecDetailClass = value[2]  # Spec_detail class
                            for detail_data in entity_data['sefic']:
                                detail_id = detail_data.get('id')
                                if detail_id:
                                    # Update existing Spec_detail instance
                                    try:
                                        detail_instance = SpecDetailClass.objects.get(id=detail_id, sefic=saved_instance)
                                        detail_serializer = SpecificationDetailSerializer(detail_instance, data=detail_data, partial=True)
                                    except SpecDetailClass.DoesNotExist:
                                        continue
                                else:
                                    # Create new Spec_detail instance
                                    detail_data['sefic'] = saved_instance.id
                                    detail_serializer = SpecificationDetailSerializer(data=detail_data)

                                if detail_serializer.is_valid():
                                    detail_serializer.save()
                                else:
                                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        return Response(entity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Proposal updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(proposal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
    elif request.method == 'DELETE':
        # Add DELETE request handling logic here
        if proposal_id is None:
            return Response({"error": "Proposal ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            proposal = Proposal.objects.get(id=proposal_id)
        except Proposal.DoesNotExist:
            return Response({"error": "Proposal not found"}, status=status.HTTP_404_NOT_FOUND)

        proposal.delete()
        return Response({"message": "Proposal deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    




class AddendumView(APIView):
    def get(self, request, format=None):
        Addendums = Addendum.objects.all()
        serializer = AddendumSerializer(Addendums, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AddendumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        try:
            Addendums = Addendum.objects.get(id=id)
        except Addendum.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AddendumSerializer(Addendums, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            Addendums = Addendum.objects.get(id=id)
        except Addendum.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        Addendums.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    








# THIS IS Specification VIEW WITH ALL CRUD OPRATION
class SpecificationViews(APIView):

    def get(self, request, format=None):
        specification = Specification.objects.all()
        serializer = SpecificationSerializer(specification, many=True)
        return Response(serializer.data)






class SpecificationDetailViews(APIView):

    def get(self, request, format=None):
        specification = Spec_detail.objects.all()
        serializer = SpecificationDetailSerializer(specification, many=True)
        return Response(serializer.data)

