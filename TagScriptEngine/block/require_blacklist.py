from typing import Optional

from ..interface import verb_required_block
from ..interpreter import Context


class RequireBlock(verb_required_block(True, parameter=True)):
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

    ACCEPTED_NAMES = ("require", "whitelist")

    def process(self, ctx: Context) -> Optional[str]:
        actions = ctx.response.actions.get("requires")
        if actions:
            return None
        ctx.response.actions["requires"] = {
            "items": [i.strip() for i in ctx.verb.payload.split(",")],
            "response": ctx.verb.parameter,
        }
        return ""


class BlacklistBlock(verb_required_block(True, parameter=True)):
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

    ACCEPTED_NAMES = ("blacklist",)

    def process(self, ctx: Interpreter.Context) -> Optional[str]:
        if not ctx.verb.parameter:
            return None
        if actions := ctx.response.actions.get("blacklist"):
            return None
        ctx.response.actions["blacklist"] = {
            "items": [i.strip() for i in ctx.verb.payload.split(",")],
            "response": ctx.verb.parameter,
        }
        return ""
