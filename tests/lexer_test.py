import parsy

ops  = parsy.regex("[\+-]")
whitespace = parsy.regex('\s*')
openning_brace = parsy.regex('\(')
closing_brace = parsy.regex('\)')
const_term = parsy.regex('[0-9]+')
# ax^n
term = parsy.regex('[0-9]*x(\^[0-9]+)?')

expr_ = parsy.forward_declaration()
group = (openning_brace >> expr_.until(closing_brace | parsy.eof) << closing_brace)
expr_.become(whitespace >> (term | const_term | ops | group))
expr  = expr_.many()

print(expr.parse('10x'))
print(expr.parse('10'))
print(expr.parse('+'))
print(expr.parse('10x+1'))

print(expr.parse('2(10x^2 + 1) - (x(x^2 - 1) - 1)(-2x + 1) - 3x^2'))
