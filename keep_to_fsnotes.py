#!/usr/bin/env python3
import os
import json
import datetime
import shutil
from marshmallow import Schema, ValidationError, fields
from pathlib import Path


class MSecTimestamp(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return 0
        return datetime.timestamp(value) * 1000000 + value.microsecond

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return datetime.datetime.fromtimestamp(value/1000000) + datetime.timedelta(microseconds=value%1000000)
        except ValueError as error:
            raise ValidationError("Bad timestamp.") from error


class AttachmentsSchema(Schema):
    mimetype = fields.String()
    filePath = fields.String()


class ListItemSchema(Schema):
    text = fields.String()
    isChecked = fields.Bool()


class AnnotationSchema(Schema):
    description = fields.String()
    source = fields.String()
    title = fields.String()
    url = fields.String()


class ShareeSchema(Schema):
    isOwner = fields.Bool()
    type = fields.String()
    email = fields.String()


class KeepNoteSchema(Schema):
    title = fields.String()
    textContent = fields.String(load_default='')
    createdTimestampUsec = MSecTimestamp()
    userEditedTimestampUsec = MSecTimestamp()
    attachments = fields.List(fields.Nested(AttachmentsSchema))
    isTrashed = fields.Bool()
    isArchived = fields.Bool()
    isPinned = fields.Bool()
    color = fields.String()
    annotations = fields.List(fields.Nested(AnnotationSchema))
    listContent = fields.List(fields.Nested(ListItemSchema))
    sharees = fields.List(fields.Nested(ShareeSchema))


class KeepNote:

    def __init__(self, filename):
        with open(filename, 'rt') as f:
            schema = KeepNoteSchema()
            self.data = schema.load(data=json.load(f))

    def save(self):
        title = self.data["title"]
        if not title:
            title = self.data["textContent"].split('\n')[0]

        title = title.replace('/', '_')

        filename = f'fsnotes/{title}.md'
        with open(filename, 'wt') as f:
            f.write(f'{self.data["textContent"]}\n')

        with open(filename, 'a') as f:
            attachments = note.data.get('attachments', [])
            for attachment in attachments:
                f.write(f'![](i/{attachment["filePath"]})\n')
                if os.path.exists(f'keep/{attachment["filePath"]}'):
                    shutil.copy2(f'keep/{attachment["filePath"]}', f'fsnotes/i/{attachment["filePath"]}')

            listContent = note.data.get('listContent', [])
            for item in listContent:
                f.write(f'- [{"x" if item["isChecked"] else " "}] {item["text"]}\n')

        os.utime(filename, (self.data['createdTimestampUsec'].timestamp(), self.data['userEditedTimestampUsec'].timestamp()))


# enum all jsons in Keep
Path('fsnotes/i').mkdir(parents=True, exist_ok=True)
for f in os.listdir('keep'):
    if f.endswith(".json"):
        note = KeepNote(f'keep/{f}')
        note.save()
