import requests,json

header={"cookie":"UID=340577662_A1_1520993338; CID=7bd782f06db1a0c1bfdc9e3c8649f8a9; SEID=efedf32a6a524bccbe841261256187d4b9eb3dea56e51412b296430b56fdf1c9fd98657064ba3d480c73100ea771570c3e5dfda3d107506d8ea195fb; ssov_340577662=0_340577662_75d2767c3bda05e76faee45935cd3e75; PHPSESSID=mnfaqgdpfdn585ercosm92k4n5; Hm_lvt_44a958b429c66ae50f8bf3a9d959ccf5=1521166731; Hm_lpvt_44a958b429c66ae50f8bf3a9d959ccf5=1521181335"}
payload={"imei":"867068022329964","map":{"72":"407624556251029789"}}
r=requests.post("http://ictxl.115.com/app/1.1/ios/1.2/upload/add_map",data=payload,headers=header)
print(r.text)