SUPABASE_URL = "https://botphmiwdqesguwrytbm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvdHBobWl3ZHFlc2d1d3J5dGJtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjgxNjY4OSwiZXhwIjoyMDg4MzkyNjg5fQ.Sluxkkuk3RrbdfZpIVuTYzysIOw9Y0M91JxgLk3nvP0"
# SUPABASE_URL = "https://mukjajpmohydgwxqimeg.supabase.co"
# SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im11a2phanBtb2h5ZGd3eHFpbWVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2MDIzMjMsImV4cCI6MjA4NzE3ODMyM30.Ff1q1z0vth9oKOO8eYp_aiLv7zHpsZgcp983NhnI0No"
 
import asyncio
 
from fastapi import HTTPException
 
from supabase import create_client, Client
from typing import  Dict, Any
 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
 
def parse_eci_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse and structure ECI API response"""
    return {
        "id": response_data.get("id"),
        "epicid": response_data.get("epicId"),
        "epicnumber": response_data.get("epicNumber"),
        "formreferenceno": response_data.get("formReferenceNo"),
       
        # Personal Information
        "applicantfirstname": response_data.get("applicantFirstName"),
        "applicantfirstnamel1": response_data.get("applicantFirstNameL1"),
        "applicantfirstnamel2": response_data.get("applicantFirstNameL2"),
        "applicantlastname": response_data.get("applicantLastName"),
        "applicantlastnamel1": response_data.get("applicantLastNameL1"),
        "applicantlastnamel2": response_data.get("applicantLastNameL2"),
        "fullname": response_data.get("fullName"),
        "fullnamel1": response_data.get("fullNameL1"),
       
        # Demographics
        "age": response_data.get("age"),
        "gender": response_data.get("gender"),
        "genderl1": response_data.get("genderL1"),
        "birthyear": response_data.get("birthYear"),
       
        # Relation Information
        "relationtype": response_data.get("relationType"),
        "relationtypel1": response_data.get("relationTypeL1"),
       
        "relationnamel1": response_data.get("relationNameL1"),
        "relationnamel2": response_data.get("relationNameL2"),
        "relationlname": response_data.get("relationLName"),
        "relationlnamel1": response_data.get("relationLNameL1"),
        "relativefullname": response_data.get("relativeFullName"),
        "relativefullnamel1": response_data.get("relativeFullNameL1"),
       
        # Location Information
        "partnumber": response_data.get("partNumber"),
        "partid": response_data.get("partId"),
        "partname": response_data.get("partName"),
        "partnamel1": response_data.get("partNameL1"),
        "partserialnumber": response_data.get("partSerialNumber"),
        "sectionno": response_data.get("sectionNo"),
       
        # Assembly/Parliamentary Details
        "asmblyname": response_data.get("asmblyName"),
        "asmblynamel1": response_data.get("asmblyNameL1"),
        "acid": response_data.get("acId"),
        "acnumber": response_data.get("acNumber"),
        "prlmntname": response_data.get("prlmntName"),
        "prlmntnamel1": response_data.get("prlmntNameL1"),
        "prlmntno": response_data.get("prlmntNo"),
       
        # District/State
        "districtvalue": response_data.get("districtValue"),
        "districtvaluel1": response_data.get("districtValueL1"),
        "districtcd": response_data.get("districtCd"),
        "districtid": response_data.get("districtId"),
        "districtno": response_data.get("districtNo"),
        "statename": response_data.get("stateName"),
        "statenamel1": response_data.get("stateNameL1"),
        "stateid": response_data.get("stateId"),
        "statecd": response_data.get("stateCd"),
       
        # Polling Station Details
        "psbuildingname": response_data.get("psbuildingName"),
        "psbuildingnamel1": response_data.get("psBuildingNameL1"),
        "psroomdetails": response_data.get("psRoomDetails"),
        "psroomdetailsl1": response_data.get("psRoomDetailsL1"),
        "buildingaddress": response_data.get("buildingAddress"),
        "buildingaddressl1": response_data.get("buildingAddressL1"),
        "partlatlong": response_data.get("partLatLong"),
       
        # Disability Information
        "disabilityany": response_data.get("disabilityAny"),
        "disabilitytype": response_data.get("disabilityType"),
        "islocomotordisabled": response_data.get("isLocomotorDisabled"),
        "isspeechhearingdisabled": response_data.get("isSpeechHearingDisabled"),
        "isvisuallyimpaired": response_data.get("isVisuallyImpaired"),
        "otherdisability": response_data.get("otherDisability"),
        "iswheelchairrequired": response_data.get("isWheelchairRequired"),
        "pwd": response_data.get("pwd"),
        "pwdmarkingformtype": response_data.get("pwdMarkingFormType"),
        "pwdmarkingrefno": response_data.get("pwdMarkingRefNo"),
       
        # Form/Process Information
        "formtype": response_data.get("formType"),
        "processtype": response_data.get("processType"),
        "statustype": response_data.get("statusType"),
        "revisionid": response_data.get("revisionId"),
       
        # Timestamps
        "createddttm": response_data.get("createdDttm"),
        "modifieddttm": response_data.get("modifiedDttm"),
        "epicdatetime": response_data.get("epicDatetime"),
       
        # Flags
        "isactive": response_data.get("isActive", True),
        "isdeleted": response_data.get("isDeleted", False),
        "isvalidated": response_data.get("isValidated"),
        "isvip": response_data.get("isVip"),
        "isform8migration": response_data.get("isForm8Migration"),
 
 
        #Section Covered
        "sectionno": response_data.get("sectionNo"),
   
   
    }
async def save_voter_to_db(voter_data: Dict[str, Any]) -> str:
    """Save voter data to Supabase"""
    try:
        # Check for duplicate
        existing = supabase.table("voter_records").select("id").eq("epicnumber", voter_data["epicnumber"]).execute()
       
        if existing.data:
            raise HTTPException(status_code=409, detail="Voter already exists in database")
       
        # Insert voter
        result = supabase.table("voter_records").insert(voter_data).execute()
       
        if result.data:
            return result.data[0]["id"]
        else:
            raise HTTPException(status_code=500, detail="Failed to save voter to database")
           
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
   
 
 
async def process_voter_data(voter_data: Dict[str, Any]) -> str:
     voter_id = await save_voter_to_db(voter_data)
     return {
        "message": "Voter data saved successfully",
        "voter_id": voter_id
     }
 
if __name__ == "__main__":
   
    voters_data={'id': '3608982_JQQ0420802_S08', 'epicId': 3608982, 'epicNumber': 'JQQ0420802', 'formReferenceNo': None, 'applicantFirstName': 'SAVITA', 'underJo': None, 'applicantFirstNameL1': 'सविता', 'applicantFirstNameL2': None, 'applicantLastName': None, 'applicantLastNameL1': None, 'applicantLastNameL2': None, 'relationName': 'MAHENDER', 'relationNameL1': 'महेन्द्र', 'relationNameL2': None, 'age': 46, 'gender': 'F', 'partNumber': '2', 'partId': 2247, 'partName': 'LOT', 'partNameL1': 'लोट', 'partSerialNumber': 31, 'asmblyName': 'BAIJNATH', 'asmblyNameL1': 'बैजनाथ', 'acId': 9, 'acNumber': 20, 'prlmntName': 'Kangra', 'prlmntNameL1': None, 'prlmntNo': '1', 'districtValue': 'KANGRA', 'districtValueL1': 'कांगड़ा', 'districtCd': 'S0802', 'districtId': None, 'districtNo': 2, 'stateName': 'Himachal Pradesh', 'stateNameL1': 'हिमाचल प्रदेश', 'stateId': 8,'pwdMarkingRefNo': None, 'pwd': None, 'isVip': None, 'epicDatetime': '2025-03-18T10:33:12.285+00:00', 'fullName': 'savita', 'fullNameL1': 'सविता', 'relativeFullName': 'mahender', 'relativeFullNameL1': 'महेन्द्र', 'psRoomDetails': 'ROOM NO 2', 'psRoomDetailsL1': 'कमरा नंबर 2', 'psBuildingNameL1': 'रा.प्रा.पा.', 'buildingAddress': 'LOT Tehsil BAIJNATH District Kangra Pin Code-176115', 'buildingAddressL1': 'लोट तहसील बैजनाथ जिला काँगड़ा पिन कोड-176115'}
    parsed_data = parse_eci_response(voters_data)
    message=asyncio.run(process_voter_data(parsed_data))
    print(message["message"])
    print(message["voter_id"])