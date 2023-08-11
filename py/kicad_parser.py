from typing import List, Union


class KiCadParser:
    WHITESPACE = " \n\r\t"
    TOKEN_ENDER = WHITESPACE + ")"

    s_expr = ""
    idx = 0

    def __init__(self, s_expr: str = ""):
        """Initializes the parser with a given S-expression string."""
        self.s_expr = s_expr

    def eat_space(self) -> None:
        """Advances the index to the next non-whitespace character."""
        while self.s_expr[self.idx] in self.WHITESPACE:
            self.eat_next_character()

    def peek_next_character(self) -> str:
        """Returns the current character without advancing the index."""
        return self.s_expr[self.idx]

    def get_next_character(self) -> str:
        """Returns the current character and advances the index."""
        ch = self.s_expr[self.idx]
        self.eat_next_character()
        return ch

    def eat_next_character(self) -> None:
        """Advances the index by one."""
        self.idx += 1

    def expect_character(self, ch: str) -> None:
        """Raises an exception if the current character is not the expected one."""
        if self.s_expr[self.idx] != ch:
            raise Exception("Expected " + ch + " found " + self.s_expr[self.idx])

    def get_next_token(self, quoted: bool = False) -> str:
        """
        Returns the next token in the S-expression string.
        If `quoted` is True, the token is enclosed in double quotes.
        """
        token = ""
        quote = '"'
        self.eat_space()

        if self.peek_next_character() == quote or quoted:
            self.eat_next_character()
            while self.s_expr[self.idx] != quote:
                token += self.get_next_character()
            self.eat_next_character()
            return quote + token + quote

        else:
            while not self.s_expr[self.idx] in self.TOKEN_ENDER:
                token += self.get_next_character()
            self.eat_space()
            return token

    def peek_next_token(self) -> str:
        """Returns the next token without advancing the index."""
        saveidx = self.idx
        token = self.get_next_token()
        self.idx = saveidx
        return token

    def to_list(self) -> List:
        """
        Parses the S-expression string and converts it to a nested list structure.
        """
        ret: List = []
        stack: List[List] = [ret]

        self.eat_space()
        self.expect_character("(")
        self.eat_next_character()

        while True:
            self.eat_space()
            ch = self.peek_next_character()

            if ch == ")":
                self.eat_next_character()
                stack.pop()
                if not stack:
                    return ret
                else:
                    continue

            if ch == "(":
                new_list: List = []
                stack[-1].append(new_list)
                stack.append(new_list)
                self.eat_next_character()
                continue

            if ch != "(" and ch != ")":
                token = self.get_next_token()
                stack[-1].append(token)

    def print_list(self, list: List, depth: int = 0) -> str:
        """
        Returns a formatted string representation of the nested list.
        """
        output = []
        indent = " " * 2 * depth

        for e in list:
            if isinstance(e, List):
                output.append(indent + "(")
                output.append(self.print_list(e, depth + 1))
                output.append(indent + ")")
            else:
                output.append(indent + e)

        return "\n".join(output)

    def list_to_sexp(self, root: List) -> List[str]:
        """
        Converts a nested list back to an S-expression string.
        """

        def list_to_sexp_inner(
            root: List, depth: int = 0, out: List[str] = []
        ) -> List[str]:

            indent = " " * 2 * depth

            for e in root:
                if isinstance(e, List):
                    out.append(indent + "(")
                    list_to_sexp_inner(e, depth + 1, out)
                    out.append(indent + ")")
                elif isinstance(e, (float, int)):
                    out.append(indent + str(e))
                else:
                    out.append(indent + e)
            return out

        return list_to_sexp_inner([root], 0, [])

    @staticmethod
    def q_string(s: str) -> str:
        """Returns the input string enclosed in double quotes."""
        return '"' + s + '"'
