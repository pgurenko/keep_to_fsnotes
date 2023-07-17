#!/usr/bin/env python3
import os
import json
import datetime
from marshmallow import Schema, ValidationError, fields


class MSecTimestamp(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return 0
        return datetime.timestamp(value) * 1000000 + value.microsecond

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            print(f'@@@value={value}')
            return datetime.datetime.fromtimestamp(value/1000000) + datetime.timedelta(microseconds=value%1000000)
        except ValueError as error:
            raise ValidationError("Bad timestamp.") from error


class AttachmentsSchema(Schema):
    mimetype = fields.Str()
    filePath = fields.Str()


class KeepNoteSchema(Schema):
    title = fields.Str()
    textContent = fields.Str(load_default='')
    createdTimestampUsec = MSecTimestamp()
    userEditedTimestampUsec = MSecTimestamp()
    attachments = fields.List(fields.Nested(AttachmentsSchema))


class KeepNote:

    def __init__(self, filename):
        with open(filename, 'rt') as f:
            note = KeepNoteSchema.from_dict(json.load(f))

            print(note.title)
            print(getattr(note, 'textContent', ''))
            print(note.createdTimestampUsec)
            print(note.userEditedTimestampUsec)
            print(getattr(note, 'attachments', ''))
            # exit(0)

            # [{"filePath":"175154aa763.b99d62826c8d9b61.jpg","mimetype":"image/jpeg"}]
            # self.attachments = []
            

# enum all jsons in Keep
for f in os.listdir('keep'):
    if f.endswith(".json"):
        KeepNote(f'keep/{f}')