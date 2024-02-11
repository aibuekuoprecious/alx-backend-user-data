#!/usr/bin/env python3
"""
Contains a logger implementation that filters sensitive data.
"""

import os
import re
import logging
from typing import List, Tuple

import mysql.connector

PII_FIELDS: Tuple[str] = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Filter sensitive data from a message.
    """
    pattern = re.compile(r"({0}=)[^{1}]*({1})".format("|".join(fields), separator))
    return pattern.sub(r"\1{}\2".format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter object.

        Args:
            fields (List[str]): A list of fields to be redacted.

        Returns:
            None
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record and applies redaction to sensitive data.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log record with redacted sensitive data.
        """
        log = super(RedactingFormatter, self).format(record=record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Get a logger instance with a redacting formatter.

    Returns:
        logging.Logger: The logger instance.
    """
    logger = logging.getLogger("user_data")
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to the personal data database and returns a MySQLConnection object.

    Returns:
        The connection to the personal data database.
    """
    connector = mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD"),
    )
    return connector


def main() -> None:
    """
    Main function to retrieve user data from the database and log it.
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    rows = (row for row in cursor)
    for row in rows:
        msg = (
            f"name={row[0]}\n"
            f"email={row[1]}\n"
            f"phone={row[2]}\n"
            f"ssn={row[3]}\n"
            f"password={row[4]}\n"
            f"ip={row[5]}\n"
            f"last_login={row[6]}\n"
            f"user_agent={row[7]}\n"
        )
        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
