import boto3

#AWS Remote Connection Setting
AWS_ID="AKIASW7332IZ4M4GPJXC"
AWS_KEY="ADjUk/V2RwtU5GI3A4+JA+3WzPt59gFZpZWGiVLW"


#Redis Connection Setting


#Mysql ConnectionSetting

Lidar1={"ip":"169.254.115.232", "port":2368, "desc":"Hesai128LineLidar", "ExpectedLength":812, "LengthFix":True, "EnableDecode":False}
Lidar2={"ip":"169.254.115.232", "port":11520, "desc":"JLR300LineLidar", "ExpectedLength":1300, "LengthFix":True, "EnableDecode":False}
Radar={"ip":"169.254.115.232", "port":1004, "desc":"DelphiRadar", "ExpectedLength":1300, "LengthFix":False, "EnableDecode":False}