#!/usr/bin/env python3
import os
import token
import tokenize

TOKEN_WHITELIST = [token.OP, token.NAME, token.NUMBER, token.STRING]

if __name__ == "__main__":
    table = []
    for path, subdirs, files in os.walk("team_C"):
        for name in files:
            if not name.endswith(".py"): continue
            if "checkpoi" in path: continue
            filepath = os.path.join(path, name)
            with tokenize.open(filepath) as file_:
                if "opcodes" in filepath:  # runs OOM on the long lines in opcodes.py
                    token_count, line_count = 9999, len(file_.readlines())
                else:
                    tokens = [t for t in tokenize.generate_tokens(file_.readline) if t.type in TOKEN_WHITELIST]
                    token_count, line_count = len(tokens), len(set([t.start[0] for t in tokens]))
                table.append([filepath, line_count, token_count/line_count])

    print("Name                    Lines Tokens/Line")
    for fp, lc, tl in sorted(table, key=lambda x: -x[1]):
        print(f"{fp:23} {lc:4d}  {tl:4.1f}")

    print(f"TOTAL                   {sum([x[1] for x in table]):4d}")
