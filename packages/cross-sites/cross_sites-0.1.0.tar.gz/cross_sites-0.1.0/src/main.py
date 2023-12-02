import re

sting = "user ((DAT))(NGUYEN)"

reg = re.compile(r"\((\w+)\)")

rs = reg.findall(sting)


print(rs)
