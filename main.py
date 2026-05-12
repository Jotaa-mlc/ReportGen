import sys

from report.compras.main import (
    main as compras_report
)


REPORTS = {
    "compras": compras_report,
}


def main():

    report_name = sys.argv[1]

    REPORTS[report_name]()


if __name__ == "__main__":

    main()