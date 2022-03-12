from sqlalchemy.orm import Session

def ILSPData2DB(req_info, db_EQDAILY):
    tblname = req_info["EQ"]

    insertColumnStr = ', '.join([("`" + _ + "`") for _ in [
        "MEAS_DTTM", "DATA_GROUP", "STATUS", "VAL_1", "USL_1", 
        "UCL_1", "TARGET_1", "LCL_1", "LSL_1", "VAL_2", 
        "USL_2", "UCL_2", "TARGET_2", "LCL_2", "LSL_2"
    ]])

    req_info["STATUS"] = ""
    req_info["STATUS"] = 0
    statusDict = {0:"ERR", 1:"OK", 2:"OOC", 3:"OOS"}
    for val_1, usl_1, ucl_1, lcl_1, lsl_1, val_2, usl_2, ucl_2, lcl_2, lsl_2 \
        in zip(req_info["VAL_1"].split(","), req_info["USL_1"].split(","), req_info["UCL_1"].split(","), \
            req_info["LCL_1"].split(","), req_info["LSL_1"].split(","), \
            req_info["VAL_2"].split(","), req_info["USL_2"].split(","), req_info["UCL_2"].split(","), \
            req_info["LCL_2"].split(","), req_info["LSL_2"].split(",")):
        tmpStatus = 0
        # OOS
        if float(val_1) < float(lsl_1) or float(val_1) > float(usl_1) or float(val_2) < float(lsl_2) or float(val_2) > float(usl_2):
            tmpStatus = 3
        # OOC
        elif float(val_1) < float(lcl_1) or float(val_1) > float(ucl_1) or float(val_2) < float(lcl_2) or float(val_2) > float(ucl_2):
            tmpStatus = 2
        # OK
        else:
            tmpStatus = 1
        
        if req_info["STATUS"] == 0:
            req_info["STATUS"] = tmpStatus
        else:
            if req_info["STATUS"] < tmpStatus:
                req_info["STATUS"] = tmpStatus
    
    req_info["STATUS"] = statusDict.get(req_info["STATUS"])
    print(req_info["STATUS"])     
    sqlStr = f'INSERT INTO `{tblname}` ({insertColumnStr}) VALUES ' + \
        f'(\"{req_info["MEAS_DTTM"]}\",\"{req_info["DATA_GROUP"]}\",\"{req_info["STATUS"]}\"' + \
        f',\"{req_info["VAL_1"]}\",\"{req_info["UCL_1"]}\",\"{req_info["UCL_1"]}\",\"{req_info["TARGET_1"]}\",\"{req_info["LCL_1"]}\",\"{req_info["LSL_1"]}\"' + \
        f',\"{req_info["VAL_2"]}\",\"{req_info["USL_2"]}\",\"{req_info["UCL_2"]}\",\"{req_info["TARGET_2"]}\",\"{req_info["LCL_2"]}\",\"{req_info["LSL_2"]}\")' + \
        f' ON DUPLICATE KEY UPDATE ' + \
        f'`STATUS`="{req_info["STATUS"]}",' + \
        f'`VAL_1`="{req_info["VAL_1"]}",' + \
        f'`USL_1`="{req_info["USL_1"]}",' + \
        f'`UCL_1`="{req_info["UCL_1"]}",' + \
        f'`TARGET_1`="{req_info["TARGET_1"]}",' + \
        f'`LCL_1`="{req_info["LCL_1"]}",' + \
        f'`LSL_1`="{req_info["LSL_1"]}",' + \
        f'`VAL_2`="{req_info["VAL_1"]}",' + \
        f'`USL_2`="{req_info["USL_1"]}",' + \
        f'`UCL_2`="{req_info["UCL_1"]}",' + \
        f'`TARGET_2`="{req_info["TARGET_1"]}",' + \
        f'`LCL_2`="{req_info["LCL_1"]}",' + \
        f'`LSL_2`="{req_info["LSL_1"]}"'
    
    db_EQDAILY.execute(sqlStr)
    db_EQDAILY.commit()

    sqlStr = f'INSERT INTO `STAT_SUM` (`EQPT_ID`, `DATA_GROUP`, `MEAS_DTTM`, `STATUS`) VALUES ' + \
        f'("{tblname}","{req_info["DATA_GROUP"]}","{req_info["MEAS_DTTM"]}","{req_info["STATUS"]}")' + \
        f' ON DUPLICATE KEY UPDATE `STATUS`="{req_info["STATUS"]}",`MEAS_DTTM`="{req_info["MEAS_DTTM"]}"'
    print(sqlStr)
    db_EQDAILY.execute(sqlStr)
    db_EQDAILY.commit()

def SPMEData2DB(req_info, db_EQDAILY):
    tblname = req_info["EQ"]

    req_info["STATUS"] = ""
    req_info["STATUS"] = 0
    statusDict = {0:"ERR", 1:"OK", 2:"OOC", 3:"OOS"}
    if req_info["EQ"] == "SPME05":
        if req_info["DATA_GROUP"] == "COLOR":
            if req_info.get("TRANS", "") == "":
                insertColumnStr = ', '.join([("`" + _ + "`") for _ in [
                    "MEAS_DTTM", "GLASS_ID", "DATA_GROUP", "STATUS", "VAL_RbY", 
                    "USL_RbY", "UCL_RbY", "TARGET_RbY", "LCL_RbY", "LSL_RbY", 
                    "VAL_Rsx", "USL_Rsx", "UCL_Rsx", "TARGET_Rsx", "LCL_Rsx", 
                    "LSL_Rsx", "VAL_Rsy", "USL_Rsy", "UCL_Rsy", "TARGET_Rsy", 
                    "LCL_Rsy", "LSL_Rsy", "VAL_GbY", "USL_GbY", "UCL_GbY", 
                    "TARGET_GbY", "LCL_GbY", "LSL_GbY", "VAL_Gsx", "USL_Gsx", 
                    "UCL_Gsx", "TARGET_Gsx", "LCL_Gsx", "LSL_Gsx", "VAL_Gsy", 
                    "USL_Gsy", "UCL_Gsy", "TARGET_Gsy", "LCL_Gsy", "LSL_Gsy", 
                    "VAL_BbY", "USL_BbY", "UCL_BbY", "TARGET_BbY", "LCL_BbY", 
                    "LSL_BbY", "VAL_Bsx", "USL_Bsx", "UCL_Bsx", "TARGET_Bsx", 
                    "LCL_Bsx", "LSL_Bsx", "VAL_Bsy", "USL_Bsy", "UCL_Bsy", 
                    "TARGET_Bsy", "LCL_Bsy", "LSL_Bsy", "VAL_WbY", "USL_WbY", 
                    "UCL_WbY", "TARGET_WbY", "LCL_WbY", "LSL_WbY", "VAL_Wsx", 
                    "USL_Wsx", "UCL_Wsx", "TARGET_Wsx", "LCL_Wsx", "LSL_Wsx", 
                    "VAL_Wsy", "USL_Wsy", "UCL_Wsy", "TARGET_Wsy", "LCL_Wsy", 
                    "LSL_Wsy"
                ]])
                for tmpColor in ["R", "G", "B", "W"]:
                    for tmpItem in ["bY", "sx", "sy"]:
                        for val, usl, ucl, lcl, lsl, \
                            in zip(req_info[tmpColor][tmpItem]["VAL"].split(","), 
                                    req_info[tmpColor][tmpItem]["USL"].split(","), 
                                    req_info[tmpColor][tmpItem]["UCL"].split(","), 
                                    req_info[tmpColor][tmpItem]["LCL"].split(","), 
                                    req_info[tmpColor][tmpItem]["LSL"].split(",")
                                ):
                            tmpStatus = 0
                            # OOS
                            if float(val) < float(lsl) or float(val) > float(usl):
                                tmpStatus = 3
                            # OOC
                            elif float(val) < float(lcl) or float(val) > float(ucl):
                                tmpStatus = 2
                            # OK
                            else:
                                tmpStatus = 1
                            
                            if req_info["STATUS"] == 0:
                                req_info["STATUS"] = tmpStatus
                            else:
                                if req_info["STATUS"] < tmpStatus:
                                    req_info["STATUS"] = tmpStatus
            
                req_info["STATUS"] = statusDict.get(req_info["STATUS"])
                sqlStr = f'INSERT INTO `{tblname}` ({insertColumnStr}) VALUES ' + \
                    f'(\"{req_info["MEAS_DTTM"]}\",\"{req_info["GLASS_ID"]}\",\"{req_info["DATA_GROUP"]}\",\"{req_info["STATUS"]}\"' + \
                    f',\"{req_info["R"]["bY"]["VAL"]}\",\"{req_info["R"]["bY"]["USL"]}\",\"{req_info["R"]["bY"]["UCL"]}\",\"{req_info["R"]["bY"]["TARGET"]}\",\"{req_info["R"]["bY"]["LCL"]}\",\"{req_info["R"]["bY"]["LSL"]}\"' + \
                    f',\"{req_info["R"]["sx"]["VAL"]}\",\"{req_info["R"]["sx"]["USL"]}\",\"{req_info["R"]["sx"]["UCL"]}\",\"{req_info["R"]["sx"]["TARGET"]}\",\"{req_info["R"]["sx"]["LCL"]}\",\"{req_info["R"]["sx"]["LSL"]}\"' + \
                    f',\"{req_info["R"]["sy"]["VAL"]}\",\"{req_info["R"]["sy"]["USL"]}\",\"{req_info["R"]["sy"]["UCL"]}\",\"{req_info["R"]["sy"]["TARGET"]}\",\"{req_info["R"]["sy"]["LCL"]}\",\"{req_info["R"]["sy"]["LSL"]}\"' + \
                    f',\"{req_info["G"]["bY"]["VAL"]}\",\"{req_info["G"]["bY"]["USL"]}\",\"{req_info["G"]["bY"]["UCL"]}\",\"{req_info["G"]["bY"]["TARGET"]}\",\"{req_info["G"]["bY"]["LCL"]}\",\"{req_info["G"]["bY"]["LSL"]}\"' + \
                    f',\"{req_info["G"]["sx"]["VAL"]}\",\"{req_info["G"]["sx"]["USL"]}\",\"{req_info["G"]["sx"]["UCL"]}\",\"{req_info["G"]["sx"]["TARGET"]}\",\"{req_info["G"]["sx"]["LCL"]}\",\"{req_info["G"]["sx"]["LSL"]}\"' + \
                    f',\"{req_info["G"]["sy"]["VAL"]}\",\"{req_info["G"]["sy"]["USL"]}\",\"{req_info["G"]["sy"]["UCL"]}\",\"{req_info["G"]["sy"]["TARGET"]}\",\"{req_info["G"]["sy"]["LCL"]}\",\"{req_info["G"]["sy"]["LSL"]}\"' + \
                    f',\"{req_info["B"]["bY"]["VAL"]}\",\"{req_info["B"]["bY"]["USL"]}\",\"{req_info["B"]["bY"]["UCL"]}\",\"{req_info["B"]["bY"]["TARGET"]}\",\"{req_info["B"]["bY"]["LCL"]}\",\"{req_info["B"]["bY"]["LSL"]}\"' + \
                    f',\"{req_info["B"]["sx"]["VAL"]}\",\"{req_info["B"]["sx"]["USL"]}\",\"{req_info["B"]["sx"]["UCL"]}\",\"{req_info["B"]["sx"]["TARGET"]}\",\"{req_info["B"]["sx"]["LCL"]}\",\"{req_info["B"]["sx"]["LSL"]}\"' + \
                    f',\"{req_info["B"]["sy"]["VAL"]}\",\"{req_info["B"]["sy"]["USL"]}\",\"{req_info["B"]["sy"]["UCL"]}\",\"{req_info["B"]["sy"]["TARGET"]}\",\"{req_info["B"]["sy"]["LCL"]}\",\"{req_info["B"]["sy"]["LSL"]}\"' + \
                    f',\"{req_info["W"]["bY"]["VAL"]}\",\"{req_info["W"]["bY"]["USL"]}\",\"{req_info["W"]["bY"]["UCL"]}\",\"{req_info["W"]["bY"]["TARGET"]}\",\"{req_info["W"]["bY"]["LCL"]}\",\"{req_info["W"]["bY"]["LSL"]}\"' + \
                    f',\"{req_info["W"]["sx"]["VAL"]}\",\"{req_info["W"]["sx"]["USL"]}\",\"{req_info["W"]["sx"]["UCL"]}\",\"{req_info["W"]["sx"]["TARGET"]}\",\"{req_info["W"]["sx"]["LCL"]}\",\"{req_info["W"]["sx"]["LSL"]}\"' + \
                    f',\"{req_info["W"]["sy"]["VAL"]}\",\"{req_info["W"]["sy"]["USL"]}\",\"{req_info["W"]["sy"]["UCL"]}\",\"{req_info["W"]["sy"]["TARGET"]}\",\"{req_info["W"]["sy"]["LCL"]}\",\"{req_info["W"]["sy"]["LSL"]}\")' + \
                    f' ON DUPLICATE KEY UPDATE ' + \
                    f'`STATUS`="{req_info["STATUS"]}",' + \
                    f'`VAL_RbY`="{req_info["R"]["bY"]["VAL"]}",' + \
                    f'`USL_RbY`="{req_info["R"]["bY"]["USL"]}",' + \
                    f'`UCL_RbY`="{req_info["R"]["bY"]["UCL"]}",' + \
                    f'`TARGET_RbY`="{req_info["R"]["bY"]["TARGET"]}",' + \
                    f'`LCL_RbY`="{req_info["R"]["bY"]["LCL"]}",' + \
                    f'`LSL_RbY`="{req_info["R"]["bY"]["LSL"]}",' + \
                    f'`VAL_Rsx`="{req_info["R"]["sx"]["VAL"]}",' + \
                    f'`USL_Rsx`="{req_info["R"]["sx"]["USL"]}",' + \
                    f'`UCL_Rsx`="{req_info["R"]["sx"]["UCL"]}",' + \
                    f'`TARGET_Rsx`="{req_info["R"]["sx"]["TARGET"]}",' + \
                    f'`LCL_Rsx`="{req_info["R"]["sx"]["LCL"]}",' + \
                    f'`LSL_Rsx`="{req_info["R"]["sx"]["LSL"]}",' + \
                    f'`VAL_Rsy`="{req_info["R"]["sy"]["VAL"]}",' + \
                    f'`USL_Rsy`="{req_info["R"]["sy"]["USL"]}",' + \
                    f'`UCL_Rsy`="{req_info["R"]["sy"]["UCL"]}",' + \
                    f'`TARGET_Rsy`="{req_info["R"]["sy"]["TARGET"]}",' + \
                    f'`LCL_Rsy`="{req_info["R"]["sy"]["LCL"]}",' + \
                    f'`LSL_Rsy`="{req_info["R"]["sy"]["LSL"]}",' + \
                    f'`VAL_GbY`="{req_info["G"]["bY"]["VAL"]}",' + \
                    f'`USL_GbY`="{req_info["G"]["bY"]["USL"]}",' + \
                    f'`UCL_GbY`="{req_info["G"]["bY"]["UCL"]}",' + \
                    f'`TARGET_GbY`="{req_info["G"]["bY"]["TARGET"]}",' + \
                    f'`LCL_GbY`="{req_info["G"]["bY"]["LCL"]}",' + \
                    f'`LSL_GbY`="{req_info["G"]["bY"]["LSL"]}",' + \
                    f'`VAL_Gsx`="{req_info["G"]["sx"]["VAL"]}",' + \
                    f'`USL_Gsx`="{req_info["G"]["sx"]["USL"]}",' + \
                    f'`UCL_Gsx`="{req_info["G"]["sx"]["UCL"]}",' + \
                    f'`TARGET_Gsx`="{req_info["G"]["sx"]["TARGET"]}",' + \
                    f'`LCL_Gsx`="{req_info["G"]["sx"]["LCL"]}",' + \
                    f'`LSL_Gsx`="{req_info["G"]["sx"]["LSL"]}",' + \
                    f'`VAL_Gsy`="{req_info["G"]["sy"]["VAL"]}",' + \
                    f'`USL_Gsy`="{req_info["G"]["sy"]["USL"]}",' + \
                    f'`UCL_Gsy`="{req_info["G"]["sy"]["UCL"]}",' + \
                    f'`TARGET_Gsy`="{req_info["G"]["sy"]["TARGET"]}",' + \
                    f'`LCL_Gsy`="{req_info["G"]["sy"]["LCL"]}",' + \
                    f'`LSL_Gsy`="{req_info["G"]["sy"]["LSL"]}",' + \
                    f'`VAL_BbY`="{req_info["B"]["bY"]["VAL"]}",' + \
                    f'`USL_BbY`="{req_info["B"]["bY"]["USL"]}",' + \
                    f'`UCL_BbY`="{req_info["B"]["bY"]["UCL"]}",' + \
                    f'`TARGET_BbY`="{req_info["B"]["bY"]["TARGET"]}",' + \
                    f'`LCL_BbY`="{req_info["B"]["bY"]["LCL"]}",' + \
                    f'`LSL_BbY`="{req_info["B"]["bY"]["LSL"]}",' + \
                    f'`VAL_Bsx`="{req_info["B"]["sx"]["VAL"]}",' + \
                    f'`USL_Bsx`="{req_info["B"]["sx"]["USL"]}",' + \
                    f'`UCL_Bsx`="{req_info["B"]["sx"]["UCL"]}",' + \
                    f'`TARGET_Bsx`="{req_info["B"]["sx"]["TARGET"]}",' + \
                    f'`LCL_Bsx`="{req_info["B"]["sx"]["LCL"]}",' + \
                    f'`LSL_Bsx`="{req_info["B"]["sx"]["LSL"]}",' + \
                    f'`VAL_Bsy`="{req_info["B"]["sy"]["VAL"]}",' + \
                    f'`USL_Bsy`="{req_info["B"]["sy"]["USL"]}",' + \
                    f'`UCL_Bsy`="{req_info["B"]["sy"]["UCL"]}",' + \
                    f'`TARGET_Bsy`="{req_info["B"]["sy"]["TARGET"]}",' + \
                    f'`LCL_Bsy`="{req_info["B"]["sy"]["LCL"]}",' + \
                    f'`LSL_Bsy`="{req_info["B"]["sy"]["LSL"]}",' + \
                    f'`VAL_WbY`="{req_info["W"]["bY"]["VAL"]}",' + \
                    f'`USL_WbY`="{req_info["W"]["bY"]["USL"]}",' + \
                    f'`UCL_WbY`="{req_info["W"]["bY"]["UCL"]}",' + \
                    f'`TARGET_WbY`="{req_info["W"]["bY"]["TARGET"]}",' + \
                    f'`LCL_WbY`="{req_info["W"]["bY"]["LCL"]}",' + \
                    f'`LSL_WbY`="{req_info["W"]["bY"]["LSL"]}",' + \
                    f'`VAL_Wsx`="{req_info["W"]["sx"]["VAL"]}",' + \
                    f'`USL_Wsx`="{req_info["W"]["sx"]["USL"]}",' + \
                    f'`UCL_Wsx`="{req_info["W"]["sx"]["UCL"]}",' + \
                    f'`TARGET_Wsx`="{req_info["W"]["sx"]["TARGET"]}",' + \
                    f'`LCL_Wsx`="{req_info["W"]["sx"]["LCL"]}",' + \
                    f'`LSL_Wsx`="{req_info["W"]["sx"]["LSL"]}",' + \
                    f'`VAL_Wsy`="{req_info["W"]["sy"]["VAL"]}",' + \
                    f'`USL_Wsy`="{req_info["W"]["sy"]["USL"]}",' + \
                    f'`UCL_Wsy`="{req_info["W"]["sy"]["UCL"]}",' + \
                    f'`TARGET_Wsy`="{req_info["W"]["sy"]["TARGET"]}",' + \
                    f'`LCL_Wsy`="{req_info["W"]["sy"]["LCL"]}",' + \
                    f'`LSL_Wsy`="{req_info["W"]["sy"]["LSL"]}"'
                print(sqlStr)
                db_EQDAILY.execute(sqlStr)

                sqlStr = f'INSERT INTO `STAT_SUM` (`EQPT_ID`, `DATA_GROUP`, `MEAS_DTTM`, `STATUS`) VALUES ' + \
                f'("{tblname}","COLOR","{req_info["MEAS_DTTM"]}","{req_info["STATUS"]}")' + \
                f' ON DUPLICATE KEY UPDATE `STATUS`="{req_info["STATUS"]}",`MEAS_DTTM`="{req_info["MEAS_DTTM"]}"'
                print(sqlStr)
                db_EQDAILY.execute(sqlStr)
            else:
                insertColumnStr = ', '.join([("`" + _ + "`") for _ in [
                    "MEAS_DTTM", "GLASS_ID", "DATA_GROUP", "STATUS", "VAL_TRANS", 
                    "USL_TRANS", "UCL_TRANS", "TARGET_TRANS", "LCL_TRANS", "LSL_TRANS"
                ]])
            
                req_info["STATUS"] = ""
                req_info["STATUS"] = 0
                for val, usl, ucl, lcl, lsl, \
                    in zip(req_info["TRANS"]["VAL"].split(","), 
                            req_info["TRANS"]["USL"].split(","), 
                            req_info["TRANS"]["UCL"].split(","), 
                            req_info["TRANS"]["LCL"].split(","), 
                            req_info["TRANS"]["LSL"].split(",")
                        ):
                    tmpStatus = 0
                    # OOS
                    if float(val) < float(lsl) or float(val) > float(usl):
                        tmpStatus = 3
                    # OOC
                    elif float(val) < float(lcl) or float(val) > float(ucl):
                        tmpStatus = 2
                    # OK
                    else:
                        tmpStatus = 1
                    
                    if req_info["STATUS"] == 0:
                        req_info["STATUS"] = tmpStatus
                    else:
                        if req_info["STATUS"] < tmpStatus:
                            req_info["STATUS"] = tmpStatus
            
                req_info["STATUS"] = statusDict.get(req_info["STATUS"])
                sqlStr = f'INSERT INTO `{tblname}` ({insertColumnStr}) VALUES ' + \
                    f'(\"{req_info["MEAS_DTTM"]}\",\"{req_info["GLASS_ID"]}\",\"TRANS\",\"{req_info["STATUS"]}\"' + \
                    f',\"{req_info["TRANS"]["VAL"]}\",\"{req_info["TRANS"]["USL"]}\",\"{req_info["TRANS"]["UCL"]}\",\"{req_info["TRANS"]["TARGET"]}\",\"{req_info["TRANS"]["LCL"]}\",\"{req_info["TRANS"]["LSL"]}\")' + \
                    f' ON DUPLICATE KEY UPDATE ' + \
                    f'`STATUS`="{req_info["STATUS"]}",' + \
                    f'`VAL_TRANS`="{req_info["TRANS"]["VAL"]}",' + \
                    f'`USL_TRANS`="{req_info["TRANS"]["USL"]}",' + \
                    f'`UCL_TRANS`="{req_info["TRANS"]["UCL"]}",' + \
                    f'`TARGET_TRANS`="{req_info["TRANS"]["TARGET"]}",' + \
                    f'`LCL_TRANS`="{req_info["TRANS"]["LCL"]}",' + \
                    f'`LSL_TRANS`="{req_info["TRANS"]["LSL"]}"'
                print(sqlStr)
                db_EQDAILY.execute(sqlStr)

                sqlStr = f'INSERT INTO `STAT_SUM` (`EQPT_ID`, `DATA_GROUP`, `MEAS_DTTM`, `STATUS`) VALUES ' + \
                f'("{tblname}","TRANS","{req_info["MEAS_DTTM"]}","{req_info["STATUS"]}")' + \
                f' ON DUPLICATE KEY UPDATE `STATUS`="{req_info["STATUS"]}",`MEAS_DTTM`="{req_info["MEAS_DTTM"]}"'
                print(sqlStr)
                db_EQDAILY.execute(sqlStr)
        elif req_info["DATA_GROUP"] == "OD":
            insertColumnStr = ', '.join([("`" + _ + "`") for _ in [
                "MEAS_DTTM", "GLASS_ID", "DATA_GROUP", "STATUS", "VAL_OD", 
                "USL_OD", "UCL_OD", "TARGET_OD", "LCL_OD", "LSL_OD",
            ]])
            for val, usl, ucl, lcl, lsl, \
                in zip(req_info["OD"]["VAL"].split(","), 
                        req_info["OD"]["USL"].split(","), 
                        req_info["OD"]["UCL"].split(","), 
                        req_info["OD"]["LCL"].split(","), 
                        req_info["OD"]["LSL"].split(",")
                    ):
                tmpStatus = 0
                # OOS
                if float(val) < float(lsl) or float(val) > float(usl):
                    tmpStatus = 3
                # OOC
                elif float(val) < float(lcl) or float(val) > float(ucl):
                    tmpStatus = 2
                # OK
                else:
                    tmpStatus = 1
                
                if req_info["STATUS"] == 0:
                    req_info["STATUS"] = tmpStatus
                else:
                    if req_info["STATUS"] < tmpStatus:
                        req_info["STATUS"] = tmpStatus
        
            req_info["STATUS"] = statusDict.get(req_info["STATUS"])
            sqlStr = f'INSERT INTO `{tblname}` ({insertColumnStr}) VALUES ' + \
                f'(\"{req_info["MEAS_DTTM"]}\",\"{req_info["GLASS_ID"]}\",\"{req_info["DATA_GROUP"]}\",\"{req_info["STATUS"]}\"' + \
                f',\"{req_info["OD"]["VAL"]}\",\"{req_info["OD"]["USL"]}\",\"{req_info["OD"]["UCL"]}\",\"{req_info["OD"]["TARGET"]}\",\"{req_info["OD"]["LCL"]}\",\"{req_info["OD"]["LSL"]}\")' + \
                f' ON DUPLICATE KEY UPDATE ' + \
                f'`STATUS`="{req_info["STATUS"]}",' + \
                f'`VAL_OD`="{req_info["OD"]["VAL"]}",' + \
                f'`USL_OD`="{req_info["OD"]["USL"]}",' + \
                f'`UCL_OD`="{req_info["OD"]["UCL"]}",' + \
                f'`TARGET_OD`="{req_info["OD"]["TARGET"]}",' + \
                f'`LCL_OD`="{req_info["OD"]["LCL"]}",' + \
                f'`LSL_OD`="{req_info["OD"]["LSL"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)

            sqlStr = f'INSERT INTO `STAT_SUM` (`EQPT_ID`, `DATA_GROUP`, `MEAS_DTTM`, `STATUS`) VALUES ' + \
            f'("{tblname}","{req_info["DATA_GROUP"]}","{req_info["MEAS_DTTM"]}","{req_info["STATUS"]}")' + \
            f' ON DUPLICATE KEY UPDATE `STATUS`="{req_info["STATUS"]}",`MEAS_DTTM`="{req_info["MEAS_DTTM"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)
    else:
        if req_info["DATA_GROUP"] == "COLOR":
            insertColumnStr = ', '.join([("`" + _ + "`") for _ in [
                    "MEAS_DTTM", "GLASS_ID", "DATA_GROUP", "STATUS", "VAL_RbY", 
                    "USL_RbY", "UCL_RbY", "TARGET_RbY", "LCL_RbY", "LSL_RbY", 
                    "VAL_Rsx", "USL_Rsx", "UCL_Rsx", "TARGET_Rsx", "LCL_Rsx", 
                    "LSL_Rsx", "VAL_Rsy", "USL_Rsy", "UCL_Rsy", "TARGET_Rsy", 
                    "LCL_Rsy", "LSL_Rsy", "VAL_GbY", "USL_GbY", "UCL_GbY", 
                    "TARGET_GbY", "LCL_GbY", "LSL_GbY", "VAL_Gsx", "USL_Gsx", 
                    "UCL_Gsx", "TARGET_Gsx", "LCL_Gsx", "LSL_Gsx", "VAL_Gsy", 
                    "USL_Gsy", "UCL_Gsy", "TARGET_Gsy", "LCL_Gsy", "LSL_Gsy", 
                    "VAL_BbY", "USL_BbY", "UCL_BbY", "TARGET_BbY", "LCL_BbY", 
                    "LSL_BbY", "VAL_Bsx", "USL_Bsx", "UCL_Bsx", "TARGET_Bsx", 
                    "LCL_Bsx", "LSL_Bsx", "VAL_Bsy", "USL_Bsy", "UCL_Bsy", 
                    "TARGET_Bsy", "LCL_Bsy", "LSL_Bsy", "VAL_WbY", "USL_WbY", 
                    "UCL_WbY", "TARGET_WbY", "LCL_WbY", "LSL_WbY", "VAL_Wsx", 
                    "USL_Wsx", "UCL_Wsx", "TARGET_Wsx", "LCL_Wsx", "LSL_Wsx", 
                    "VAL_Wsy", "USL_Wsy", "UCL_Wsy", "TARGET_Wsy", "LCL_Wsy", 
                    "LSL_Wsy"
                ]])
            for tmpColor in ["R", "G", "B", "W"]:
                for tmpItem in ["bY", "sx", "sy"]:
                    for val, usl, ucl, lcl, lsl, \
                        in zip(req_info[tmpColor][tmpItem]["VAL"].split(","), 
                                req_info[tmpColor][tmpItem]["USL"].split(","), 
                                req_info[tmpColor][tmpItem]["UCL"].split(","), 
                                req_info[tmpColor][tmpItem]["LCL"].split(","), 
                                req_info[tmpColor][tmpItem]["LSL"].split(",")
                            ):
                        tmpStatus = 0
                        # OOS
                        if float(val) < float(lsl) or float(val) > float(usl):
                            tmpStatus = 3
                        # OOC
                        elif float(val) < float(lcl) or float(val) > float(ucl):
                            tmpStatus = 2
                        # OK
                        else:
                            tmpStatus = 1
                        
                        if req_info["STATUS"] == 0:
                            req_info["STATUS"] = tmpStatus
                        else:
                            if req_info["STATUS"] < tmpStatus:
                                req_info["STATUS"] = tmpStatus
        
            req_info["STATUS"] = statusDict.get(req_info["STATUS"])
            sqlStr = f'INSERT INTO `{tblname}` ({insertColumnStr}) VALUES ' + \
                f'(\"{req_info["MEAS_DTTM"]}\",\"{req_info["GLASS_ID"]}\",\"{req_info["DATA_GROUP"]}\",\"{req_info["STATUS"]}\"' + \
                f',\"{req_info["R"]["bY"]["VAL"]}\",\"{req_info["R"]["bY"]["USL"]}\",\"{req_info["R"]["bY"]["UCL"]}\",\"{req_info["R"]["bY"]["TARGET"]}\",\"{req_info["R"]["bY"]["LCL"]}\",\"{req_info["R"]["bY"]["LSL"]}\"' + \
                f',\"{req_info["R"]["sx"]["VAL"]}\",\"{req_info["R"]["sx"]["USL"]}\",\"{req_info["R"]["sx"]["UCL"]}\",\"{req_info["R"]["sx"]["TARGET"]}\",\"{req_info["R"]["sx"]["LCL"]}\",\"{req_info["R"]["sx"]["LSL"]}\"' + \
                f',\"{req_info["R"]["sy"]["VAL"]}\",\"{req_info["R"]["sy"]["USL"]}\",\"{req_info["R"]["sy"]["UCL"]}\",\"{req_info["R"]["sy"]["TARGET"]}\",\"{req_info["R"]["sy"]["LCL"]}\",\"{req_info["R"]["sy"]["LSL"]}\"' + \
                f',\"{req_info["G"]["bY"]["VAL"]}\",\"{req_info["G"]["bY"]["USL"]}\",\"{req_info["G"]["bY"]["UCL"]}\",\"{req_info["G"]["bY"]["TARGET"]}\",\"{req_info["G"]["bY"]["LCL"]}\",\"{req_info["G"]["bY"]["LSL"]}\"' + \
                f',\"{req_info["G"]["sx"]["VAL"]}\",\"{req_info["G"]["sx"]["USL"]}\",\"{req_info["G"]["sx"]["UCL"]}\",\"{req_info["G"]["sx"]["TARGET"]}\",\"{req_info["G"]["sx"]["LCL"]}\",\"{req_info["G"]["sx"]["LSL"]}\"' + \
                f',\"{req_info["G"]["sy"]["VAL"]}\",\"{req_info["G"]["sy"]["USL"]}\",\"{req_info["G"]["sy"]["UCL"]}\",\"{req_info["G"]["sy"]["TARGET"]}\",\"{req_info["G"]["sy"]["LCL"]}\",\"{req_info["G"]["sy"]["LSL"]}\"' + \
                f',\"{req_info["B"]["bY"]["VAL"]}\",\"{req_info["B"]["bY"]["USL"]}\",\"{req_info["B"]["bY"]["UCL"]}\",\"{req_info["B"]["bY"]["TARGET"]}\",\"{req_info["B"]["bY"]["LCL"]}\",\"{req_info["B"]["bY"]["LSL"]}\"' + \
                f',\"{req_info["B"]["sx"]["VAL"]}\",\"{req_info["B"]["sx"]["USL"]}\",\"{req_info["B"]["sx"]["UCL"]}\",\"{req_info["B"]["sx"]["TARGET"]}\",\"{req_info["B"]["sx"]["LCL"]}\",\"{req_info["B"]["sx"]["LSL"]}\"' + \
                f',\"{req_info["B"]["sy"]["VAL"]}\",\"{req_info["B"]["sy"]["USL"]}\",\"{req_info["B"]["sy"]["UCL"]}\",\"{req_info["B"]["sy"]["TARGET"]}\",\"{req_info["B"]["sy"]["LCL"]}\",\"{req_info["B"]["sy"]["LSL"]}\"' + \
                f',\"{req_info["W"]["bY"]["VAL"]}\",\"{req_info["W"]["bY"]["USL"]}\",\"{req_info["W"]["bY"]["UCL"]}\",\"{req_info["W"]["bY"]["TARGET"]}\",\"{req_info["W"]["bY"]["LCL"]}\",\"{req_info["W"]["bY"]["LSL"]}\"' + \
                f',\"{req_info["W"]["sx"]["VAL"]}\",\"{req_info["W"]["sx"]["USL"]}\",\"{req_info["W"]["sx"]["UCL"]}\",\"{req_info["W"]["sx"]["TARGET"]}\",\"{req_info["W"]["sx"]["LCL"]}\",\"{req_info["W"]["sx"]["LSL"]}\"' + \
                f',\"{req_info["W"]["sy"]["VAL"]}\",\"{req_info["W"]["sy"]["USL"]}\",\"{req_info["W"]["sy"]["UCL"]}\",\"{req_info["W"]["sy"]["TARGET"]}\",\"{req_info["W"]["sy"]["LCL"]}\",\"{req_info["W"]["sy"]["LSL"]}\")' + \
                f' ON DUPLICATE KEY UPDATE ' + \
                f'`STATUS`="{req_info["STATUS"]}",' + \
                f'`VAL_RbY`="{req_info["R"]["bY"]["VAL"]}",' + \
                f'`USL_RbY`="{req_info["R"]["bY"]["USL"]}",' + \
                f'`UCL_RbY`="{req_info["R"]["bY"]["UCL"]}",' + \
                f'`TARGET_RbY`="{req_info["R"]["bY"]["TARGET"]}",' + \
                f'`LCL_RbY`="{req_info["R"]["bY"]["LCL"]}",' + \
                f'`LSL_RbY`="{req_info["R"]["bY"]["LSL"]}",' + \
                f'`VAL_Rsx`="{req_info["R"]["sx"]["VAL"]}",' + \
                f'`USL_Rsx`="{req_info["R"]["sx"]["USL"]}",' + \
                f'`UCL_Rsx`="{req_info["R"]["sx"]["UCL"]}",' + \
                f'`TARGET_Rsx`="{req_info["R"]["sx"]["TARGET"]}",' + \
                f'`LCL_Rsx`="{req_info["R"]["sx"]["LCL"]}",' + \
                f'`LSL_Rsx`="{req_info["R"]["sx"]["LSL"]}",' + \
                f'`VAL_Rsy`="{req_info["R"]["sy"]["VAL"]}",' + \
                f'`USL_Rsy`="{req_info["R"]["sy"]["USL"]}",' + \
                f'`UCL_Rsy`="{req_info["R"]["sy"]["UCL"]}",' + \
                f'`TARGET_Rsy`="{req_info["R"]["sy"]["TARGET"]}",' + \
                f'`LCL_Rsy`="{req_info["R"]["sy"]["LCL"]}",' + \
                f'`LSL_Rsy`="{req_info["R"]["sy"]["LSL"]}",' + \
                f'`VAL_GbY`="{req_info["G"]["bY"]["VAL"]}",' + \
                f'`USL_GbY`="{req_info["G"]["bY"]["USL"]}",' + \
                f'`UCL_GbY`="{req_info["G"]["bY"]["UCL"]}",' + \
                f'`TARGET_GbY`="{req_info["G"]["bY"]["TARGET"]}",' + \
                f'`LCL_GbY`="{req_info["G"]["bY"]["LCL"]}",' + \
                f'`LSL_GbY`="{req_info["G"]["bY"]["LSL"]}",' + \
                f'`VAL_Gsx`="{req_info["G"]["sx"]["VAL"]}",' + \
                f'`USL_Gsx`="{req_info["G"]["sx"]["USL"]}",' + \
                f'`UCL_Gsx`="{req_info["G"]["sx"]["UCL"]}",' + \
                f'`TARGET_Gsx`="{req_info["G"]["sx"]["TARGET"]}",' + \
                f'`LCL_Gsx`="{req_info["G"]["sx"]["LCL"]}",' + \
                f'`LSL_Gsx`="{req_info["G"]["sx"]["LSL"]}",' + \
                f'`VAL_Gsy`="{req_info["G"]["sy"]["VAL"]}",' + \
                f'`USL_Gsy`="{req_info["G"]["sy"]["USL"]}",' + \
                f'`UCL_Gsy`="{req_info["G"]["sy"]["UCL"]}",' + \
                f'`TARGET_Gsy`="{req_info["G"]["sy"]["TARGET"]}",' + \
                f'`LCL_Gsy`="{req_info["G"]["sy"]["LCL"]}",' + \
                f'`LSL_Gsy`="{req_info["G"]["sy"]["LSL"]}",' + \
                f'`VAL_BbY`="{req_info["B"]["bY"]["VAL"]}",' + \
                f'`USL_BbY`="{req_info["B"]["bY"]["USL"]}",' + \
                f'`UCL_BbY`="{req_info["B"]["bY"]["UCL"]}",' + \
                f'`TARGET_BbY`="{req_info["B"]["bY"]["TARGET"]}",' + \
                f'`LCL_BbY`="{req_info["B"]["bY"]["LCL"]}",' + \
                f'`LSL_BbY`="{req_info["B"]["bY"]["LSL"]}",' + \
                f'`VAL_Bsx`="{req_info["B"]["sx"]["VAL"]}",' + \
                f'`USL_Bsx`="{req_info["B"]["sx"]["USL"]}",' + \
                f'`UCL_Bsx`="{req_info["B"]["sx"]["UCL"]}",' + \
                f'`TARGET_Bsx`="{req_info["B"]["sx"]["TARGET"]}",' + \
                f'`LCL_Bsx`="{req_info["B"]["sx"]["LCL"]}",' + \
                f'`LSL_Bsx`="{req_info["B"]["sx"]["LSL"]}",' + \
                f'`VAL_Bsy`="{req_info["B"]["sy"]["VAL"]}",' + \
                f'`USL_Bsy`="{req_info["B"]["sy"]["USL"]}",' + \
                f'`UCL_Bsy`="{req_info["B"]["sy"]["UCL"]}",' + \
                f'`TARGET_Bsy`="{req_info["B"]["sy"]["TARGET"]}",' + \
                f'`LCL_Bsy`="{req_info["B"]["sy"]["LCL"]}",' + \
                f'`LSL_Bsy`="{req_info["B"]["sy"]["LSL"]}",' + \
                f'`VAL_WbY`="{req_info["W"]["bY"]["VAL"]}",' + \
                f'`USL_WbY`="{req_info["W"]["bY"]["USL"]}",' + \
                f'`UCL_WbY`="{req_info["W"]["bY"]["UCL"]}",' + \
                f'`TARGET_WbY`="{req_info["W"]["bY"]["TARGET"]}",' + \
                f'`LCL_WbY`="{req_info["W"]["bY"]["LCL"]}",' + \
                f'`LSL_WbY`="{req_info["W"]["bY"]["LSL"]}",' + \
                f'`VAL_Wsx`="{req_info["W"]["sx"]["VAL"]}",' + \
                f'`USL_Wsx`="{req_info["W"]["sx"]["USL"]}",' + \
                f'`UCL_Wsx`="{req_info["W"]["sx"]["UCL"]}",' + \
                f'`TARGET_Wsx`="{req_info["W"]["sx"]["TARGET"]}",' + \
                f'`LCL_Wsx`="{req_info["W"]["sx"]["LCL"]}",' + \
                f'`LSL_Wsx`="{req_info["W"]["sx"]["LSL"]}",' + \
                f'`VAL_Wsy`="{req_info["W"]["sy"]["VAL"]}",' + \
                f'`USL_Wsy`="{req_info["W"]["sy"]["USL"]}",' + \
                f'`UCL_Wsy`="{req_info["W"]["sy"]["UCL"]}",' + \
                f'`TARGET_Wsy`="{req_info["W"]["sy"]["TARGET"]}",' + \
                f'`LCL_Wsy`="{req_info["W"]["sy"]["LCL"]}",' + \
                f'`LSL_Wsy`="{req_info["W"]["sy"]["LSL"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)

            sqlStr = f'INSERT INTO `STAT_SUM` (`EQPT_ID`, `DATA_GROUP`, `MEAS_DTTM`, `STATUS`) VALUES ' + \
            f'("{tblname}","COLOR","{req_info["MEAS_DTTM"]}","{req_info["STATUS"]}")' + \
            f' ON DUPLICATE KEY UPDATE `STATUS`="{req_info["STATUS"]}",`MEAS_DTTM`="{req_info["MEAS_DTTM"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)

            # TRANS
            insertColumnStr = ', '.join([("`" + _ + "`") for _ in [
                    "MEAS_DTTM", "GLASS_ID", "DATA_GROUP", "STATUS", "VAL_TRANS", 
                    "USL_TRANS", "UCL_TRANS", "TARGET_TRANS", "LCL_TRANS", "LSL_TRANS"
                ]])
            
            req_info["STATUS"] = ""
            req_info["STATUS"] = 0
            for val, usl, ucl, lcl, lsl, \
                in zip(req_info["TRANS"]["VAL"].split(","), 
                        req_info["TRANS"]["USL"].split(","), 
                        req_info["TRANS"]["UCL"].split(","), 
                        req_info["TRANS"]["LCL"].split(","), 
                        req_info["TRANS"]["LSL"].split(",")
                    ):
                tmpStatus = 0
                # OOS
                if float(val) < float(lsl) or float(val) > float(usl):
                    tmpStatus = 3
                # OOC
                elif float(val) < float(lcl) or float(val) > float(ucl):
                    tmpStatus = 2
                # OK
                else:
                    tmpStatus = 1
                
                if req_info["STATUS"] == 0:
                    req_info["STATUS"] = tmpStatus
                else:
                    if req_info["STATUS"] < tmpStatus:
                        req_info["STATUS"] = tmpStatus
        
            req_info["STATUS"] = statusDict.get(req_info["STATUS"])
            sqlStr = f'INSERT INTO `{tblname}` ({insertColumnStr}) VALUES ' + \
                f'(\"{req_info["MEAS_DTTM"]}\",\"{req_info["GLASS_ID"]}\",\"TRANS\",\"{req_info["STATUS"]}\"' + \
                f',\"{req_info["TRANS"]["VAL"]}\",\"{req_info["TRANS"]["USL"]}\",\"{req_info["TRANS"]["UCL"]}\",\"{req_info["TRANS"]["TARGET"]}\",\"{req_info["TRANS"]["LCL"]}\",\"{req_info["TRANS"]["LSL"]}\")' + \
                f' ON DUPLICATE KEY UPDATE ' + \
                f'`STATUS`="{req_info["STATUS"]}",' + \
                f'`VAL_TRANS`="{req_info["TRANS"]["VAL"]}",' + \
                f'`USL_TRANS`="{req_info["TRANS"]["USL"]}",' + \
                f'`UCL_TRANS`="{req_info["TRANS"]["UCL"]}",' + \
                f'`TARGET_TRANS`="{req_info["TRANS"]["TARGET"]}",' + \
                f'`LCL_TRANS`="{req_info["TRANS"]["LCL"]}",' + \
                f'`LSL_TRANS`="{req_info["TRANS"]["LSL"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)

            sqlStr = f'INSERT INTO `STAT_SUM` (`EQPT_ID`, `DATA_GROUP`, `MEAS_DTTM`, `STATUS`) VALUES ' + \
            f'("{tblname}","TRANS","{req_info["MEAS_DTTM"]}","{req_info["STATUS"]}")' + \
            f' ON DUPLICATE KEY UPDATE `STATUS`="{req_info["STATUS"]}",`MEAS_DTTM`="{req_info["MEAS_DTTM"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)
        
        elif req_info["DATA_GROUP"] == "Lab":
            insertColumnStr = ', '.join([("`" + _ + "`") for _ in [
                    "MEAS_DTTM", "GLASS_ID", "DATA_GROUP", "STATUS", "VAL_L*", 
                    "USL_L*", "UCL_L*", "TARGET_L*", "LCL_L*", "LSL_L*", 
                    "VAL_a*", "USL_a*", "UCL_a*", "TARGET_a*", "LCL_a*", 
                    "LSL_a*", "VAL_b*", "USL_b*", "UCL_b*", "TARGET_b*", 
                    "LCL_b*", "LSL_b*"
                ]])
            for tmpItem in ["L", "a", "b"]:
                for val, usl, ucl, lcl, lsl, \
                    in zip(req_info[tmpItem]["VAL"].split(","), 
                            req_info[tmpItem]["USL"].split(","), 
                            req_info[tmpItem]["UCL"].split(","), 
                            req_info[tmpItem]["LCL"].split(","), 
                            req_info[tmpItem]["LSL"].split(",")
                        ):
                    tmpStatus = 0
                    # OOS
                    if float(val) < float(lsl) or float(val) > float(usl):
                        tmpStatus = 3
                    # OOC
                    elif float(val) < float(lcl) or float(val) > float(ucl):
                        tmpStatus = 2
                    # OK
                    else:
                        tmpStatus = 1
                    
                    if req_info["STATUS"] == 0:
                        req_info["STATUS"] = tmpStatus
                    else:
                        if req_info["STATUS"] < tmpStatus:
                            req_info["STATUS"] = tmpStatus
        
            req_info["STATUS"] = statusDict.get(req_info["STATUS"])
            sqlStr = f'INSERT INTO `{tblname}` ({insertColumnStr}) VALUES ' + \
                f'(\"{req_info["MEAS_DTTM"]}\",\"{req_info["GLASS_ID"]}\",\"{req_info["DATA_GROUP"]}\",\"{req_info["STATUS"]}\"' + \
                f',\"{req_info["L"]["VAL"]}\",\"{req_info["L"]["USL"]}\",\"{req_info["L"]["UCL"]}\",\"{req_info["L"]["TARGET"]}\",\"{req_info["L"]["LCL"]}\",\"{req_info["L"]["LSL"]}\"' + \
                f',\"{req_info["a"]["VAL"]}\",\"{req_info["a"]["USL"]}\",\"{req_info["a"]["UCL"]}\",\"{req_info["a"]["TARGET"]}\",\"{req_info["a"]["LCL"]}\",\"{req_info["a"]["LSL"]}\"' + \
                f',\"{req_info["b"]["VAL"]}\",\"{req_info["b"]["USL"]}\",\"{req_info["b"]["UCL"]}\",\"{req_info["b"]["TARGET"]}\",\"{req_info["b"]["LCL"]}\",\"{req_info["b"]["LSL"]}\")' + \
                f' ON DUPLICATE KEY UPDATE ' + \
                f'`STATUS`="{req_info["STATUS"]}",' + \
                f'`VAL_L*`="{req_info["L"]["VAL"]}",' + \
                f'`USL_L*`="{req_info["L"]["USL"]}",' + \
                f'`UCL_L*`="{req_info["L"]["UCL"]}",' + \
                f'`TARGET_L*`="{req_info["L"]["TARGET"]}",' + \
                f'`LCL_L*`="{req_info["L"]["LCL"]}",' + \
                f'`LSL_L*`="{req_info["L"]["LSL"]}",' + \
                f'`VAL_a*`="{req_info["a"]["VAL"]}",' + \
                f'`USL_a*`="{req_info["a"]["USL"]}",' + \
                f'`UCL_a*`="{req_info["a"]["UCL"]}",' + \
                f'`TARGET_a*`="{req_info["a"]["TARGET"]}",' + \
                f'`LCL_a*`="{req_info["a"]["LCL"]}",' + \
                f'`LSL_a*`="{req_info["a"]["LSL"]}",' + \
                f'`VAL_b*`="{req_info["b"]["VAL"]}",' + \
                f'`USL_b*`="{req_info["b"]["USL"]}",' + \
                f'`UCL_b*`="{req_info["b"]["UCL"]}",' + \
                f'`TARGET_b*`="{req_info["b"]["TARGET"]}",' + \
                f'`LCL_b*`="{req_info["b"]["LCL"]}",' + \
                f'`LSL_b*`="{req_info["b"]["LSL"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)

            sqlStr = f'INSERT INTO `STAT_SUM` (`EQPT_ID`, `DATA_GROUP`, `MEAS_DTTM`, `STATUS`) VALUES ' + \
            f'("{tblname}","Lab","{req_info["MEAS_DTTM"]}","{req_info["STATUS"]}")' + \
            f' ON DUPLICATE KEY UPDATE `STATUS`="{req_info["STATUS"]}",`MEAS_DTTM`="{req_info["MEAS_DTTM"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)

        elif req_info["DATA_GROUP"] in ["OD_H", "OD_L"]:
            insertColumnStr = ', '.join([("`" + _ + "`") for _ in [
                    "MEAS_DTTM", "GLASS_ID", "DATA_GROUP", "STATUS", "VAL_OD", 
                    "USL_OD", "UCL_OD", "TARGET_OD", "LCL_OD", "LSL_OD",
                ]])
            for val, usl, ucl, lcl, lsl, \
                in zip(req_info["OD"]["VAL"].split(","), 
                        req_info["OD"]["USL"].split(","), 
                        req_info["OD"]["UCL"].split(","), 
                        req_info["OD"]["LCL"].split(","), 
                        req_info["OD"]["LSL"].split(",")
                    ):
                tmpStatus = 0
                # OOS
                if float(val) < float(lsl) or float(val) > float(usl):
                    tmpStatus = 3
                # OOC
                elif float(val) < float(lcl) or float(val) > float(ucl):
                    tmpStatus = 2
                # OK
                else:
                    tmpStatus = 1
                
                if req_info["STATUS"] == 0:
                    req_info["STATUS"] = tmpStatus
                else:
                    if req_info["STATUS"] < tmpStatus:
                        req_info["STATUS"] = tmpStatus
        
            req_info["STATUS"] = statusDict.get(req_info["STATUS"])
            sqlStr = f'INSERT INTO `{tblname}` ({insertColumnStr}) VALUES ' + \
                f'(\"{req_info["MEAS_DTTM"]}\",\"{req_info["GLASS_ID"]}\",\"{req_info["DATA_GROUP"]}\",\"{req_info["STATUS"]}\"' + \
                f',\"{req_info["OD"]["VAL"]}\",\"{req_info["OD"]["USL"]}\",\"{req_info["OD"]["UCL"]}\",\"{req_info["OD"]["TARGET"]}\",\"{req_info["OD"]["LCL"]}\",\"{req_info["OD"]["LSL"]}\")' + \
                f' ON DUPLICATE KEY UPDATE ' + \
                f'`STATUS`="{req_info["STATUS"]}",' + \
                f'`VAL_OD`="{req_info["OD"]["VAL"]}",' + \
                f'`USL_OD`="{req_info["OD"]["USL"]}",' + \
                f'`UCL_OD`="{req_info["OD"]["UCL"]}",' + \
                f'`TARGET_OD`="{req_info["OD"]["TARGET"]}",' + \
                f'`LCL_OD`="{req_info["OD"]["LCL"]}",' + \
                f'`LSL_OD`="{req_info["OD"]["LSL"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)

            sqlStr = f'INSERT INTO `STAT_SUM` (`EQPT_ID`, `DATA_GROUP`, `MEAS_DTTM`, `STATUS`) VALUES ' + \
            f'("{tblname}","{req_info["DATA_GROUP"]}","{req_info["MEAS_DTTM"]}","{req_info["STATUS"]}")' + \
            f' ON DUPLICATE KEY UPDATE `STATUS`="{req_info["STATUS"]}",`MEAS_DTTM`="{req_info["MEAS_DTTM"]}"'
            print(sqlStr)
            db_EQDAILY.execute(sqlStr)
    
    db_EQDAILY.commit()

def SUFPData2DB(req_info, db_EQDAILY):
    tblname = req_info["EQ"]

    insertColumnStr = ', '.join([("`" + _ + "`") for _ in ["MEAS_DTTM", "GLASS_ID", "DATA_GROUP", "STATUS"]])
    tmpData = {}
    for tmpPnt in ["P1", "P2", "P3", "P4"]:
        for tmpItem in ["Hm", "TopDx", "TopDy", "BotDx", "BotDy"]:
            for tmpVal in ["VAL", "USL", "UCL", "TARGET", "LCL", "LSL"]:
                insertColumnStr += f', `{tmpVal}_{tmpItem}_{tmpPnt}`'
                tmpData[tmpVal + "_" + tmpItem + "_" + tmpPnt] = []

    req_info["STATUS"] = ""
    req_info["STATUS"] = 0
    statusDict = {0:"ERR", 1:"OK", 2:"OOC", 3:"OOS"}

    # add by hm.chiang 2022.02.16 -- SUFP13 H2 NO USE
    if tblname == "SUFP13":
        for tmpItem in ["Hm", "TopDx", "TopDy", "BotDx", "BotDy"]:
            for idx, (val, usl, ucl, target, lcl, lsl) \
                in enumerate(zip(req_info[tmpItem]["VAL"].split(","), req_info[tmpItem]["USL"].split(","), req_info[tmpItem]["UCL"].split(","), \
                    req_info[tmpItem]["TARGET"].split(","), req_info[tmpItem]["LCL"].split(","), req_info[tmpItem]["LSL"].split(","))):
                pnt = "P" + str((idx % 4) + 1)
                tmpData["VAL_" + tmpItem + "_" + pnt].append(val)
                tmpData["USL_" + tmpItem + "_" + pnt].append(usl)
                tmpData["UCL_" + tmpItem + "_" + pnt].append(ucl)
                tmpData["TARGET_" + tmpItem + "_" + pnt].append(target)
                tmpData["LCL_" + tmpItem + "_" + pnt].append(lcl)
                tmpData["LSL_" + tmpItem + "_" + pnt].append(lsl)
                
                tmpStatus = 0
                # OOS
                if (float(val) < float(lsl) or float(val) > float(usl)) and idx not in [4, 5, 6, 7]:
                    tmpStatus = 3
                # OOC
                elif (float(val) < float(lcl) or float(val) > float(ucl)) and idx not in [4, 5, 6, 7]:
                    tmpStatus = 2
                # OK
                else:
                    tmpStatus = 1
                
                if req_info["STATUS"] == 0:
                    req_info["STATUS"] = tmpStatus
                else:
                    if req_info["STATUS"] < tmpStatus:
                        req_info["STATUS"] = tmpStatus
    else:
        for tmpItem in ["Hm", "TopDx", "TopDy", "BotDx", "BotDy"]:
            for idx, (val, usl, ucl, target, lcl, lsl) \
                in enumerate(zip(req_info[tmpItem]["VAL"].split(","), req_info[tmpItem]["USL"].split(","), req_info[tmpItem]["UCL"].split(","), \
                    req_info[tmpItem]["TARGET"].split(","), req_info[tmpItem]["LCL"].split(","), req_info[tmpItem]["LSL"].split(","))):
                pnt = "P" + str((idx % 4) + 1)
                tmpData["VAL_" + tmpItem + "_" + pnt].append(val)
                tmpData["USL_" + tmpItem + "_" + pnt].append(usl)
                tmpData["UCL_" + tmpItem + "_" + pnt].append(ucl)
                tmpData["TARGET_" + tmpItem + "_" + pnt].append(target)
                tmpData["LCL_" + tmpItem + "_" + pnt].append(lcl)
                tmpData["LSL_" + tmpItem + "_" + pnt].append(lsl)

                tmpStatus = 0
                # OOS
                if float(val) < float(lsl) or float(val) > float(usl):
                    tmpStatus = 3
                # OOC
                elif float(val) < float(lcl) or float(val) > float(ucl):
                    tmpStatus = 2
                # OK
                else:
                    tmpStatus = 1
                
                if req_info["STATUS"] == 0:
                    req_info["STATUS"] = tmpStatus
                else:
                    if req_info["STATUS"] < tmpStatus:
                        req_info["STATUS"] = tmpStatus
    req_info["STATUS"] = statusDict.get(req_info["STATUS"])
    print(req_info["STATUS"])

    insertValStr = ""
    updateValStr = ""
    for tmpPnt in ["P1", "P2", "P3", "P4"]:
        for tmpItem in ["Hm", "TopDx", "TopDy", "BotDx", "BotDy"]:
            for tmpVal in ["VAL", "USL", "UCL", "TARGET", "LCL", "LSL"]:
                tmpStr = "\"" + ','.join(tmpData[tmpVal + "_" + tmpItem + "_" + tmpPnt]) + "\""
                insertValStr += "," + tmpStr
                updateValStr += f',`{tmpVal}_{tmpItem}_{tmpPnt}`={tmpStr}'

    sqlStr = f'INSERT INTO `{tblname}` ({insertColumnStr}) VALUES ' + \
        f'(\"{req_info["MEAS_DTTM"]}\",\"{req_info["GLASS_ID"]}\",\"{req_info["DATA_GROUP"]}\",\"{req_info["STATUS"]}\"' + insertValStr + ')' + \
        f' ON DUPLICATE KEY UPDATE ' + \
        f'`STATUS`="{req_info["STATUS"]}"' + updateValStr
    
    db_EQDAILY.execute(sqlStr)

    sqlStr = f'INSERT INTO `STAT_SUM` (`EQPT_ID`, `DATA_GROUP`, `MEAS_DTTM`, `STATUS`) VALUES ' + \
        f'("{tblname}","{req_info["DATA_GROUP"]}","{req_info["MEAS_DTTM"]}","{req_info["STATUS"]}")' + \
        f' ON DUPLICATE KEY UPDATE `STATUS`="{req_info["STATUS"]}",`MEAS_DTTM`="{req_info["MEAS_DTTM"]}"'
    db_EQDAILY.execute(sqlStr)
    db_EQDAILY.commit()
