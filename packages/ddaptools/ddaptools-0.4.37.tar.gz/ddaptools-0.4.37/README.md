# DDAP Modules

## Introduction

Here some useful modules to be used when for the development of DDAP

- So they can be plugged into ddanalytics applications and so forth.

## Features

- [x] dda_constants
- [x] etl_functions

### Classes

- [ ] guardian
  - [ ] BasicTokenGuardian


### DEPLOY

```bash
make new
```
update the `setup.py`




## Updated Instructions

Right so what you have to do, is having the `span_guid` here, you should be able to work on having them. On the 

```py
UPDATE event
SET end_time = CASE WHEN end_time < '2023-06-16 10:00:00' THEN '2023-06-16 10:00:00' ELSE end_time END
WHERE span_guid = 'your_span_guid'
```

```sql
UPDATE event SET end_time = CASE WHEN end_time < '2023-06-16 10:00:00' THEN '2023-06-16 0:00:00' ELSE end_time END WHERE span_guid = 'your_span_guid'
```


```sql
UPDATE event SET end_time = CASE WHEN end_time < '2023-06-17 10:00:00' THEN '2023-06-17 10:00:00' ELSE end_time END WHERE span_guid = 'aaad64e8-672f-3fa3-a94f-53c3cfe3d789'
```


```sql
UPDATE event SET end_time = '2023-06-15 10:00:00' WHERE span_guid = '0c4b4c8b-d00a-88ed-0f1e-24e045becaeb'
```



```sql
UPDATE event SET end_time = CASE WHEN end_time < '2023-06-17 10:00:00' THEN '2023-06-17 10:00:00' ELSE end_time END WHERE span_guid = '0c4b4c8b-d00a-88ed-0f1e-24e045becaeb'
```


```sql
UPDATE event SET end_time = CASE WHEN end_time < '2023-06-17 10:00:00' THEN '2023-06-17 10:00:00' ELSE end_time END WHERE span_guid = 'aaad64e8-672f-3fa3-a94f-53c3cfe3d789'
```














