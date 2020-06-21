## tags.py
# Tagged message support.
import pydle.client
import pydle.protocol
from pydle.features import rfc1459
import re
import attr
import typing
TAG_INDICATOR = '@'
TAG_SEPARATOR = ';'
TAG_VALUE_SEPARATOR = '='
TAGGED_MESSAGE_LENGTH_LIMIT = 1024

TAG_CONVERSIONS = {
    r"\:": ';',
    r"\s": ' ',
    r"\\": '\\',
    r"\r": '\r',
    r"\n": '\n'
}

@attr.s
class TaggedMessage(rfc1459.RFC1459Message):

    tags = attr.ib(type=typing.Optional[typing.Dict[str, typing.Any]], default=None)

    @classmethod
    def parse(cls, line, encoding=pydle.protocol.DEFAULT_ENCODING):
        """
        Parse given line into IRC message structure.
        Returns a TaggedMessage.
        """
        valid = True
        # Decode message.
        try:
            message = line.decode(encoding)
        except UnicodeDecodeError:
            # Try our fallback encoding.
            message = line.decode(pydle.protocol.FALLBACK_ENCODING)

        # Sanity check for message length.
        if len(message) > TAGGED_MESSAGE_LENGTH_LIMIT:
            valid = False

        # Strip message separator.
        if message.endswith(rfc1459.protocol.LINE_SEPARATOR):
            message = message[:-len(rfc1459.protocol.LINE_SEPARATOR)]
        elif message.endswith(rfc1459.protocol.MINIMAL_LINE_SEPARATOR):
            message = message[:-len(rfc1459.protocol.MINIMAL_LINE_SEPARATOR)]
        raw = message

        # Parse tags.
        tags = {}
        if message.startswith(TAG_INDICATOR):
            message = message[len(TAG_INDICATOR):]
            raw_tags, message = message.split(' ', 1)

            for raw_tag in raw_tags.split(TAG_SEPARATOR):
                if TAG_VALUE_SEPARATOR in raw_tag:
                    tag, value = raw_tag.split(TAG_VALUE_SEPARATOR, 1)
                else:
                    tag = raw_tag
                    value = True
                # Parse escape sequences since IRC escapes != python escapes

                # convert known escapes first
                for escape, replacement in TAG_CONVERSIONS.items():
                    value = value.replace(escape, replacement)

                # convert other escape sequences based on the spec
                pattern =re.compile(r"(\\[\s\S])+")
                for match in pattern.finditer(value):
                    escape = match.group()
                    value = value.replace(escape, escape[1])


                # Finally: add constructed tag to the output object.
                tags[tag] = value

        # Parse rest of message.
        message = super().parse(message.lstrip().encode(encoding), encoding=encoding)
        _kw = attr.asdict(message)
        del _kw['valid']
        del _kw['raw']

        return TaggedMessage(raw=raw, valid=message.valid and valid, tags=tags, **_kw)

    def construct(self, force=False):
        """
        Construct raw IRC message and return it.
        """
        message = super().construct(force=force)

        # Add tags.
        if self.tags:
            raw_tags = []
            for tag, value in self.tags.items():
                if value == True:
                    raw_tags.append(tag)
                else:
                    raw_tags.append(tag + TAG_VALUE_SEPARATOR + value)

            message = TAG_INDICATOR + TAG_SEPARATOR.join(raw_tags) + ' ' + message

        if len(message) > TAGGED_MESSAGE_LENGTH_LIMIT and not force:
            raise protocol.ProtocolViolation(
                'The constructed message is too long. ({len} > {maxlen})'.format(len=len(message),
                                                                                 maxlen=TAGGED_MESSAGE_LENGTH_LIMIT),
                message=message)
        return message


class TaggedMessageSupport(rfc1459.RFC1459Support):
    def _create_message(self, command, *params, tags=None, **kwargs):
        return TaggedMessage(params=params, command=command,  tags=tags or {},**kwargs)

    def _parse_message(self):
        sep = rfc1459.protocol.MINIMAL_LINE_SEPARATOR.encode(self.encoding)
        message, _, data = self._receive_buffer.partition(sep)
        self._receive_buffer = data

        return TaggedMessage.parse(message + sep, encoding=self.encoding)
