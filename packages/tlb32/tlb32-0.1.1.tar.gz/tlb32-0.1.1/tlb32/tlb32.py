#!/usr/bin/env python3

from pygments.token import Name, Text, Operator, Punctuation, Comment
from pygments.lexers import get_lexer_by_name
from pygments import lex
import binascii
import argparse

DEBUG = False


def process(tlb_path: str):
    lexer = get_lexer_by_name("tlb")

    with open(tlb_path, "r") as f:
        tlb = f.read()

    tokens = list(lex(tlb, lexer))

    finds = []

    in_block = False

    start_idx = None
    for idx, token in enumerate(tokens):
        if (not in_block) and token in ((Comment.Singleline, "// request"), (Comment.Singleline, "// response")):
            start_idx = idx
            in_block = True
        if in_block and token[0] == Punctuation and token[1] == ";":
            in_block = False
            finds.append((start_idx, idx))

    def is_has_tag(tokens):
        for idx, t in enumerate(tokens):
            if t[0] == Name.Tag:
                return idx
        return None

    def get_tag_idx(tokens):
        for idx, t in enumerate(tokens):
            if t[0] == Name:
                return idx + 1
        return 0

    def is_request(tokens):
        if tokens[0] == (Comment.Singleline, "// request"):
            return True
        else:
            return False

    def request_op(schema: str):
        return format((binascii.crc32(bytes(schema, "utf-8")) | 0x80000) & 0x7fffffff, "x")

    def response_op(schema: str):
        return format(binascii.crc32(bytes(schema, "utf-8")) | 0x80000000, "x")

    offset = 0

    for f_idxs in finds:
        (start, end) = f_idxs
        start += offset
        end += offset
        block_tokens = tokens[start:end]
        has_tag = is_has_tag(block_tokens)
        tag_idx = (has_tag if has_tag else get_tag_idx(block_tokens)) + start
        need_replace = has_tag is not None
        tag_mode = is_request(block_tokens)
        full_block = "".join([t[1] for t in block_tokens])
        if DEBUG:
            print(f"\nfind scheme:\n{full_block}")

        if "{" in full_block or "##" in full_block:
            print("Implicit fields and Parametrized types is not supported. Sorry.")
            continue

        clear_block_parts = []
        need_ws = False

        for t in block_tokens:
            # print(t)
            if t[0] not in (Name.Tag, Text.Whitespace, Comment.Multiline, Comment.Singleline) \
                    and not (t[0] == Punctuation and not t[1] in (":", "[", "]")):

                if need_ws and t not in ((Punctuation, ":"), (Punctuation, "]")):
                    clear_block_parts.append(" ")

                clear_block_parts.append(t[1])

                if t in ((Punctuation, ":"), (Operator, "^"), (Punctuation, "[")):
                    need_ws = False
                else:
                    need_ws = True

        clear_block = "".join(clear_block_parts)
        if DEBUG:
            print(f"clear scheme:\n    {clear_block}")

        if tag_mode:
            tag = request_op(clear_block)
        else:
            tag = response_op(clear_block)
        if DEBUG:
            print(f"crc32 tag:\n    {tag}\n")

        print(f"mode: {'request ' if tag_mode else 'response'} | tag: {tag} | scheme: {clear_block}")

        tag_token = (Name.Tag, f"#{tag}")
        if need_replace:
            tokens[tag_idx] = tag_token
        else:
            tokens.insert(tag_idx, tag_token)
            offset += 1
    result_tlb = "".join([t[1] for t in tokens])
    with open(tlb_path, "w") as f:
        f.write(result_tlb)


def main():
    global DEBUG
    parser = argparse.ArgumentParser(
        prog="tlb32",
        description="Tool for automatic calculation of operation codes in TL-B schemes.",
    )

    parser.add_argument("filename")
    parser.add_argument("--debug", dest="debug", default=False, action="store_true")

    args = parser.parse_args()

    tlb_path = args.filename
    DEBUG = args.debug
    print(r"""_____________/\\\\\\______/\\\_____________/\\\\\\\\\\______/\\\\\\\\\_____cont.team      
_____________\////\\\_____\/\\\___________/\\\///////\\\___/\\\///////\\\___________       
____/\\\__________\/\\\_____\/\\\__________\///______/\\\___\///______\//\\\________      
__/\\\\\\\\\\\_____\/\\\_____\/\\\_________________/\\\//______________/\\\/________     
__\////\\\////______\/\\\_____\/\\\\\\\\\__________\////\\\__________/\\\//_________    
______\/\\\__________\/\\\_____\/\\\////\\\____________\//\\\______/\\\//___________   
_______\/\\\_/\\______\/\\\_____\/\\\__\/\\\___/\\\______/\\\_____/\\\/_____________  
________\//\\\\\_____/\\\\\\\\\__\/\\\\\\\\\___\///\\\\\\\\\/_____/\\\\\\\\\\\\\\\__ 
__________\/////_____\/////////___\/////////______\/////////______\///////////////__""")
    process(tlb_path)


if __name__ == '__main__':
    main()
