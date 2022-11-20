import parsy


def preprocess(quest):
    poly = quest.split('=')

    if len(poly) > 2:
        raise Exception("Problem not correctly formatted")
    elif len(poly) == 1:
        poly.append("0")

    lex = lexer()

    try:
        lhs_exp = lex.parse(poly[0].strip())
        rhs_exp = lex.parse(poly[1].strip())
    except parsy.ParseError as exc:
        if  '\\)' in exc.expected:
            raise Exception("Could not find matching closing bracket")

        raise Exception("Ill-formatted input")

    return lhs_exp, rhs_exp


def lexer():
    """ Tokenizes the imput expression
     '10x+1' => ['10x', '+', '1']
     '2(10x^2 + 1) - (x - 1)(-2x + 1)' =>
         ['2', ['10x^2', '+', '1'], '-', ['x', ['x^2', '-', '1'], '-', '1'], ['-', '2x', '+', '1']]
    """
    operators  = parsy.regex("[\+-]")
    whitespace = parsy.regex('\s*')
    openning_brace = parsy.regex('\(')
    closing_brace = parsy.regex('\)')
    const_term = parsy.regex('[0-9]+')
    # ax^n
    term = parsy.regex('[0-9]*x(\^[0-9]+)?')

    expr_ = parsy.forward_declaration()
    group = (openning_brace >> expr_.until(closing_brace | parsy.eof) << closing_brace)
    expr_.become(whitespace >> (term | const_term | operators | group) << whitespace)
    expr  = expr_.many()

    return expr
    