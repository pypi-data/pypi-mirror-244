import re
from pathlib import Path

from ..dataclasses import Header, QOSReport
from ..logger import setup_logger
from .match_header_tag import match_header_tag
from .match_report_tag import match_report_tag

# Parser for Amateur Data Interchange Format

logger = setup_logger()

EOH_MATCH = re.compile(r"<eoh>")
EOR_MATCH = re.compile(r"<eor>")

# Group 1 is tag, group 2 is length, group 3 is value
TAG_MATCH = re.compile(r"^<(.*):(\d*)>(.*)$")


def parse_adi(file_path: str | Path) -> tuple[Header, list[QOSReport]]:
    header = Header()
    qos_reports: list[QOSReport] = []

    with open(
        file=file_path,
        mode="r",
        encoding="utf-8",
        errors="replace",
    ) as adif_file:
        # Get Header
        while True:
            current_line: str = adif_file.readline()

            header.full_header += current_line

            tag_match = re.match(pattern=TAG_MATCH, string=current_line)

            if tag_match:
                tag_str, length, value = tag_match.groups()

                match_header_tag(
                    header=header,
                    tag_str=tag_str,
                    value=value,
                )

            if re.match(pattern=EOH_MATCH, string=current_line):
                break

        while True:
            qos_report = QOSReport()

            while True:
                current_line: str = adif_file.readline()
                if not current_line:
                    break

                qos_report.full_report += current_line

                tag_match = re.match(pattern=TAG_MATCH, string=current_line)

                if tag_match:
                    tag_str, length, value = tag_match.groups()

                    match_report_tag(
                        qos_report=qos_report,
                        tag_str=tag_str,
                        value=value,
                    )

                if re.match(pattern=EOR_MATCH, string=current_line):
                    qos_reports.append(qos_report)
                    break

            if not current_line:
                break

    return header, qos_reports
