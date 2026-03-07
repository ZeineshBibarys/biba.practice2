import re

# 1)
def match_a_followed_by_zero_or_more_bs(s: str) -> bool:
    return re.fullmatch(r'ab*', s) is not None

# 2)
def match_a_followed_by_two_to_three_bs(s: str) -> bool:
    return re.fullmatch(r'ab{2,3}', s) is not None

# 3) 
def find_lowercase_joined_with_underscore(s: str):
    return re.findall(r'[a-z]+(?:_[a-z]+)+', s)

# 4)
def find_capital_followed_by_lowers(s: str):
    return re.findall(r'[A-Z][a-z]+', s)

# 5) 
def match_a_then_anything_ending_b(s: str) -> bool:
    return re.fullmatch(r'a.*b', s) is not None

# 6)
def replace_space_comma_dot_with_colon(s: str) -> str:
    return re.sub(r'[ ,.]', ':', s)

# 7)
def snake_to_camel(s: str) -> str:
    parts = s.split('_')
    if not parts:
        return s
    return parts[0] + ''.join(p.capitalize() for p in parts[1:] if p != '')

# 8) 
def split_at_uppercase(s: str):
    return re.findall(r'[A-Z][a-z]*|[a-z]+|[0-9]+', s)

# 9)
def insert_spaces_before_capitals(s: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', s)

# 10)
def camel_to_snake(s: str) -> str:
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()

