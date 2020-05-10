import os

from logger import log


class DocumentReader(object):
    def __init__(self, document_path):
        self.document_path = document_path
        if not os.path.isfile(self.document_path):
            raise SystemExit("File not found: %s" % self.document_path)
        log.info("Reading file: %s.", self.document_path)
        with open(self.document_path, "rb") as f:
            self.file_string = f.read()

    def get_string(self):
        try:
            return self.file_string.decode("utf-8").strip()
        except UnicodeDecodeError:
            raise SystemExit("Cannot read '" + self.document_path + "': UnicodeDecodeError.")

    def save(self, doc_content):
        with open(self.document_path, "wb") as f:
            f.write(doc_content.encode("utf-8"))
        log.info("Wrote UTF-8-encoded document: %s.", self.document_path)
