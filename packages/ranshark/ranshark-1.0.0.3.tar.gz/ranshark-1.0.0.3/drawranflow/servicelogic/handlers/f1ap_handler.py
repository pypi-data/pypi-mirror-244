import json
import logging
import os

import pandas as pd
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from drawranflow.models import Identifiers, Message
from .utils import getGnbId as gid

def open_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return f"File Not found {file_name}"
    return data


def configure_logging(log_file_path):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
        ]
    )


# Configuration for log file path
BASE_DIR = getattr(settings, 'BASE_DIR', None)
LOG_FILE_PATH = os.path.join(BASE_DIR, 'debug.log')
configure_logging(LOG_FILE_PATH)


def get_direction(message, interface):
    direction = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'intfconfig', f'{interface}_proc.json'))
    direct = open_file(direction)
    directions = direct.get(message.lower(), {})
    return directions.get("srcNode"), directions.get("dstNode")


def process_f1dataframe(row, index, interface, item_id):
    # Process "RRC Setup Request" messages
    gnb_du_ue_f1ap_id = row['f1ap.GNB_DU_UE_F1AP_ID']
    gnb_cu_ue_f1ap_id = row['f1ap.GNB_CU_UE_F1AP_ID']
    pci = row['nr-rrc.pdcch_DMRS_ScramblingID']
    message_type = row['_ws.col.info']
    logging.debug(
        f"Processing row {index}: GNB_DU_UE_F1AP_ID={gnb_du_ue_f1ap_id}, GNB_CU_UE_F1AP_ID={gnb_cu_ue_f1ap_id}"
        f",Message Type={message_type}, pci:{pci}")

    match message_type:
        case "RRC Setup Request":
            cucp_f1c_ip = row['ip.dst']
            logging.debug("Processing RRC Setup Request ")
            nrcgi = row['f1ap.nRCellIdentity']
            nrcgi = nrcgi.replace(":", "")
            gnb_id = gid(nrcgi)
            try:
                # Check if the identifier exists
                identifier_exists = Identifiers.objects.filter(
                    GNB_DU_UE_F1AP_ID=gnb_du_ue_f1ap_id,
                    C_RNTI=row['f1ap.C_RNTI'],
                    uploadedFiles_id=item_id,
                    CUCP_F1C_IP=cucp_f1c_ip,

                ).exists()

                if not identifier_exists:
                    if pci:
                        identifier_object, created = Identifiers.objects.get_or_create(
                            C_RNTI=row['f1ap.C_RNTI'],
                            GNB_DU_UE_F1AP_ID=gnb_du_ue_f1ap_id,
                            pci=pci,
                            uploadedFiles_id=item_id,
                            CUCP_F1C_IP=cucp_f1c_ip,
                            gnb_id= gnb_id
                        )
                    else:
                        identifier_object, created = Identifiers.objects.get_or_create(
                            C_RNTI=row['f1ap.C_RNTI'],
                            GNB_DU_UE_F1AP_ID=gnb_du_ue_f1ap_id,
                            uploadedFiles_id=item_id,
                            CUCP_F1C_IP=cucp_f1c_ip,

                        )
                    identifier_to_create = identifier_object
                    save_messages(row, identifier_to_create, interface)
                else:
                    pass

            except Exception as e:
                logging.error(f"Error processing RRC Setup Request: {e}")
        case "RRC Reestablishment Request":

            cucp_f1c_ip = row['ip.dst'],
            nrcgi = row['f1ap.nRCellIdentity']
            nrcgi = nrcgi.replace(":", "")
            gnb_id = gid(nrcgi)
            logging.debug("Processing Reestablishment Request")
            try:
                # Check if the identifier exists
                identifier_exists = Identifiers.objects.filter(
                    GNB_DU_UE_F1AP_ID=gnb_du_ue_f1ap_id,
                    C_RNTI=row['f1ap.C_RNTI'],
                    uploadedFiles_id=item_id,
                    CUCP_F1C_IP=cucp_f1c_ip,

                ).exists()

                if not identifier_exists:
                    if pci:
                        identifier_object, created = Identifiers.objects.get_or_create(
                            C_RNTI=row['f1ap.C_RNTI'],
                            GNB_DU_UE_F1AP_ID=gnb_du_ue_f1ap_id,
                            pci=pci,
                            uploadedFiles_id=item_id,
                            gnb_id=gnb_id
                        )
                    else:
                        identifier_object, created = Identifiers.objects.get_or_create(
                            C_RNTI=row['f1ap.C_RNTI'],
                            GNB_DU_UE_F1AP_ID=gnb_du_ue_f1ap_id,
                            uploadedFiles_id=item_id,
                            CUCP_F1C_IP=cucp_f1c_ip,

                        )
                    identifier_to_create = identifier_object
                    save_messages(row, identifier_to_create, interface)
                else:
                    pass

            except Exception as e:
                logging.error(f"Error processing RRC Reestablishment Request: {e}")

        case 'RRC Setup':
            if not pd.isnull(gnb_du_ue_f1ap_id) and not pd.isnull(gnb_cu_ue_f1ap_id):
                try:
                    cucp_f1c_ip = row['ip.src']

                    existing_identifier = Identifiers.objects.get(
                        GNB_DU_UE_F1AP_ID=gnb_du_ue_f1ap_id,
                        GNB_CU_UE_F1AP_ID__isnull=True,
                        uploadedFiles_id=item_id,
                        CUCP_F1C_IP=cucp_f1c_ip,
                    )
                    if existing_identifier:
                        existing_identifier.GNB_CU_UE_F1AP_ID = gnb_cu_ue_f1ap_id
                        if pci:
                            existing_identifier.pci = pci
                        existing_identifier.save()
                        save_messages(row, existing_identifier, interface)
                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...{index}")
                    pass
            else:
                pass
        case _:
            if not pd.isnull(gnb_du_ue_f1ap_id) and not pd.isnull(gnb_cu_ue_f1ap_id):
                try:
                    existing_identifier = Identifiers.objects.get(
                        GNB_DU_UE_F1AP_ID=gnb_du_ue_f1ap_id,
                        GNB_CU_UE_F1AP_ID=gnb_cu_ue_f1ap_id,
                        uploadedFiles_id=item_id

                    )
                    if existing_identifier:
                        # Check if "RRC Setup Request" exists for the identifier
                        rrc_setup_request_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='RRC Setup Request'
                        ).exists()
                        rrc_reestblish_request_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='RRC Reestablishment Request'
                        ).exists()

                        if rrc_setup_request_exists or rrc_reestblish_request_exists:
                            save_messages(row, existing_identifier, interface)
                        else:
                            logging.info(
                                f"Skipping DB update/inserts for row {index}. 'RRC Setup Request' not found in Messages for the identifier.")
                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...")
                    pass
            else:
                pass


def process_e1dataframe(row, index, interface, item_id):
    gnb_cu_cp_ue_e1ap_id = row['e1ap.GNB_CU_CP_UE_E1AP_ID']
    gnb_cu_up_ue_e1ap_id = row['e1ap.GNB_CU_UP_UE_E1AP_ID']
    message_type = row['_ws.col.info']
    logging.debug(
        f"Processing row {index}: GNB_CU_CP_UE_E1AP_ID={gnb_cu_cp_ue_e1ap_id}, GNB_CU_UP_UE_E1AP_ID={gnb_cu_up_ue_e1ap_id}"
        f",Message Type={message_type}")

    match message_type:
        case 'BearerContextSetupRequest':
            logging.debug("Processing BearerContextSetupRequest")
            try:
                # Check if the identifier exists
                identifier_object = Identifiers.objects.get(
                    GNB_CU_UE_F1AP_ID=gnb_cu_cp_ue_e1ap_id,
                    GNB_CU_CP_UE_E1AP_ID__isnull=True,
                    GNB_CU_UP_UE_E1AP_ID__isnull=True,
                    uploadedFiles_id=item_id

                )
                # Print messages associated with the identifier for debugging
                associated_messages = Message.objects.filter(identifiers_id=identifier_object.id)
                for msg in associated_messages:
                    logging.debug(f"Message for identifier {identifier_object.id}: {msg.Message}")

                rrc_setup_complete_exists = Message.objects.filter(
                    identifiers_id=identifier_object.id,
                    Message__iexact='Service request'.strip()  # Case-insensitive and strip spaces
                ).exists()
                logging.debug(
                    f"Message for identifier {identifier_object.id}: {Message.objects.filter(identifiers_id=identifier_object.id).values_list('Message', flat=True)}")
                rrc_reg_complete_exists = Message.objects.filter(
                    identifiers_id=identifier_object.id,
                    Message__iexact='Registration request'.strip()  # Case-insensitive and strip spaces
                ).exists()
                logging.debug(
                    f"Identifiers object {identifier_object.id}, rrc_setup_complete_exists: {rrc_setup_complete_exists}")

                # print(rrc_setup_complete_exists, "rrc_setup_complete_exists", identifier_object)
                if rrc_setup_complete_exists or rrc_reg_complete_exists:
                    identifier_object.GNB_CU_CP_UE_E1AP_ID = gnb_cu_cp_ue_e1ap_id
                    identifier_object.save()
                    save_messages(row, identifier_object, interface)

            except Identifiers.DoesNotExist:
                logging.error("Identifier does not exist.")
                pass
            except Exception as e:
                logging.error(f"Error processing BearerContextSetupRequest: {e}")
                pass
        case 'BearerContextSetupResponse':
            logging.debug("Processing BearerContextSetupResponse or BearerContextSetupFailure")
            if not pd.isnull(gnb_cu_cp_ue_e1ap_id) and not pd.isnull(gnb_cu_up_ue_e1ap_id):
                try:
                    existing_identifier = Identifiers.objects.get(
                        GNB_CU_CP_UE_E1AP_ID=gnb_cu_cp_ue_e1ap_id,
                        GNB_CU_UP_UE_E1AP_ID__isnull=True,
                        uploadedFiles_id=item_id

                    )
                    if existing_identifier:
                        existing_identifier.GNB_CU_UP_UE_E1AP_ID = gnb_cu_up_ue_e1ap_id
                        existing_identifier.save()
                        save_messages(row, existing_identifier, interface)
                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...{index}")
                    pass
            else:
                pass
        case 'BearerContextSetupFailure':
            logging.debug("Processing BearerContextSetupResponse or BearerContextSetupFailure")

            if not pd.isnull(gnb_cu_cp_ue_e1ap_id) and not pd.isnull(gnb_cu_up_ue_e1ap_id):
                try:
                    existing_identifier = Identifiers.objects.get(
                        GNB_CU_CP_UE_E1AP_ID=gnb_cu_cp_ue_e1ap_id,
                        GNB_CU_UP_UE_E1AP_ID__isnull=True,
                        uploadedFiles_id=item_id

                    )
                    if existing_identifier:
                        existing_identifier.GNB_CU_UP_UE_E1AP_ID = gnb_cu_up_ue_e1ap_id
                        existing_identifier.save()
                        save_messages(row, existing_identifier, interface)
                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...{index}")
                    pass
            else:
                pass
        case _:
            if not pd.isnull(gnb_cu_cp_ue_e1ap_id) and not pd.isnull(gnb_cu_up_ue_e1ap_id):
                try:
                    existing_identifier = Identifiers.objects.get(
                        GNB_CU_CP_UE_E1AP_ID=gnb_cu_cp_ue_e1ap_id,
                        GNB_CU_UP_UE_E1AP_ID=gnb_cu_up_ue_e1ap_id,
                        uploadedFiles_id=item_id

                    )
                    if existing_identifier:
                        # Check if "RRC Setup Request" exists for the identifier
                        bearer_context_setup_response_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='BearerContextSetupResponse'
                        ).exists()

                        if bearer_context_setup_response_exists:
                            save_messages(row, existing_identifier, interface)
                        else:
                            logging.info(
                                f"Skipping DB update/inserts for row {index}. 'BearerContextSetupResponse' not found in Messages for the identifier.")
                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...")
                    pass
            else:
                pass


def process_ngapdataframe(row, index, interface, item_id):
    ran_ue_ngap_id = row['ngap.RAN_UE_NGAP_ID']
    amf_ue_ngap_id = row['ngap.AMF_UE_NGAP_ID']
    message_type = row['_ws.col.info']
    logging.debug(
        f"Processing row {index}: RAN_UE_NGAP_ID={ran_ue_ngap_id}, AMF_UE_NGAP_ID={amf_ue_ngap_id}"
        f",Message Type={message_type}")

    match message_type:
        case message_type if 'Service request' in message_type or "Registration request" in message_type or "Tracking area update request" in message_type:
            logging.debug("Processing Service request or Registration or Tracking")
            try:
                # Check if the identifier exists
                identifier_object = Identifiers.objects.get(
                    GNB_CU_UE_F1AP_ID=ran_ue_ngap_id,
                    RAN_UE_NGAP_ID__isnull=True,
                    AMF_UE_NGAP_ID__isnull=True,
                    uploadedFiles_id=item_id

                )

                # # Print messages associated with the identifier for debugging
                # associated_messages = Message.objects.filter(identifiers_id=identifier_object.id)
                # for msg in associated_messages:
                #     logging.debug(f"Message for identifier {identifier_object.id}: {msg.Message}")

                # Additional conditions after confirming that the identifier exists
                rrc_setup_complete_exists = Message.objects.filter(
                    identifiers_id=identifier_object.id,
                    Message__iexact='Service request'.strip()  # Case-insensitive and strip spaces
                ).exists()
                reg_complete_exists = Message.objects.filter(
                    identifiers_id=identifier_object.id,
                    Message__iexact='Registration request'.strip()  # Case-insensitive and strip spaces
                ).exists()
                track_complete_exists = Message.objects.filter(
                    identifiers_id=identifier_object.id,
                    Message__iexact='Tracking area update request'.strip()  # Case-insensitive and strip spaces
                ).exists()

                logging.debug(
                    f"Message for identifier {identifier_object.id}: {Message.objects.filter(identifiers_id=identifier_object.id).values_list('Message', flat=True)}")

                logging.debug(
                    f"Identifiers object {identifier_object.id}, rrc_setup_complete_exists: {rrc_setup_complete_exists}")

                if rrc_setup_complete_exists or reg_complete_exists or track_complete_exists:
                    # and (service_request_exists or registration_request_exists):
                    identifier_object.RAN_UE_NGAP_ID = ran_ue_ngap_id
                    identifier_object.save()
                    save_messages(row, identifier_object, interface)

            except Identifiers.DoesNotExist:
                logging.error("Identifier does not exist.")
                pass
            except Exception as e:
                logging.error(f"Error processing Service request: {e}")
                pass

        case message_type if 'InitialContextSetupRequest' in message_type or message_type.startswith(
                'Registration reject'):
            logging.debug("Processing InitialContextSetupRequest")

            if not pd.isnull(ran_ue_ngap_id) and not pd.isnull(amf_ue_ngap_id):
                try:

                    existing_identifier = Identifiers.objects.get(
                        RAN_UE_NGAP_ID=ran_ue_ngap_id,
                        AMF_UE_NGAP_ID__isnull=True,
                        uploadedFiles_id=item_id

                    )
                    if existing_identifier:
                        existing_identifier.AMF_UE_NGAP_ID = amf_ue_ngap_id
                        existing_identifier.save()
                        save_messages(row, existing_identifier, interface)

                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...{index}")
                    pass
            else:
                pass
        case message if message.startswith('Registration reject'):
            logging.debug("Processing Registration reject")

            if not pd.isnull(ran_ue_ngap_id) and not pd.isnull(amf_ue_ngap_id):
                try:
                    existing_identifier = Identifiers.objects.get(
                        GNB_CU_UE_F1AP_ID=ran_ue_ngap_id,
                        RAN_UE_NGAP_ID=ran_ue_ngap_id,
                        AMF_UE_NGAP_ID__isnull=True,
                        uploadedFiles_id=item_id

                    )
                    if existing_identifier:
                        existing_identifier.AMF_UE_NGAP_ID = amf_ue_ngap_id
                        existing_identifier.save()
                        save_messages(row, existing_identifier)
                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...{index}")
                    pass
            else:
                pass
        case _:
            if not pd.isnull(ran_ue_ngap_id) and not pd.isnull(amf_ue_ngap_id):
                try:
                    existing_identifier = Identifiers.objects.get(
                        RAN_UE_NGAP_ID=ran_ue_ngap_id,
                        AMF_UE_NGAP_ID=amf_ue_ngap_id,
                        uploadedFiles_id=item_id

                    )
                    if existing_identifier:
                        # Check if "RRC Setup Request" exists for the identifier
                        registration_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='Registration request',
                            Protocol__icontains='ngap'
                        ).exists()
                        service_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='Service request',
                            Protocol__icontains='ngap'
                        ).exists()
                        tracking_area_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='Tracking area update request',
                            Protocol__icontains='ngap'
                        ).exists()
                        if registration_exists or service_exists or tracking_area_exists:
                            save_messages(row, existing_identifier, interface)
                        else:
                            logging.info(
                                f"Skipping DB update/inserts for row {index}. 'Registration request/Service request/Tracking area' not found in Messages for the identifier.")
                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...")
                    pass
            else:
                pass


def process_xnapdataframe(row, index, interface, item_id):
    XNAP_SRC_RAN_ID = row['xnap.NG_RANnodeUEXnAPID_src']
    XNAP_TRGT_RAN_ID = row['xnap.NG_RANnodeUEXnAPID_dst']

    message_type = row['_ws.col.info']
    logging.debug(
        f"Processing row {index}: NG_RANnodeUEXnAPID_src={XNAP_SRC_RAN_ID},"
        f"NG_RANnodeUEXnAPID_dst={XNAP_TRGT_RAN_ID},,Message Type={message_type}")

    match message_type:
        case 'HandoverRequest':
            logging.debug("Processing XNAP HandoverRequest")
            try:
                # Check if the identifier exists
                identifier_object = Identifiers.objects.get(
                    GNB_CU_UE_F1AP_ID=XNAP_SRC_RAN_ID,
                    XNAP_SRC_RAN_ID__isnull=True,
                    XNAP_TRGT_RAN_ID__isnull=True,
                    AMF_UE_NGAP_ID__isnull=False,
                    uploadedFiles_id=item_id

                )

                # # Print messages associated with the identifier for debugging
                # associated_messages = Message.objects.filter(identifiers_id=identifier_object.id)
                # for msg in associated_messages:
                #     logging.debug(f"Message for identifier {identifier_object.id}: {msg.Message}")

                # Additional conditions after confirming that the identifier exists
                rrc_setup_complete_exists = Message.objects.filter(
                    identifiers_id=identifier_object.id,
                    Message__iexact='Service request'.strip()  # Case-insensitive and strip spaces
                ).exists()
                reg_complete_exists = Message.objects.filter(
                    identifiers_id=identifier_object.id,
                    Message__iexact='Registration request'.strip()  # Case-insensitive and strip spaces
                ).exists()
                track_complete_exists = Message.objects.filter(
                    identifiers_id=identifier_object.id,
                    Message__iexact='Tracking area update request'.strip()  # Case-insensitive and strip spaces
                ).exists()

                logging.debug(
                    f"Message for identifier {identifier_object.id}: {Message.objects.filter(identifiers_id=identifier_object.id).values_list('Message', flat=True)}")

                logging.debug(
                    f"Identifiers object {identifier_object.id}, rrc_setup_complete_exists: {rrc_setup_complete_exists}")

                if rrc_setup_complete_exists or reg_complete_exists or track_complete_exists:
                    # and (service_request_exists or registration_request_exists):
                    identifier_object.XNAP_SRC_RAN_ID = XNAP_SRC_RAN_ID
                    identifier_object.save()
                    save_messages(row, identifier_object, interface)

            except Identifiers.DoesNotExist:
                logging.error("Identifier does not exist.")
                pass
            except Exception as e:
                logging.error(f"Error processing Service request: {e}")
                pass

        case message_type if 'HandoverRequestAcknowledge' in message_type:
            logging.debug("Processing HandoverRequestAcknowledge")

            if not pd.isnull(XNAP_SRC_RAN_ID) and not pd.isnull(XNAP_TRGT_RAN_ID):
                try:

                    existing_identifier = Identifiers.objects.get(
                        XNAP_SRC_RAN_ID=XNAP_SRC_RAN_ID,
                        RAN_UE_NGAP_ID=XNAP_SRC_RAN_ID,
                        XNAP_TRGT_RAN_ID__isnull=True,
                        uploadedFiles_id=item_id

                    )
                    if existing_identifier:
                        existing_identifier.XNAP_TRGT_RAN_ID = XNAP_TRGT_RAN_ID
                        existing_identifier.save()
                        save_messages(row, existing_identifier, interface)
                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...{index}")
                    pass
            else:
                pass
        case _:
            if not pd.isnull(XNAP_TRGT_RAN_ID) and not pd.isnull(XNAP_SRC_RAN_ID):
                try:
                    existing_identifier = Identifiers.objects.get(
                        XNAP_TRGT_RAN_ID=XNAP_TRGT_RAN_ID,
                        XNAP_SRC_RAN_ID=XNAP_SRC_RAN_ID,
                        uploadedFiles_id=item_id

                    )
                    if existing_identifier:
                        # Check if "RRC Setup Request" exists for the identifier
                        registration_exists = Message.objects.filter(
                            identifiers=existing_identifier,
                            Message='HandoverRequest'
                        ).exists()
                        if registration_exists:
                            save_messages(row, existing_identifier, interface)
                        else:
                            logging.info(
                                f"Skipping DB update/inserts for row {index}. 'HandoverRequest' not found in Messages for the identifier.")
                except ObjectDoesNotExist as e:
                    logging.error(f"ObjectDoesNotExist: {e}. Skipping...")
                    pass
            else:
                pass


def open_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return f"File Nor found {file_name}"
    return data


def getDirection(message, interface):
    direction = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'intfconfig', f'{interface}_proc.json'))
    direct = open_file(direction)
    directions = {}
    if isinstance(message, list):
        message = message[0]
    for key, values in direct.items():
        if key.lower() == message.lower():
            directions = values
    logging.debug(f'{message},{directions["srcNode"]},{directions["dstNode"]}')
    return directions["srcNode"], directions["dstNode"]


def create_message_object(row, identifier, interface):
    try:
        timestamp_str = row['frame.time']
        srcNode, dstNode = getDirection(row['_ws.col.info'], interface)

        message = Message(
            FrameNumber=row['frame.number'],
            FrameTime=timestamp_str,
            IpSrc=row['ip.src'],
            IpDst=row['ip.dst'],
            Protocol=row['frame.protocols'],
            F1_Proc=row['f1ap.procedureCode'],
            E1_Proc=row['e1ap.procedureCode'],
            NG_Proc=row['ngap.procedureCode'],
            C1_RRC=row['nr-rrc.c1'],
            C2_RRC=row['nr-rrc.c2'],
            MM_Message_Type=row['nas-5gs.mm.message_type'],
            SM_Message_Type=row['nas-5gs.sm.message_type'],
            Message=row['_ws.col.info'],
            identifiers=identifier,
            srcNode=srcNode,
            dstNode=dstNode,
        )
        logging.debug(
            f" creating message with src Node: {srcNode}, dstNode: {dstNode}, Message : {row['_ws.col.info']}, FrameNumner: {row['frame.number']}, Identifier_id: {identifier}")
        return message

    except Exception as e:
        logging.error(f"Error creating message object: {e}, {row['_ws.col.info']},{row['frame.number']}, {identifier}")

    return None


def save_messages(row, identifier, interface):
    # Check if a message of the same type and frame number already exists for the identifier
    message_type = row['_ws.col.info']
    frame_number = row['frame.number']
    message_exists = None
    try:
        message_exists = Message.objects.filter(
            identifiers=identifier,
            Message=message_type,
            FrameNumber=frame_number
        ).exists()
    except Exception as e:
        logging.error(f"Failed to query save message , {e}, {row['_ws.col.info']},{identifier}")
    if not message_exists:
        # Process the message
        message = create_message_object(row, identifier, interface)
        message.save()
        logging.debug(f"Saved message: {message}")
