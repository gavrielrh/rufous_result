# Rufous Result

Translation of [Rust's Result type](https://doc.rust-lang.org/std/result/enum.Result.html) to Python 3.

## Example Usage

```python
import requests
from models.user import User
from rufous_result.result import Result, Err, Ok

def get_user_from_api(id: int) -> Result<User, UserNotFoundError>:
    res = requests.get(f"https://example.com/api/user/{id}") 
    if res.ok:
        return Ok(User.from_dict(res.json()))
    return Err(UserNotFoundError(res.reason))

user_id = int(input("User to lookup: "))
print(get_user_from_api(user_id).unwrap_or("User not found"))
```

See the [tests](./tests/test_result.py) for more examples.
