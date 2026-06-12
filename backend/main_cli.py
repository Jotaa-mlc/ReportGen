import sys

from report.compras.main import (
    main as compras_report
)

from import_from_MDB import main as import_from_MDB

REPORTS = {
    "updt_db": import_from_MDB,
    "compras": compras_report,
}


def main():

    report_name = sys.argv[1]
    report_args = sys.argv[2:]

    REPORTS[report_name](*report_args)


if __name__ == "__main__":

    main()