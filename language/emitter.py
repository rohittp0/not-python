class Emitter:

    def __init__(self, file_path):
        self.file_path = file_path
        self.header = ""
        self.code = ""

    def emit(self, code):
        self.code += code

    def emit_line(self, code):
        self.code += code + '\n'

    def header_line(self, code):
        self.header += code + '\n'

    def write_file(self):
        with open(self.file_path, 'w') as outputFile:
            outputFile.write(self.header + self.code)
