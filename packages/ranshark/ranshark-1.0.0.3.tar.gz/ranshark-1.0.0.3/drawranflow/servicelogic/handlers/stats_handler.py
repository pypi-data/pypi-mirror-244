from drawranflow.models import Identifiers,IdentifiersStats,Stats,Message,UploadedFile
import logging
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum, Q


class computeStats:
    def __init__(self):
        pass

    @classmethod
    def packet_to_json(cls,packet):
        # Extract IP layer if it exists
        new_dict = {}
        for key in packet:
            # split the key by the first dot and get the top-level key and the second-level key suffix
            if key != "" and "per" not in key:
                if "." in key:
                    top_level_key, suffix = key.split(".", 1)
                else:
                    top_level_key = key
                    suffix = ""

                # create a new dictionary with the top-level key if it doesn't exist
                if top_level_key not in new_dict:
                    new_dict[top_level_key] = {}

                    # add the second-level key suffix and its value to the new dictionary
                new_dict[top_level_key][suffix] = packet[key]
                # convert the output dictionary to a pretty-printed JSON string
        return new_dict

    @classmethod
    def packetLayers(cls,packet):
        f1ap = packet.f1ap._all_fields if 'F1AP' in packet else {}
        e1ap = packet.e1ap._all_fields if 'E1AP' in packet else {}
        ngap = packet.ngap._all_fields if 'NGAP' in packet else {}
        xnap = packet.xnap._all_fields if 'XNAP' in packet else {}
        ipadd = packet.ip._all_fields if 'IP' in packet else {}
        filtered_ipdata = {key: value for key, value in ipadd.items() if key in ["ip.src", "ip.dst"]}
        del packet
        return {**filtered_ipdata, **f1ap, **ngap, **e1ap, **xnap}

    @classmethod
    def rrc_related_message_stats(cls, file_id, ip, identifier):
        time_window = timezone.timedelta(seconds=1)
        try:
            rrc_setup_messages = Message.objects.filter(
                identifiers_id=identifier.id,
                Message='RRC Setup'
            )
            if rrc_setup_messages:
                for rrc_setup in rrc_setup_messages:
                    related_messages = Message.objects.filter(
                        identifiers_id=identifier.id,
                        FrameTime__gte=rrc_setup.FrameTime,
                        FrameTime__lte=rrc_setup.FrameTime + time_window
                    )
                    has_service_request = related_messages.filter(Message='Service request',
                                                                  Protocol__icontains='f1ap').exists()
                    has_registration_request = related_messages.filter(Message='Registration request',
                                                                       Protocol__icontains='f1ap').exists()
                    has_tracking_request = related_messages.filter(Message='Tracking area update request',
                                                                   Protocol__icontains='f1ap').exists()

                    rrc, created = IdentifiersStats.objects.get_or_create(
                        category='RRC',
                        identifier_id=identifier.id,
                        uploadedFiles_id=file_id,
                        cucp_f1c_ip=ip
                    )

                    if created or (rrc is not None and rrc.attempts == 0):
                        rrc.attempts += 1
                        if has_service_request or has_registration_request or has_tracking_request:
                            rrc.success += 1
                        if related_messages.filter(Message='Registration reject', Protocol__icontains='f1ap').exists():
                            rrc.fails += 1
                        if not has_service_request and not has_registration_request and not has_tracking_request:
                            rrc.timeouts += 1
                        rrc.save()
        except Exception as e:
            logging.error(f"Error in processing rrc stats, {e}")

    @classmethod
    def initial_related_messages_stats(cls, file_id, ip, identifier):
        has_initial_context_request = Message.objects.filter(Message='InitialContextSetupRequest',
                                                             identifiers_id=identifier.id).exists()
        has_initial_context_response = Message.objects.filter(Message='InitialContextSetupResponse',
                                                              identifiers_id=identifier.id).exists()
        has_initial_context_failure = Message.objects.filter(Message='InitialContextSetupFailure',
                                                             identifiers_id=identifier.id).exists()

        ctxt, ctxt_created = IdentifiersStats.objects.get_or_create(
            category='InitialCtxt',
            identifier_id=identifier.id,
            uploadedFiles_id=file_id,
            cucp_f1c_ip=ip
        )
        if ctxt_created or (ctxt is not None and ctxt.attempts == 0):
            if has_initial_context_request:
                ctxt.attempts += 1
            if has_initial_context_response:
                ctxt.success += 1
            if has_initial_context_failure:
                ctxt.fails += 1
            if has_initial_context_request and not has_initial_context_failure and not has_initial_context_response:
                ctxt.timeouts += 1
            ctxt.save()

    @classmethod
    def bearerctxt_related_messages_stats(cls, file_id, ip, identifier):
        has_initial_context_request = Message.objects.filter(Message='BearerContextSetupRequest',
                                                             identifiers_id=identifier.id).exists()
        has_initial_context_response = Message.objects.filter(Message='BearerContextSetupResponse',
                                                              identifiers_id=identifier.id).exists()
        has_initial_context_failure = Message.objects.filter(Message='BearerContextSetupFailure',
                                                             identifiers_id=identifier.id).exists()

        ctxt, ctxt_created = IdentifiersStats.objects.get_or_create(
            category='Bctxt',
            identifier_id=identifier.id,
            uploadedFiles_id=file_id,
            cucp_f1c_ip=ip
        )
        if ctxt_created or (ctxt is not None and ctxt.attempts == 0):
            if has_initial_context_request:
                ctxt.attempts += 1
            if has_initial_context_response:
                ctxt.success += 1
            if has_initial_context_failure:
                ctxt.fails += 1
            if has_initial_context_request and not has_initial_context_failure and not has_initial_context_response:
                ctxt.timeouts += 1
            ctxt.save()

    @classmethod
    def check_is_analysis_complete(cls, file_id):
        identifiers_rrc_count = Message.objects.filter(identifiers__uploadedFiles_id=file_id,
                                                       Message='RRC Setup').count()
        processed_identifiers_rrc_count = IdentifiersStats.objects.filter(
            uploadedFiles_id=file_id,
            category='RRC',
            attempts__gt=0,
        ).count()

        identifiers_ctxt_count = Message.objects.filter(identifiers__uploadedFiles_id=file_id,
                                                        Message='InitialContextSetupRequest').count()
        processed_identifiers_ctxt_count = IdentifiersStats.objects.filter(
            uploadedFiles_id=file_id,
            category='InitialCtxt',
            attempts__gt=0,
        ).count()

        identifiers_bctxt_count = Message.objects.filter(identifiers__uploadedFiles_id=file_id,
                                                         Message='BearerContextSetupRequest').count()
        processed_identifiers_bctxt_count = IdentifiersStats.objects.filter(
            uploadedFiles_id=file_id,
            category='Bctxt',
            attempts__gt=0,
        ).count()

        if identifiers_rrc_count == processed_identifiers_rrc_count and identifiers_rrc_count == processed_identifiers_ctxt_count and identifiers_rrc_count == processed_identifiers_bctxt_count:
            upload_file = UploadedFile.objects.get(id=file_id)
            upload_file.is_analysis_complete = True
            upload_file.save()

    @classmethod
    def update_stats_by_id(cls, file_id):
        upload_file = UploadedFile.objects.get(id=file_id)
        unique_ips = Identifiers.objects.filter(uploadedFiles_id=file_id).values_list('CUCP_F1C_IP',
                                                                                      flat=True).distinct()

        if not upload_file.is_analysis_complete:
            with transaction.atomic():
                for ip in unique_ips:
                    identifiers = Identifiers.objects.filter(uploadedFiles_id=file_id, CUCP_F1C_IP=ip)
                    for identifier in identifiers:
                        cls.rrc_related_message_stats(file_id, ip, identifier)
                        cls.initial_related_messages_stats(file_id, ip, identifier)
                        cls.bearerctxt_related_messages_stats(file_id, ip, identifier)

                    cls.update_cumulative_stats(file_id, 'RRC', ip)
                    cls.update_cumulative_stats(file_id, 'InitialCtxt', ip)
                    cls.update_cumulative_stats(file_id, 'Bctxt', ip)

                    cls.check_is_analysis_complete(file_id)

    @classmethod
    def get_cucp_ips(cls, id):
        unique_cucp_ips = Identifiers.objects.filter(
            uploadedFiles_id=id,
            CUCP_F1C_IP__isnull=False,
        ).exclude(CUCP_F1C_IP="").values_list("CUCP_F1C_IP", flat=True).order_by('CUCP_F1C_IP').distinct()

        return unique_cucp_ips

    @classmethod
    def update_cumulative_stats(cls, upload_file_id, category, ip):
        identifier_stats_summary = IdentifiersStats.objects.filter(
            uploadedFiles_id=upload_file_id, category=category, cucp_f1c_ip=ip
        ).aggregate(
            attempts_count=Sum('attempts'),
            success_count=Sum('success'),
            fails_count=Sum('fails'),
            timeouts_count=Sum('timeouts')
        )
        cumulative_stats, created = Stats.objects.get_or_create(category=category, uploadedFiles_id=upload_file_id,
                                                                cucp_f1c_ip=ip)

        if identifier_stats_summary:
            cumulative_stats.attempts = identifier_stats_summary['attempts_count'] or 0
            cumulative_stats.success = identifier_stats_summary['success_count'] or 0
            cumulative_stats.fails = identifier_stats_summary['fails_count'] or 0
            cumulative_stats.timeouts = identifier_stats_summary['timeouts_count'] or 0

        cumulative_stats.save()