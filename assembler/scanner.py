import re

class Token(object):
    def __init__(self, text, category):
        self.text = text
        self.category = category

    @property
    def size_bytes(self):
        if self.category == "string":
            return len(bytes(json.loads(value.text), "utf-8"))
        elif self.category in ("integer", "label", "address", "size", "label_ref"):
            return 8
        elif self.category == "token":
            return 1
        else:
            exit(f"Internal Error: Size could not be determined for {self.category}")

    def __len__(self):
        return len(self.text)

    def __repr__(self):
        return f"Token({self.text !r}, {self.category !r})"

def scan_forward(text):
    for regex, category in [
        (r"#.*$", "comment"),
        (r"\"\"", "string"),
        (r"\".*?[^\\]\"", "string"),
        (r"\d+", "integer"),
        (r"\%[a-zA-Z_][a-zA-Z0-9_]*", "command"),
        (r"\?[a-zA-Z_][a-zA-Z0-9_]*", "size"),
        (r"\@[a-zA-Z_][a-zA-Z0-9_]*", "address"),
        (r"\:[a-zA-Z_][a-zA-Z0-9_.]*", "label_ref"),
        (r"\:\.[a-zA-Z_][a-zA-Z0-9_]*", "dot_label_ref"),
        (r"[a-zA-Z_][a-zA-Z0-9_]*:", "label"),
        (r"\.[a-zA-Z_][a-zA-Z0-9_]*:", "dotlabel"),
        (r"[a-zA-Z_][a-zA-Z0-9_]*", "token"),
        (r"=", "constant_assign"),
        (r"\{", "function_start"),
        (r"\}", "function_end"),
    ]:
        m = re.match(regex, text)
        if m:
            return Token(m.group(0), category)

    exit(f"Syntax Error: {text[:10]}{'...' if len(text) > 10 else ''}")
