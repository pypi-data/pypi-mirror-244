import re
from datetime import datetime

import maidenhead

from ..dataclasses import QOSReport
from ..logger import setup_logger

COMMENT_MATCH = re.compile(r"^(.*?)\s*//\s*(.*)$")

logger = setup_logger()


def match_report_tag(qos_report: QOSReport, tag_str: str, value: str) -> None:
    comment: str | None = None
    comment_match = re.match(pattern=COMMENT_MATCH, string=value)
    if comment_match:
        value = comment_match.group(1)
        comment = comment_match.group(2)

    match tag_str:
        case "APP_LoTW_OWNCALL":
            qos_report.app_lotw_owncall = value
        case "STATION_CALLSIGN":
            qos_report.station_callsign = value
        case "MY_DXCC":
            qos_report.my_dxcc = int(value)
        case "MY_COUNTRY":
            qos_report.my_country = value
        case "APP_LoTW_MY_DXCC_ENTITY_STATUS":
            qos_report.app_lotw_dxcc_entity_status = value
        case "MY_GRIDSQUARE":
            qos_report.my_gridsquare = value
            (
                qos_report.my_latitude,
                qos_report.my_longitude,
            ) = maidenhead.to_location(maiden=value, center=True)
        case "MY_STATE":
            qos_report.my_state = value
            qos_report.my_state_human = comment or qos_report.my_state
        case "MY_CNTY":
            qos_report.my_cnty = value
            qos_report.my_cnty_human = comment or qos_report.my_cnty_human
        case "MY_CQ_ZONE":
            qos_report.my_cq_zone = int(value)
        case "MY_ITU_ZONE":
            qos_report.my_itu_zone = int(value)
        case "CALL":
            qos_report.call = value
        case "BAND":
            qos_report.band = value
        case "FREQ":
            qos_report.freq = float(value)
        case "MODE":
            qos_report.mode = value
        case "APP_LoTW_MODEGROUP":
            qos_report.app_lotw_modegroup = value
        case "QSO_DATE":
            qos_report.qso_date = int(value)
        case "APP_LoTW_RXQSO":
            qos_report.app_lotw_rxqso = datetime.strptime(
                value, "%Y-%m-%d %H:%M:%S"
            )
        case "TIME_ON":
            qos_report.time_on = int(value)
        case "APP_LoTW_QSO_TIMESTAMP":
            qos_report.app_lotw_qso_timestamp = datetime.fromisoformat(value)
        case "QSL_RCVD":
            qos_report.qsl_rcvd = value
        case "QSLRDATE":
            qos_report.qslrdate = datetime.strptime(value, "%Y%m%d").date()
        case "APP_LoTW_RXQSL":
            qos_report.app_lotw_rxqsl = datetime.strptime(
                value, "%Y-%m-%d %H:%M:%S"
            )
        case "DXCC":
            qos_report.dxcc = int(value)
        case "COUNTRY":
            qos_report.country = value
        case "APP_LoTW_DXCC_ENTITY_STATUS":
            qos_report.app_lotw_dxcc_entity_status = value
        case "PFX":
            qos_report.pfx = str(value)
        case "APP_LoTW_2xQSL":
            qos_report.app_lotw_2xqsl = value
        case "GRIDSQUARE":
            qos_report.gridsquare = value
            qos_report.latitude, qos_report.longitude = maidenhead.to_location(
                maiden=value, center=True
            )
        case "CQZ":
            qos_report.cqz = int(value)
        case "ITUZ":
            qos_report.ituz = int(value)
        case "STATE":
            qos_report.state = value
            qos_report.state_human = comment or qos_report.state_human
        case "CNTY":
            qos_report.cnty = value
            qos_report.cnty_human = comment or qos_report.cnty_human
        case "APP_LoTW_CREDIT_GRANTED":
            qos_report.app_lotw_credit_granted = value
        case "CREDIT_GRANTED":
            qos_report.credit_granted = value
        case "APP_LoTW_ITUZ_Inferred":
            qos_report.app_lotw_ituz_inferred = value
        case "APP_LoTW_CQZ_Inferred":
            qos_report.app_lotw_cqz_inferred = value
        case "APP_LoTW_CQZ_Invalid":
            qos_report.app_lotw_cqz_invalid = value
        case "APP_LoTW_ITUZ_Invalid":
            qos_report.app_lotw_ituz_invalid = value
        case "APP_LoTW_MY_CQ_ZONE_Inferre":
            qos_report.app_lotw_cqz_invalid = value
        case "APP_LoTW_MY_ITU_ZONE_Inferred":
            qos_report.app_lotw_ituz_inferred = value
        case "FREQ_RX":
            qos_report.freq_rx = float(value)
        case "IOTA":
            qos_report.iota = value
        case "SUBMODE":
            qos_report.submode = value
        case "PROP_MODE":
            qos_report.prop_mode = value
        case "APP_LoTW_NPSUNIT":
            qos_report.app_lotw_npsunit = value
        case "APP_LoTW_QSLMODE":
            qos_report.app_lotw_qslmode = value
        case "APP_LoTW_MODE":
            qos_report.app_lotw_mode = value
        case "SAT_NAME":
            qos_report.sat_name = value
        case "APP_LoTW_GRIDSQUARE_Invalid":
            qos_report.app_lotw_gridsquare_invalid = value
        case _:
            logger.warn(f"Unknown tag: {tag_str}, {value}")
