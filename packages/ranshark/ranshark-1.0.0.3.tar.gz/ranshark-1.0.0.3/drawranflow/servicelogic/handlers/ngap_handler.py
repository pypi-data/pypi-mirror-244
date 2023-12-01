import time
import datetime
import pandas as pd
from django.db.models import Q
from drawranflow.models import Identifiers, Message


class NgapDataFrameProcessor:
    def __init__(self, df):
        self.df = df

    def process_dataframe(self):
        print("Calling NGAP========>")
        messages_to_create = []
        for index, row in self.df.iterrows():
            message_type = row['Message']
            frame_number = row['FrameNumber']

            if message_type == 'Service request' or message_type == 'Registration Request':
                ran_ue_ngap_id = row['RAN_UE_NGAP_ID']

                # Check if an identifier exists with GNB_CU_UE_F1AP_ID and RAN_UE_NGAP_ID is not null
                if not pd.isnull(ran_ue_ngap_id):
                    # Check if an identifier with the specified conditions already exists
                    identifier_exists = Identifiers.objects.filter(
                        GNB_CU_UE_F1AP_ID=ran_ue_ngap_id,
                        RAN_UE_NGAP_ID__isnull=True
                    ).first()
                    print("identifier_exists",identifier_exists)
                    # Check if a message of the same type already exists for this identifier
                    message_exists = Message.objects.filter(
                        Message=message_type,
                        FrameNumber=frame_number,
                        identifiers=identifier_exists
                    ).exists()

                    # Check if an RRC message exists for this identifier with the specified conditions
                    rrc_message_exists = Message.objects.filter(
                        Q(Protocol='sll:ethertype:ip:sctp:f1ap:pdcp-nr:nr-rrc:nas-5gs') &
                        Q(Message__in=['Service request', 'Registration Request']) &
                        Q(identifiers=identifier_exists)
                    ).exists()

                    print("rrc_message_exists and identifier_exists and not message_exists", rrc_message_exists,
                          identifier_exists, message_exists)
                    if identifier_exists and not message_exists:
                        # Update the RAN_UE_NGAP_ID field
                        identifier_exists.RAN_UE_NGAP_ID = ran_ue_ngap_id
                        identifier_exists.save()
                        self.save_messages(row, identifier_exists)

        # Now, process "RRC Setup" and other messages
        for index, row in self.df.iterrows():
            ran_ue_ngap_id = row['RAN_UE_NGAP_ID']
            amf_ue_ngap_id = row['AMF_UE_NGAP_ID']
            message_type = row['Message']
            if message_type == 'InitialContextSetupRequest':
                print(message_type)

                self.update_identifiers(row)
            else:
                print("in else",message_type)
                # Check if both GNB_DU_UE_F1AP_ID and GNB_CU_UE_F1AP_ID are not null
                if not pd.isnull(ran_ue_ngap_id) and not pd.isnull(amf_ue_ngap_id):
                    existing_identifier = Identifiers.objects.get(
                        RAN_UE_NGAP_ID=ran_ue_ngap_id,
                        AMF_UE_NGAP_ID=amf_ue_ngap_id
                    )
                    self.save_messages(row, existing_identifier)

    def create_message_object(self, row, identifier):
        end_time = time.time()
        message = Message(
            FrameNumber=row['FrameNumber'],
            FrameTime=datetime.datetime.fromtimestamp(end_time),
            IpSrc=row['IpSrc'],
            IpDst=row['IpDst'],
            Protocol=row['Protocol'],
            F1_Proc=row['F1_Proc'],
            Message=row['Message'],
            identifiers=identifier
        )
        return message

    def update_identifiers(self, row):
        ran_ue_ngap_id = row['RAN_UE_NGAP_ID']
        amf_ue_ngap_id = row['AMF_UE_NGAP_ID']
        print("identifier_exists")

        identifier_exists = Identifiers.objects.get(
            Q(GNB_CU_UE_F1AP_ID=ran_ue_ngap_id) &
            Q(AMF_UE_NGAP_ID__isnull=True) & Q(RAN_UE_NGAP_ID=ran_ue_ngap_id)
        )

        if identifier_exists:
            identifier_exists.AMF_UE_NGAP_ID = amf_ue_ngap_id
            identifier_exists.save()
            self.save_messages(row, identifier_exists)

    def save_messages(self, row, identifier):
        # Check if a message of the same type and frame number already exists for the identifier
        message_type = row['Message']
        frame_number = row['FrameNumber']

        message_exists = Message.objects.filter(
            identifiers=identifier,
            Message=message_type,
            FrameNumber=frame_number
        ).exists()

        if not message_exists:
            # Process the message
            message = self.create_message_object(row, identifier)
            message.save()
