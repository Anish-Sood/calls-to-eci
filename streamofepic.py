import requests
import base64
import concurrent.futures
import random
import ddddocr
import itertools
import csv
from time import sleep
from proxies import proxy_list
# import supa

captcha_url = "https://gateway-voters.eci.gov.in/api/v1/captcha-service/generateCaptcha"
details_url = "https://gateway-voters.eci.gov.in/api/v1/elastic/search-by-epic-from-national-display"



# proxies={
#         "http": "http://bcnkcfeo:iuj01wt7i00z@31.59.20.176:6754/",
#         "https": "http://bcnkcfeo:iuj01wt7i00z@31.59.20.176:6754/"
#     }

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

ocr = ddddocr.DdddOcr()

def fetch_epic_data(epNo):
    # print(epNo)
    repetitons = 10
    
    with requests.Session() as session:
        session.headers.update(HEADERS)
        
        for i in range(repetitons):
            proxy = random.choice(proxy_list)
            
            session.proxies = proxy  
            
            try:
                # Get Captcha
                response = session.get(captcha_url, timeout=10)
                if response.status_code != 200:
                    continue
                
                data = response.json()
                captcha_value = data["captcha"]
                captcha_id = data["id"]

                image_bytes = base64.b64decode(captcha_value)
                captcha_ans = ocr.classification(image_bytes) 

                if not captcha_ans or len(captcha_ans) != 6:
                    continue

                payload = {
                    "captchaData": captcha_ans,
                    "captchaId": captcha_id,
                    "epicNumber": epNo,
                    "isPortal": "true",
                    "securityKey": "na",
                    "stateCd": "S19"
                }
                
                response2 = session.post(details_url, json=payload, timeout=10)
                
                if response2.status_code == 200:
                    data2 = response2.json()
                    if data2:
                        record_content = data2[0]["content"]
                        # supa.insert_voter_record(record_content) # Insert into Supabase
                        return {"epNo": epNo, "status": "success", "data": data2[0]["content"]}
                    else:
                        return {"epNo": epNo, "status": "not_found", "data": None}
                
                elif response2.status_code == 400:
                    # wrong captcha, loop retry with a new proxy
                    continue

            except Exception as e:
                # connection error, timeout, dead proxy
                # Loop will continue and pick a new proxy
                continue
                
    return {"epNo": epNo, "status": "failed", "data": f"Failed after {repetitons} retries"}


def process_stream_epics(epic_stream, max_workers):

    # convert stream to an iterator (in case a list/iterable is passed)
    epic_iter = iter(epic_stream)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Fill the initial queue up to max_workers
        future_to_epic = {}
        
        # islice takes exactly 'max_workers' items from the stream
        for epNo in itertools.islice(epic_iter, max_workers):
            future = executor.submit(fetch_epic_data, epNo)
            future_to_epic[future] = epNo
            
        # Process futures as they complete and replenish the queue
        while future_to_epic:
            # Wait for at least one future to complete
            done, _ = concurrent.futures.wait(
                future_to_epic.keys(), 
                return_when=concurrent.futures.FIRST_COMPLETED
            )
            
            for future in done:
                epNo = future_to_epic.pop(future)
                
                # handle of result
                try:
                    result = future.result()
                    print(f"Done {epNo}: {result['status']}")
                    yield result
                except Exception as exc:
                    print(f"{epNo}'s exception: {exc}")
                    yield {"epNo": epNo, "status": "exception", "data": str(exc)}
                
                # Pull the next epic from the stream to replace the finished one
                try:
                    next_epNo = next(epic_iter)
                    next_future = executor.submit(fetch_epic_data, next_epNo)
                    future_to_epic[next_future] = next_epNo
                except StopIteration:
                    pass


# if __name__ == "__main__":
#     # stream = my_epic_number_generator()

#     epic_stream = ['HP/03/043/021226', 'HP/03/043/021248', 'JQQ0388348', 'HP/03/043/021264', 'SBY0084319', 'SBY0000331', 'SBY0445031', 'SBY0172973', 'SBY0000364', 'JQQ0388371', 'SBY0468553', 'JQQ0421115', 'SBY0213256', 'SBY0124107', 'SBY0505149', 'SBY0339846', 'SBY0173013', 'SBY0552026', 'SBY0426916', 'JQQ0632570', 'HP/03/043/021181', 'HP/03/043/021188', 'SBY0107854', 'JQQ0632679', 'HP/03/043/021195', 'JQQ0420885', 'SBY0555110', 'JQQ0421123', 'SBY0000356', 'HP/03/043/021193', 'JQQ0420729', 'HP/03/043/021166', 'HP/03/043/021202', 'SBY0318006', 'SBY0486464', 'SBY0213280', 'JQQ0420802', 'SBY0440222', 'SBY0172999', 'JQQ0478636', 'SBY0340133', 'SBY0342238', 'HP/03/043/021196', 'JQQ9902313', 'HP/03/043/021201', 'SBY0444588', 'HP/03/043/021105', 'SBY0100834', 'HP/03/043/021106', 'SBY0444885', 'JQQ0478586', 'HP/03/043/021014', 'HP/03/043/021203', 'JQQ0561506', 'SBY0339838', 'JQQ0420786', 'HP/03/043/021197', 'SBY0544916', 'JQQ0561514', 'HP/03/043/021219', 'SBY0440453', 'SBY0124115', 'JQQ0561522', 'JQQ0421073', 'SBY0262212', 'SBY0173005', 'JQQ0574236', 'JQQ0421024', 'JQQ0574244', 'HP/03/043/021220', 'JQQ0561530', 'JQQ0561993', 'HP/03/043/021156', 'SBY0442160', 'SBY0041327', 'HP/03/043/021192', 'HP/03/043/021204', 'JQQ0420711', 'SBY0551994', 'SBY0127449', 'SBY0041319', 'JQQ0562009', 'HP/03/043/021247', 'HP/03/043/021221', 'SBY0108944', 'SBY0041400', 'JQQ0632703', 'SBY0551952', 'HP/03/043/021206', 'SBY0354001', 'SBY0340117', 'JQQ0561902', 'SBY0000372', 'SBY0041426', 'JQQ0561951', 'SBY0150243', 'JQQ0561175', 'JQQ0632653', 'HP/03/043/021211', 'JQQ0574228', 'JQQ0420992', 'JQQ0420976', 'HP/03/043/021238', 'JQQ0632737', 'JQQ0420745', 'SBY0150235', 'JQQ0421206', 'SBY0172981', 'SBY0041418', 'SBY0213298', 'SBY0342246', 'SBY0124123', 'JQQ0421313', 'JQQ0645275', 'JQQ0574210', 'SBY0150227', 'HP/03/043/021182', 'HP/03/043/021235', 'HP/03/043/021258', 'SBY0041392', 'SBY0041301', 'SBY0124131', 'HP/03/043/021245', 'JQQ0561217', 'SBY0340158', 'SBY0340166', 'JQQ0421016', 'JQQ0574129', 'JQQ0561241', 'SBY0339861', 'SBY0000323', 'HP/03/043/021222', 'SBY0027177', 'SBY0339812', 'SBY0468546', 'SBY0000315', 'SBY0041244', 'SBY0041285', 'JQQ0574046', 'JQQ0574087', 'HP/03/043/021257', 'JQQ0574111', 'JQQ0561274', 'SBY0538645', 'JQQ0574103', 'JQQ0574095', 'JQQ0574079', 'SBY0213249', 'JQQ0574053', 'JQQ0421362', 'SBY0555227', 'SBY0213264', 'SBY0284950', 'JQQ0421180', 'JQQ0420737', 'HP/03/043/021168', 'JQQ0574038', 'SBY0426932', 'HP/03/043/021001', 'HP/03/043/021183', 'SBY0124149', 'SBY0213272', 'SBY0127464', 'HP/03/043/021142', 'JQQ0478578', 'SBY0087700', 'JQQ0561894', 'JQQ0478594', 'JQQ0561332', 'JQQ0561282', 'SBY0354019', 'SBY0507921', 'SBY0518282', 'SBY0539080', 'JQQ0561688', 'HP/03/043/021209', 'SBY0499855', 'SBY0127472', 'HP/03/043/021207', 'JQQ0421214', 'HP/03/043/021171', 'SBY0244020', 'SBY0468595', 'JQQ0574202', 'SBY0352948', 'HP/03/043/021065', 'HP/03/043/021062', 'JQQ0421230', 'SBY0499863', 'SBY0244038', 'SBY0213199', 'JQQ0421297', 'HP/03/043/021140', 'SBY0318030', 'HP/03/043/021111', 'SBY0108902', 'SBY0318048', 'SBY0150250', 'SBY0190652', 'SBY0339853', 'HP/03/043/021141', 'SBY0314393', 'SBY0150268', 'SBY0318022', 'SBY0533638', 'JQQ0561316', 'SBY0439984', 'SBY0426973', 'SBY0084335', 'SBY0150276', 'SBY0084327', 'HP/03/043/021059', 'HP/03/043/021172', 'SBY0499871', 'JQQ0478545', 'HP/03/043/021208', 'HP/03/043/021056', 'SBY0127480', 'HP/03/043/021214', 'JQQ0421255', 'JQQ0561399', 'HP/03/043/021069', 'JQQ0561696', 'JQQ0420851', 'JQQ0561498', 'SBY0127498', 'SBY0463349', 'SBY0528471', 'SBY0190660', 'JQQ0421248', 'SBY0526038', 'JQQ0645242', 'SBY0190645', 'SBY0124156', 'HP/03/043/021112', 'JQQ0478560', 'SBY0528463', 'HP/03/043/021067', 'SBY0124164', 'SBY0486480', 'SBY0000299', 'JQQ0421149', 'HP/03/043/021074', 'SBY0483362', 'SBY0505370', 'JQQ0421263', 'JQQ0420869', 'SBY0254805', 'HP/03/043/021068', 'JQQ0421198', 'SBY0254854', 'JQQ0388363', 'SBY0254821', 'SBY0318097', 'SBY0486506', 'SBY0127506', 'JQQ0421404', 'JQQ0648568', 'HP/03/043/021027', 'SBY0465831', 'SBY0254862', 'JQQ0574186', 'HP/03/043/021024', 'HP/03/043/021052', 'HP/03/043/021028', 'JQQ0645226', 'SBY0468579', 'SBY0254789', 'HP/03/043/021054', 'SBY0314419', 'SBY0000273', 'HP/03/043/021023', 'JQQ0421354', 'JQQ0421156', 'JQQ0421396', 'SBY0318014', 'JQQ0632661', 'SBY0339721', 'SBY0213058', 'HP/03/043/021031', 'JQ09902412', 'SBY0342261', 'SBY0490441', 'SBY0522391', 'JQQ0561142', 'JQQ0561159', 'JQQ0561431', 'JQQ0561209', 'JQQ0561639', 'SBY0468587', 'SBY0353003', 'JQQ0420943', 'HP/03/043/021087', 'SBY0306308', 'SBY0041434', 'SBY0124172', 'JQQ0561621', 'JQQ0561225', 'HP/03/043/021230', 'SBY0532804', 'SBY0533711', 'JQQ0574160', 'SBY0532689', 'JQQ0561233', 'SBY0490094', 'JQQ0561407', 'SBY0041335', 'JQQ0420935', 'SBY0243980', 'HP/03/043/021046', 'JQQ0421289', 'HP/03/043/021043', 'HP/03/043/021045', 'SBY0363515', 'SBY0072546', 'SBY0190678', 'SBY0000307', 'JQQ0561852', 'SBY0483354', 'JQQ0561746', 'HP/03/043/021200', 'JQQ0421032', 'JQQ0561860', 'HP/03/043/021244', 'JQQ0561126', 'HP/03/043/021194', 'HP/03/043/021096', 'JQQ0561977', 'SBY0124180', 'HP/03/043/021134', 'HP/03/043/021165', 'JQQ0420927', 'SBY0041277', 'SBY0127514', 'SBY0213066', 'JQQ0561555', 'JQQ0561738', 'HP/03/043/021164', 'SBY0000349', 'HP/03/043/021252', 'SBY0127522', 'JQQ0561324', 'HP/03/043/021151', 'JQQ0561811', 'JQQ0561795', 'HP/03/043/021089', 'JQQ0561571', 'JQQ0561373', 'HP/03/043/021120', 'SBY0426965', 'SBY0041368', 'JQQ0561803', 'SBY0518274', 'JQQ0561258', 'JQQ0561886', 'HP/03/043/021119', 'SBY0468538', 'JQQ0632687', 'JQQ0632562', 'JQQ0421065', 'SBY0552083', 'SBY0190637', 'JQQ0574137', 'SBY0127530', 'JQQ0561878', 'JQQ0561845', 'JQQ0478610', 'HP/03/043/021123', 'SBY0507889', 'JQQ0574145', 'JQQ0561837', 'SBY0489203', 'SBY0546317', 'HP/03/043/021124', 'SBY0213215', 'HP/03/043/021092', 'SBY0213074', 'SBY0507954', 'HP/03/043/021241', 'SBY0213173', 'JQQ0561985', 'JQQ0561100', 'SBY0108936', 'JQQ0421099', 'SBY0213207', 'SBY0254839', 'JQQ0561712', 'JQQ0561936', 'JQQ0561167', 'HP/03/043/021242', 'SBY0213140', 'HP/03/043/021110', 'HP/03/043/021094', 'JQQ0632695', 'SBY0465823', 'JQQ0561949', 'HP/03/043/021132', 'HP/03/043/021004', 'SBY0213165', 'JQQ0561829', 'SBY0254847', 'HP/03/043/021007', 'SBY0317990', 'SBY0213132', 'SBY0354043', 'JQQ0574012', 'JQQ0420752', 'SBY0041376', 'SBY0263442', 'SBY0318071', 'SBY0127571', 'SBY0254813', 'JQQ0561779', 'HP/03/043/021160', 'SBY0213090', 'HP/03/043/021122', 'SBY0041343', 'JQQ0421107', 'JQQ0420760', 'SBY0127589', 'JQQ0561605', 'SBY0318063', 'JQQ0561787', 'JQQ0574004', 'HP/03/043/021104', 'HP/03/043/021199', 'HP/03/043/021121', 'HP/03/043/021229', 'SBY0213108', 'HP/03/043/021161', 'JQQ0388389', 'SBY0213082', 'SBY0440594', 'HP/03/043/021186', 'SBY0243972', 'SBY0173021', 'SBY0041350', 'JQQ0421305', 'HP/03/043/021157', 'SBY0440586', 'SBY0213124', 'HP/03/043/021085', 'HP/03/043/021084', 'SBY0353995', 'SBY0127605', 'SBY0437764', 'SBY0127654', 'HP/03/043/021158', 'SBY0127647', 'SBY0263475', 'SBY0468561', 'HP/03/043/021163', 'SBY0127613', 'SBY0127597', 'HP/03/043/021016', 'SBY0031658', 'JQQ0420844', 'HP/03/043/021227', 'SBY0483370', 'JQQ0561910', 'JQQ0421321', 'HP/03/043/021098', 'SBY0213231', 'JQQ0561589', 'HP/03/043/021136', 'SBY0041384', 'JQQ0632729', 'HP/03/043/021175', 'SBY0306316', 'SBY0127639', 'HP/03/043/021081', 'JQQ0561654', 'HP/03/043/021101', 'HP/03/043/021138', 'SBY0127662', 'SBY0244004', 'SBY0263467', 'HP/03/043/021082', 'SBY0499822', 'HP/03/043/021263', 'SBY0263459', 'JQQ0561761', 'SBY0127621', 'JQQ9902537', 'JQQ0561191', 'SBY0213223', 'HP/03/043/021135', 'HP/03/043/021076', 'JQQ0561290', 'JQQ0574152', 'HP/03/043/021083', 'HP/03/043/021176', 'HP/03/043/021147', 'HP/03/043/021037', 'JQQ0561415', 'HP/03/043/021146', 'JQQ0561753', 'HP/03/043/021145', 'SBY0537977', 'SBY0353946', 'SBY0037838', 'SBY0213314', 'JQQ0561381', 'HP/03/043/021170', 'SBY0108928', 'JQQ0632620', 'SBY0489963', 'SBY0072538', 'SBY0244012', 'SBY0245621', 'JQQ0420950', 'HP/03/043/021144', 'SBY0526079', 'JQQ0421370', 'JQQ0574194', 'JQQ0561543', 'HP/03/043/021039', 'JQQ0421388', 'HP/03/043/021152', 'HP/03/043/021148', 'JQQ0561548', 'SBY0254797', 'SBY0041210', 'JQQ0388413', 'JQQ0388397', 'JQQ0362251', 'JQQ0573998', 'SBY0342220', 'SBY0342253', 'JQQ0388355', 'JQQ0388322', 'SBY0354027', 'JQQ0561118', 'JQQ0388421', 'SBY0041186', 'HP/03/043/021020', 'SBY0437780', 'SBY0318055', 'SBY0339713', 'SBY0041202', 'HP/03/043/021005', 'JQQ0561944', 'SBY0339804', 'SBY0505362', 'SBY0041194', 'JQQ0388314', 'SBY0460543', 'JQQ0562017', 'SBY0108910', 'JQQ0420968', 'JQQ0561340', 'SBY0563593']
    
#     column_names = ["epNo", "status", "data"]
#     output_file="details_using_epicNo\Test1.csv"
#     max_parallel=30
    
#     with open(output_file, mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.DictWriter(file, fieldnames=column_names)
#         writer.writeheader()
        
#         for result in process_stream_epics(epic_stream, max_parallel):
#             writer.writerow(result)
            
#             # used to pass the data from python buffer to hard drive at sudden script crash
#             file.flush() 

#     print(f"data saved to {output_file}")
#         #     pass