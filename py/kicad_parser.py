WHITESPACE = " \n\r\t"
TOKEN_ENDER = WHITESPACE + ")"


def qString(s):
    return '"' + s + '"'


class KiCadParser:
    s_expr = ""
    idx = 0
    arr: list = []

    def __init__(self, s_expr: str = ""):
        self.s_expr = s_expr

    def eatSpace(self) -> None:
        while self.s_expr[self.idx] in WHITESPACE:
            self.eatNextCharacter()

    def peekNextCharacter(self) -> str:
        return self.s_expr[self.idx]

    def getNextCharacter(self) -> str:
        ch = self.s_expr[self.idx]
        self.eatNextCharacter()
        return ch

    def eatNextCharacter(self) -> None:
        self.idx += 1

    def expectCharacter(self, ch) -> None:
        if self.s_expr[self.idx] != ch:
            raise Exception("Expected " + ch + " found " + self.s_expr[self.idx])

    def getNextToken(self) -> str:
        token = ""
        self.eatSpace()
        quote = '"'

        if self.peekNextCharacter() == quote:
            self.eatNextCharacter()
            while self.s_expr[self.idx] != quote:
                token += self.getNextCharacter()
            self.eatNextCharacter()
            return quote + token + quote

        else:
            while not self.s_expr[self.idx] in TOKEN_ENDER:
                token += self.getNextCharacter()
            self.eatSpace()
            return token

    def getNextTokenQuoted(self) -> str:
        token = ""
        self.eatSpace()
        while not self.s_expr[self.idx] in TOKEN_ENDER:
            token += self.getNextCharacter()
        self.eatSpace()
        return token

    def peekNextToken(self) -> str:
        saveidx = self.idx
        token = self.getNextToken()
        self.idx = saveidx
        return token

    def toList(self) -> list:
        ret: list = []

        self.eatSpace()
        self.expectCharacter("(")
        self.eatNextCharacter()

        while True:
            self.eatSpace()
            ch = self.peekNextCharacter()
            if ch == ")":
                self.eatNextCharacter()
                self.arr = ret
                return ret

            if ch == "(":
                array = self.toList()
                ret.append(array)

            if ch != "(" and ch != ")":
                token = self.getNextToken()
                ret.append(token)

    def printList(self, list, depth=0) -> None:

        indent = " " * 2 * depth

        for e in list:
            if isinstance(e, list):
                print(indent + "(")
                self.printList(e, depth + 1)
                print(indent + ")")
            else:
                print(indent + e)

    def listToSexp(self, root: list):
        def listToSexpInner(root: list, depth=0, out: list = []):

            indent = " " * 2 * depth

            for e in root:
                if isinstance(e, list):
                    out.append(indent + "(")
                    listToSexpInner(e, depth + 1, out)
                    out.append(indent + ")")
                elif isinstance(e, float):
                    out.append(indent + str(e))
                elif isinstance(e, int):
                    out.append(indent + str(e))
                else:
                    out.append(indent + e)
            return out

        return listToSexpInner([root], 0, [])
