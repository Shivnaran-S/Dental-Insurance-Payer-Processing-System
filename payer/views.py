import openpyxl
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PayerGroups, Payers, PayerDetails
from django.shortcuts import render
import logging
import re

logger = logging.getLogger(__name__)

def upload_page(request):
    return render(request, 'upload.html')

class UploadView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            PayerDetails.objects.all().delete()
            Payers.objects.all().delete()
            PayerGroups.objects.all().delete()

            uploaded_file = request.FILES.get('file')
            if not uploaded_file:
                return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

            file_name = uploaded_file.name
            if not file_name.endswith('.xlsx'):
                return Response({"error": "Unsupported file format. Please upload an XLSX file."}, status=status.HTTP_400_BAD_REQUEST)

            self.process_xlsx(uploaded_file)

            return Response({"message": "File processed successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error processing file: {e}", exc_info=True)  
            return Response({"error": "An error occurred while processing the file."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def process_xlsx(self, file):
        """Process an XLSX file."""
        try:
            workbook = openpyxl.load_workbook(file)
            excluded_sheets = ['Legend', 'Legend (1)', 'OpenDental']

            for sheet_name in workbook.sheetnames:
                if sheet_name in excluded_sheets:
                    logger.info(f"Skipping excluded sheet: {sheet_name}")
                    continue  

                sheet = workbook[sheet_name]
                rows = sheet.iter_rows(values_only=True)

                try:
                    headers = next(rows) 
                except StopIteration:
                    logger.warning(f"Skipping sheet '{sheet_name}' because it is empty.")
                    continue 

               
                payer_name_col = self.find_column_index(headers, ['Payer Name', 'Name', 'Payer', 'Payer Identification Information'])
                payer_id_col = self.find_column_index(headers, ['Payer ID', 'ID'])

                if payer_name_col is None or payer_id_col is None:
                    logger.warning(f"Skipping sheet '{sheet_name}' because required columns are missing.")
                    continue

               
                for row_index, row in enumerate(rows, start=2):  
                    try:
                        payer_name = self.clean_value(row[payer_name_col])
                        payer_id = self.clean_value(row[payer_id_col])

                        if not payer_name or not payer_id:
                            logger.warning(f"Skipping row {row_index} in sheet '{sheet_name}' because of missing data.")
                            continue

                       
                        self.process_payer(payer_name, payer_id)
                    except Exception as e:
                        logger.error(f"Error processing row {row_index} in sheet '{sheet_name}': {e}")

        except Exception as e:
            logger.error(f"Error processing XLSX file: {e}", exc_info=True)
            raise
    def find_column_index(self, headers, possible_names):
        """Find the index of a column based on possible names."""
        for name in possible_names:
            if name in headers:
                return headers.index(name)
        return None

    def clean_value(self, value):
        """Remove `=` and quotes from the value if present."""
        if value and isinstance(value, str):
            # Remove `=` and quotes 
            value = re.sub(r'^="([^"]*)"$', r'\1', value)
            value = value.strip()
        return value

    def process_payer(self, payer_name, payer_id):
        """Process a single payer."""
       
        payer_group_name = self.extract_payer_group_name(payer_name)

    
        payer_group, _ = PayerGroups.objects.get_or_create(name=payer_group_name)

      
        payer = self.find_similar_payer(payer_name, payer_group)

        if not payer:
           
            payer = Payers.objects.create(name=payer_name, payer_group=payer_group)

      
        PayerDetails.objects.get_or_create(
            payer=payer,
            name=payer_name,
            payer_number=payer_id,
            defaults={'tax_id': None}  
        )

    def extract_payer_group_name(self, payer_name):
        """Extract the payer group name from the payer name."""
        return payer_name.split()[0]

    def find_similar_payer(self, payer_name, payer_group):
        """Find a payer with a similar name in the same payer group."""
        similar_payers = Payers.objects.filter(
            name__istartswith=payer_name.split()[0],
            payer_group=payer_group
        )
        return similar_payers.first()