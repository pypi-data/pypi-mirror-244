# Type Unions

`typeunions` is a library providing [algebraic data types](https://en.wikipedia.org/wiki/Algebraic_data_type) in Python, with a clean and intuitive syntax that use all the strength of `match` and `dataclass` in python 3.10

## Install

```console
pip install typeunions
```

## Usage

```python
@typeunion
class Message
    Quit: ()
    Move: { 'x': int, 'y': int }
    Write: (str)
    ChangeColor: (int, int, int)
```

Each types (`Quit`, `Move`, `Write`, `ChangeColor`) is a python `dataclass`. Hence you can use the `match` `case` pattern:

```python
message = Message.ChangeColor(255, 128, 0)

match message:
    case Quit: print("quit")
    case Move(x, y): print(f"move {x} {y}")
    case Write(s): print(s)
    case ChangeColor(r, g, b): print(f"{r}{g}{b}")
    case _: print("error")
```


Here is an exemple of the same code with rust enum
```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

```rust
match message {
    Quit => println!("quit")
    Move(x, y) => println!("move {} {}", x, y)
    Write(s) => println!(s)
    ChangeColor(r, g, b) => println!(f"{}{}{}", r, g, b)
}
```
