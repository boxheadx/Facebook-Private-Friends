# Facebook-Private-Friends
A tool to fetch friends of anyone with private friend list

When someone sets their friend list to private, we can only see our mutual friends with them. This tool allows us to fetch the friend list even tho they've set it to private. This won't always fetch each and every friend but will fetch most of them. To fetch maximum friends, we can use a common name list instead of iterating through each letter.

## Requirements

* Install selenium
  
  ```bash
  pip3 install selenium
  ```

## Usage

* Provide the link to the user's profile as an argument

```bash
python3 friends.py https://www.facebook.com/somerandomuser
```
