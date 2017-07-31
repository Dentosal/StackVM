import copy
import itertools
import json

from . import scanner

from stackvm.byteutil import *
from stackvm.opcodes import OPCODES

OP_NAMES = {v.__name__[3:]: k for k,v in OPCODES.items()}

def count_bytes_codelike(items):
    def size(item):
        if isinstance(item, int):
            return 1
        elif isinstance(item, str):
            return len(item)
        else:
            return item.size_bytes

    return sum(map(size, items))

class LabelReference(object):
    def __init__(self, name):
        self.name = name

    @property
    def size_bytes(self):
        return 8

class PostponedAddress(object):
    def __init__(self, name):
        self.name = name

    @property
    def size_bytes(self):
        return 8


class Assembler(object):
    def __init__(self):
        self.data_addr = {}
        self.data_constants = {}
        self.code_labels = {}
        self.last_label = None

    @property
    def cloned(self):
        return copy.deepcopy(self)

    def scan(self, lines):
        tokens = []

        for line in lines:
            line = line.strip()
            while line:
                token = scanner.scan_forward(line)
                if token.category != "comment":
                    tokens.append(token)
                line = line[len(token):].strip()

        return tokens

    def process_constants(self, tokens):
        tokens = tokens[:]

        code_tokens = []
        while tokens:
            if len(tokens) >= 2 and tokens[1].category == "constant_assign":
                if len(tokens) < 3:
                    exit("Syntax Error: Code must not end with assignment operator (=)")

                name, _, value = tokens[:3]
                tokens = tokens[3:]

                if value.category == "string":
                    self.data_constants[name.text] = json.loads(value.text).encode("utf-8")
                else:
                    exit(f"Error: Unknown constant {value}")
                continue

            code_tokens.append(tokens.pop(0))

        return code_tokens

    def token_to_code(self, token, byte_pos=None):
        if token.category == "integer":
            return list(bytes_from_int(int(token.text), pad_to=8))

        elif token.category == "token":
            if token.text in OP_NAMES:
                return [OP_NAMES[token.text]]
            else:
                exit(f"Error: Unknown token {token}")

        elif token.category == "string_len":
            if token.text[1:] in self.data_constants:
                c = self.data_constants[token.text[1:]]
                return list(bytes_from_int(len(str_to_u32unicode(c.decode("utf-8"))), pad_to=8))
            else:
                exit(f"Error: Unknown constant: {token.text[1:]}")

        elif token.category == "size":
            if token.text[1:] in self.data_constants:
                c = self.data_constants[token.text[1:]]
                return list(bytes_from_int(count_bytes_codelike(c), pad_to=8))
            else:
                exit(f"Error: Unknown constant: {token.text[1:]}")

        elif token.category == "address":
            if token.text[1:] in self.data_constants:
                c = self.data_constants[token.text[1:]]
                return [PostponedAddress(token.text[1:])]
            else:
                exit(f"Error: Unknown constant: {token.text[1:]}")

        elif token.category == "label_ref": # address of label
            if self.last_label is None:
                exit(f"Error dotlabel reference before first normal label: {token.text}")
            return [LabelReference(token.text[1:])]

        elif token.category == "dot_label_ref": # address of label
            return [LabelReference(self.last_label + token.text[1:])]

        elif token.category == "command":
            exit(f"Error: Unknown command {token}")

        elif token.category == "label":
            self.last_label = token.text[:-1]
            self.code_labels[self.last_label] = byte_pos
            return []

        elif token.category == "dotlabel":
            if self.last_label is None:
                exit(f"Error dotlabel before first normal label: {token.text}")

            self.code_labels[self.last_label + token.text[:-1]] = byte_pos
            return []

        else:
            exit(f"Internal Error: Invalid token category {token.category} ({token})")

    def assemble(self, lines):
        tokens = self.scan(lines)
        tokens = self.process_constants(tokens)

        data = []
        code = []

        for name, value in self.data_constants.items():
            self.data_addr[name] = len(data)

            data_value = []
            for v in value:
                if isinstance(v, PostponedAddress):
                    data_value += bytes_from_int(self.data_addr[v.name], pad_to=8)
                else:
                    data_value.append(v)

            data += data_value

        for token in tokens:
            code += self.token_to_code(token, count_bytes_codelike(code))

        # resolve label references
        for i, item in reversed(list(enumerate(code))):
            if isinstance(item, LabelReference):
                code[i:i+1] = bytes_from_int(len(data) + self.code_labels[item.name], pad_to=8)
            elif isinstance(item, PostponedAddress):
                code[i:i+1] = bytes_from_int(self.data_addr[item.name], pad_to=8)

        return data, code
