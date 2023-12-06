from src.adi_parser import parse_adi

with open(
    file=r"C:\Users\39008\Documents\python envs\adi_parser\tests\lotwreport_full.adi",
    mode="rb",
) as file_:
    header, reports = parse_adi(file=file_)

    print(reports[-1])
