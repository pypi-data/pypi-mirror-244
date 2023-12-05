# NoteVault

Define a schema over markdown documents and store certain sections as columsn in sqlite database.

Every list item must have a `name` as unique key. For non-list items the key is the heading.

Every `save` creates new version of the documents's child items, no update/overwrite, i.e. `created == updated`.
Reason: PK is auto-incremented, so it's not possible to update existing items.
Existing items are just de-connected, i.e. foreign keys are set to `null`.
This also implies that deletion of detached items make sense.

Data will be extracted either as:
## 1. Key-Value pairs
```yaml
Model:
  KV_List:
    name:
      type: string
    start:
      type: time
      nullable: true
    duration:
      type: int
      nullable: false
    breaks:
      type: timedelta
      nullable: true
    data:
      type: string
      nullable: true
```
This works for lists and headings. The heading would be the key and the following paragraph the value.

Lists can be narrow or wide:

Narrow list (often used with headings as lists):
- start: 07:30
- duration: 2:30
- participants: @user1, @user2

Wide list:
- name: item2, start: 17:30, duration: 2, breaks:, data: "adsfadfasdf, asdfasdf"
- name: item1, start: 07:30, duration: 1, breaks: 0:30

## 2. Lists:
```yaml
Model:
  List:
    - field:
        name: item
        type: string
        nullable: false
    - field:
        name: time
        type: time
        nullable: true
    - field:
        name: break
        type: timedelta
        nullable: true
    - field:
        name: detail
        type: string
        nullable: true
```
List:
- item2, 17:30,, "adsfadfasdf, asdfasdf"
- item1, 07:30, 0:30

## Format
- Sections are defined by headings.
- key-value pairs are extracted into fields, e.g. `key: value`
- Fields (extraction units) correspond to "Tags", e.g. `li, h2` because it can contain other tags and newlines.
- field values with commas must be quoted: `participants: '@user1, @user2'`

### Single Item:
- spec: `is_list: false`
- markdown lists as fields: `- key: value`

### Multiple Items:
#### markdown lists
- spec: `is_list: true` + `list_specifier: kv_list`
- substructure: format: `- key: value, key: value, key: "complex, value"`
- 
#### sub-headings
- spec: `is_list: true` + `heading_field: name` + `list_specifier: heading` (must specify the field which will hold the sub-heading in the schema)
- substructure: format: `## Title x`
can contain:
- markdown lists as fields: `- key: value`
- sub-headings as simple content fields

