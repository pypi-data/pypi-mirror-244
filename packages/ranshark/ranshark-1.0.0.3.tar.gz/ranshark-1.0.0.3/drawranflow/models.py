from django.db import models


class UploadedFile(models.Model):
    filename = models.CharField(max_length=255, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    proces_date = models.DateTimeField(null=True)
    processed = models.BooleanField(default=False)
    complete_at = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    is_analysis_complete = models.BooleanField(default=False)

# Identifiers Model
class Identifiers(models.Model):
    C_RNTI = models.CharField(max_length=255, null=True, blank=True)
    GNB_DU_UE_F1AP_ID = models.CharField(max_length=255, null=True, blank=True)
    GNB_CU_UE_F1AP_ID = models.CharField(max_length=255, null=True, blank=True)
    GNB_CU_CP_UE_E1AP_ID = models.CharField(max_length=255, null=True, blank=True)
    GNB_CU_UP_UE_E1AP_ID = models.CharField(max_length=255, null=True, blank=True)
    RAN_UE_NGAP_ID = models.CharField(max_length=255, null=True, blank=True)
    AMF_UE_NGAP_ID = models.CharField(max_length=255, null=True, blank=True)
    XNAP_SRC_RAN_ID = models.CharField(max_length=255, null=True, blank=True)
    XNAP_TRGT_RAN_ID = models.CharField(max_length=255, null=True, blank=True)
    pci = models.CharField(max_length=255, null=True)  # Allow NULL
    CUCP_F1C_IP = models.CharField(max_length=255, null=False, blank=True)
    gnb_id = models.CharField(max_length=255, null=False, blank=True)
    uploadedFiles = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)


class Message(models.Model):
    FrameNumber = models.IntegerField()
    FrameTime = models.DateTimeField(null=True, auto_now=False, auto_now_add=False)
    IpSrc = models.CharField(max_length=255, null=True)
    IpDst = models.CharField(max_length=255, null=True)
    Protocol = models.CharField(max_length=255, null=True)
    F1_Proc = models.CharField(max_length=255, null=True)
    E1_Proc = models.CharField(max_length=255, null=True)
    NG_Proc = models.CharField(max_length=255, null=True)
    C1_RRC = models.CharField(max_length=255, null=True)
    C2_RRC = models.CharField(max_length=255, null=True)
    MM_Message_Type = models.CharField(max_length=255, null=True)
    SM_Message_Type = models.CharField(max_length=255, null=True)
    Message = models.TextField(null=True)
    identifiers = models.ForeignKey(Identifiers, on_delete=models.CASCADE, null=True, blank=True)
    srcNode = models.CharField(max_length=255, null=True)  # Add source node field
    dstNode = models.CharField(max_length=255, null=True)  # Add destination node field
    message_json = models.JSONField(null=True)


class Stats(models.Model):
    category = models.CharField(max_length=50)
    uploadedFiles = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    success = models.IntegerField(default=0)
    fails = models.IntegerField(default=0)
    timeouts = models.IntegerField(default=0)
    cucp_f1c_ip = models.CharField(max_length=255, null=False, blank=True)


class IdentifiersStats(models.Model):
    category = models.CharField(max_length=50)
    identifier = models.ForeignKey(Identifiers, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    success = models.IntegerField(default=0)
    fails = models.IntegerField(default=0)
    timeouts = models.IntegerField(default=0)
    uploadedFiles = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    cucp_f1c_ip = models.CharField(max_length=255, null=False, blank=True)
