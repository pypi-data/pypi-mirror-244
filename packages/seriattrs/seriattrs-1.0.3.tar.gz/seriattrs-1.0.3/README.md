# SeriArrts module for automatic serialization and deserialization

SeriArrts is an unofficial extension to [attrs](https://www.attrs.org/) library. 
The module is ment to be used in conjunction with databases or json which may require serialization and deserialization.
To allow creation of custom Object-Database mapping DbAttrs supports basic datatype such as ints, uints, vars etc.

## Installation

You can install the `seriattrs` package using pip:

```bash
pip install seriattrs
```

### Example

Here's an example of how to use the serialization and deserialization with `SeriArrts`:

```python
@define
class Bar(DbClass):
    dictionary: dict
    date: datetime
    decimal: Decimal

@define
class Foo(DbClass):
    dictionary: dict
    date: datetime
    decimal: Decimal
    bar: Bar

foo = Foo({}, datetime.now(), Decimal(1), Bar({}, datetime.now(), Decimal(1)))
serialized = foo.get_db_representation()
foo.bar = foo.bar._id
try:
    json.dump(serialized, sys.stdout)
except:
    assert False
deserialized = Foo.from_dict(serialized)
assert deserialized == foo
```

Here's an example of how to use the serialization and deserialization with `DbClassLiteral`:

```python
@define
class Bar(DbClassLiteral):
    dictionary: dict
    date: datetime
    decimal: Decimal

@define
class Foo(DbClass):
    dictionary: dict
    date: datetime
    decimal: Decimal
    bar: Bar

foo = Foo({}, datetime.now(), Decimal(1), Bar({}, datetime.now(), Decimal(1)))
serialized = foo.get_db_representation()
try:
    json.dump(serialized, sys.stdout)
except:
    assert False
deserialized = Foo.from_dict(serialized)
assert deserialized == foo
```

You can make use of db_types the following way

```python
@define
class Foo(DbClass):
    a: int = int8()
    b: int = uint16()
    c: str = varchar(7)
    d: str = text()


class TestFooClass(unittest.TestCase):
    def setUp(self):
        self.foo_instance = Foo(0, 0, '', '')

    def test_attribute_a(self):
        with self.assertRaises(ValueError):
            self.foo_instance.a = -129  # Below int8 range
        with self.assertRaises(ValueError):
            self.foo_instance.a = 128  # Above int8 range

    def test_attribute_b_out_of_range(self):
        with self.assertRaises(ValueError):
            self.foo_instance.b = -1  # Below uint16 range
        with self.assertRaises(ValueError):
            self.foo_instance.b = 65536  # Above uint16 range

    def test_attribute_c_out_of_range(self):
        with self.assertRaises(ValueError):
            self.foo_instance.c = "Too bigg"

    def test_attribute_d_positive(self):
        passed_text = """I'm the Scatman
Ski-bi dibby dib yo da dub dub
Yo da dub dub
Ski-bi dibby dib yo da dub dub
Yo da dub dub
(I'm the Scatman)
Ski-bi dibby dib yo da dub dub
Yo da dub dub
Ski-bi dibby dib yo da dub dub
Yo da dub dub
Ba-da-ba-da-ba-be bop bop bodda bope
Bop ba bodda bope
Be bop ba bodda bope
Bop ba bodda
Ba-da-ba-da-ba-be bop ba bodda bope
Bop ba bodda bope
Be bop ba bodda bope
Bop ba bodda bope"""
        self.foo_instance.d = passed_text
        self.assertEqual(self.foo_instance.d, passed_text)
```
