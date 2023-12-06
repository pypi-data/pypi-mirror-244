from webql.common.errors import QuerySyntaxError

from .lexer import Lexer
from .source import Source
from .token import Token
from .token_kind import TokenKind


class Parser:
    """A parser for WebQL queries. It is a recursive descent parser, which is a top-down parser that
    uses a set of recursive procedures to process the input."""

    def __init__(self, source: Source | str) -> None:
        """Initialize the parser.

        Parameters:

        source (Source | str): The source of the query."""
        self.source = isinstance(source, Source) and source or Source(source)
        self.lexer = Lexer(self.source)

    def parse(self):
        """Parses the source and check for syntax. It is the entry point of the parser."""
        self._expect_token(TokenKind.SOF)
        self._parse_container()
        self._expect_token(TokenKind.EOF)

    def _parse_container(self):
        """Parses a container, which is enclosed by curly braces."""
        self._many(TokenKind.BRACE_L, self._parse_identifier, TokenKind.BRACE_R)

    def _parse_identifier(self):
        """Parses an identifier."""
        self._expect_token(TokenKind.IDENTIFIER)

        if self._peek(TokenKind.BRACE_L):
            self._parse_container()
        elif self._peek(TokenKind.BRACKET_L):
            self._parse_list()

    def _parse_list(self):
        """Parses a list, represented by two brackets."""
        prev_token = self.lexer.token.prev
        # make sure list token is following an identifier
        if prev_token.kind != TokenKind.IDENTIFIER:
            error_message = f"Expected Identifier, found {prev_token.kind.value} on row {prev_token.line}. List token ([]) must follow an identifier."
            raise QuerySyntaxError(error_message)

        self._expect_token(TokenKind.BRACKET_L)
        self._expect_token(TokenKind.BRACKET_R)

        if self._peek(TokenKind.BRACE_L):
            self._parse_container()

    def _many(self, open_kind: TokenKind, parse_fn: callable, close_kind: TokenKind):
        """Parses zero or more tokens of the given kind by repeatedly calling the given
        parse function. Check whether the syntax is valid."""
        self._expect_token(open_kind)
        identifier_name_list = set()
        while True:
            # make sure there is no duplicate identifier in the same container
            if self._peek(TokenKind.IDENTIFIER):
                identifier = self.lexer.token.value
                if identifier in identifier_name_list:
                    error_message = f"Duplicate identifier '{identifier}' on row {self.lexer.token.line}. Identifier must be unique in the same container."
                    raise QuerySyntaxError(error_message)
                identifier_name_list.add(identifier)

            parse_fn()
            if self._expect_token(close_kind, optional=True):
                break

    def _expect_token(self, kind: TokenKind, optional=False) -> Token | None:
        """Consumes the next token if it matches the given kind, otherwise throws an
        error. If optional is true, then it returns None instead of throwing.

        Parameters:
        optional (bool): Whether to return None instead of throwing an error.
        """
        token = self.lexer.token
        if token.kind == kind:
            return self.lexer.advance()

        if optional:
            return None

        error_message = f"Expected {kind.value}, found {token.kind.value} on row {token.line}"
        raise QuerySyntaxError(error_message)

    def _peek(self, kind: TokenKind) -> bool:
        """Returns "true" if the next token is of the given kind."""
        return self.lexer.token.kind == kind
