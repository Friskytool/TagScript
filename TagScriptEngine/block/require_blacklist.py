"""
MIT License

Copyright (c) 2020-2021 phenom4n4n

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Optional

from TagScriptEngine import Interpreter, Block


class RequireBlock(Block):
    """
    The require block will attempt to convert the given parameter into a channel
    or role, using name or ID. If the user running the tag is not in the targeted
    channel or doesn't have the targeted role, the tag will stop processing and
    it will send the response if one is given. Multiple role or channel
    requirements can be given, and should be split by a ",".

    **Usage:** ``{require([response]):<role,channel>}``

    **Aliases:** ``whitelist``

    **Payload:** role, channel

    **Parameter:** response, None

    **Examples:** ::

        {require:Moderator}
        {require(This tag can only be run in #general and #bot-cmds.):#general, #bot-cmds}
        {require(You aren't allowed to use this tag.):757425366209134764, 668713062186090506, 737961895356792882}
    """

    def will_accept(self, ctx: Interpreter.Context) -> bool:
        dec = ctx.verb.declaration.lower()
        return any([dec == "require", dec == "whitelist"])

    def process(self, ctx: Interpreter.Context) -> Optional[str]:
        if not ctx.verb.payload:
            return None
        actions = ctx.response.actions.get("requires")
        if actions:
            return None
        ctx.response.actions["requires"] = {
            "items": [i.strip() for i in ctx.verb.payload.split(",")],
            "response": ctx.verb.parameter,
        }
        return ""


class BlacklistBlock(Block):
    """
    The blacklist block will attempt to convert the given parameter into a channel
    or role, using name or ID. If the user running the tag is in the targeted
    channel or has the targeted role, the tag will stop processing and
    it will send the response if one is given. Multiple role or channel
    requirements can be given, and should be split by a ",".

    **Usage:** ``{blacklist([response]):<role,channel>}``

    **Payload:** role, channel

    **Parameter:** response, None

    **Examples:** ::

        {blacklist:Muted}
        {blacklist(This tag is not allowed in #support.):#support}
        {blacklist(You are blacklisted from using tags.):Tag Blacklist, 668713062186090506}
    """

    def will_accept(self, ctx: Interpreter.Context) -> bool:
        dec = ctx.verb.declaration.lower()
        return dec == "blacklist"

    def process(self, ctx: Interpreter.Context) -> Optional[str]:
        if not ctx.verb.parameter:
            return None
        actions = ctx.response.actions.get("blacklist")
        if actions:
            return None
        ctx.response.actions["blacklist"] = {
            "items": [i.strip() for i in ctx.verb.payload.split(",")],
            "response": ctx.verb.parameter,
        }
        return ""
