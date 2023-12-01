from drawranflow.models import UploadedFile, Identifiers, IdentifiersStats, Stats,Message
import pyshark
import os
from django.conf import settings
import logging


class FileHandlers:
    MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', None)

    @classmethod
    def upload_pcap_file(cls, file):
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)

        # Try to get an existing UploadedFile record with the same filename
        try:
            upload_table = UploadedFile.objects.get(filename=file.name)

            # If it exists, delete associated records and the UploadedFile record
            Identifiers.objects.filter(uploadedFiles__id=upload_table.id).delete()
            Message.objects.filter(
                identifiers__id__in=Identifiers.objects.filter(uploadedFiles__id=upload_table.id).values('id')).delete()
            upload_table.delete()

            # Remove the file from the file system
            if os.path.exists(file_path):
                cls.delete_files(file_path)
        except UploadedFile.DoesNotExist:
            pass

        # Save the new file
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Create or update the UploadedFile record
        uploaded_file_record, created = UploadedFile.objects.get_or_create(filename=file.name, processed=False)
        uploaded_file_record.save()

        if uploaded_file_record:
            messages = {
                'message_type': 'success',
                'message_text': 'File uploaded successfully',
            }
        else:
            messages = {
                'message_type': 'error',
                'message_text': 'File upload failed',
            }

        return messages

    @classmethod
    def delete_files(cls, file_path):
        # Remove the main file
        os.remove(file_path)
        file_prefix = os.path.basename(file_path).split('.')[0]

        # Find and delete associated files with the same prefix
        for file_name in os.listdir(settings.MEDIA_ROOT):
            if file_name.startswith(file_prefix):
                file_to_delete = os.path.join(settings.MEDIA_ROOT, file_name)
                logging.debug(f"Deleting file: {file_to_delete}")
                os.remove(file_to_delete)

    @classmethod
    def construct_pcap_filter(cls, identifier_data):
        filter_conditions = []

        if identifier_data.C_RNTI is not None and identifier_data.GNB_DU_UE_F1AP_ID is not None:
            filter_conditions.append(f"(f1ap.C_RNTI=={identifier_data.C_RNTI} && "
                                     f"f1ap.GNB_DU_UE_F1AP_ID=={identifier_data.GNB_DU_UE_F1AP_ID})")

        if identifier_data.GNB_DU_UE_F1AP_ID is not None and identifier_data.GNB_CU_UE_F1AP_ID is not None:
            filter_conditions.append(f"(f1ap.GNB_CU_UE_F1AP_ID=={identifier_data.GNB_CU_UE_F1AP_ID}) or "
                                     f"(f1ap.GNB_CU_UE_F1AP_ID=={identifier_data.GNB_CU_UE_F1AP_ID} && "
                                     f"f1ap.GNB_DU_UE_F1AP_ID=={identifier_data.GNB_DU_UE_F1AP_ID})")

        if identifier_data.GNB_DU_UE_F1AP_ID is not None and identifier_data.GNB_CU_UE_F1AP_ID is None:
            filter_conditions.append(f"(f1ap.GNB_CU_UE_F1AP_ID=={identifier_data.GNB_CU_UE_F1AP_ID})")

        if identifier_data.GNB_CU_CP_UE_E1AP_ID is not None and identifier_data.GNB_CU_UP_UE_E1AP_ID is not None:
            filter_conditions.append(f"(e1ap.GNB_CU_CP_UE_E1AP_ID=={identifier_data.GNB_CU_CP_UE_E1AP_ID}) or "
                                     f"(e1ap.GNB_CU_CP_UE_E1AP_ID=={identifier_data.GNB_CU_CP_UE_E1AP_ID} && "
                                     f"e1ap.GNB_CU_UP_UE_E1AP_ID=={identifier_data.GNB_CU_UP_UE_E1AP_ID})")

        if identifier_data.GNB_CU_CP_UE_E1AP_ID is not None and identifier_data.GNB_CU_UP_UE_E1AP_ID is None:
            filter_conditions.append(f"(e1ap.GNB_CU_CP_UE_E1AP_ID=={identifier_data.GNB_CU_CP_UE_E1AP_ID})")

        if identifier_data.RAN_UE_NGAP_ID is not None and identifier_data.AMF_UE_NGAP_ID is not None:
            filter_conditions.append(f"(ngap.RAN_UE_NGAP_ID=={identifier_data.RAN_UE_NGAP_ID}) or "
                                     f"(ngap.RAN_UE_NGAP_ID=={identifier_data.RAN_UE_NGAP_ID} && "
                                     f"ngap.AMF_UE_NGAP_ID=={identifier_data.AMF_UE_NGAP_ID})")

        if identifier_data.RAN_UE_NGAP_ID is not None and identifier_data.AMF_UE_NGAP_ID is None:
            filter_conditions.append(f"ngap.RAN_UE_NGAP_ID =={identifier_data.RAN_UE_NGAP_ID}")

        if identifier_data.XNAP_SRC_RAN_ID is not None:
            filter_conditions.append(f"(xnap.NG_RANnodeUEXnAPID=={identifier_data.XNAP_SRC_RAN_ID})")

        if identifier_data.XNAP_TRGT_RAN_ID is not None:
            filter_conditions.append(f"(xnap.NG_RANnodeUEXnAPID=={identifier_data.XNAP_TRGT_RAN_ID})")

        filter_string = " or ".join(filter_conditions)
        logging.debug(f'Filter string - {filter_string}')
        # Log or use the generated filter_string as needed

        return filter_string

    @classmethod
    def fetch_identifier_data(cls, row_id):
        logging.debug(f'identifier_data in fetch_identifier_data: {row_id}')
        identifier_data = Identifiers.objects.get(id=row_id)

        return identifier_data

    @classmethod
    def filter_pcap(cls, input_file, filter_string, output_file):
        capture = pyshark.FileCapture(input_file, display_filter=f"{filter_string}", output_file=f'{output_file}')
        capture.set_debug()
        filtered_packets = [packet for packet in capture]
        logging.debug(f'filtered_packets,{filtered_packets} - output: {output_file}, filterString:{filter_string}')

        return output_file
