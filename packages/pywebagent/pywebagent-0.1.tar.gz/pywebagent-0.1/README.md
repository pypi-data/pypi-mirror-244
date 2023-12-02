# pywebagent - an experimental AI web agent
![pywebagent](logo.png "Logo")

[![Discord Follow](https://dcbadge.vercel.app/api/server/5eJkjMMa?style=for-the-badge)](https://discord.gg/5eJkjMMa)

[![GitHub Repo stars](https://img.shields.io/github/stars/pywebagent/pywebagent?style=social)](https://github.com/assafelovic/gpt-researcher)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/kogan_maxim)](https://twitter.com/kogan_maxim)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/OriKabeli)](https://twitter.com/OriKabeli)


## Description

`pywebagent` is an <b>experimental</b> Python package designed to control websites by utilizing the capabilities of OpenAI's GPT-4 Vision.  
It basically converts website capabilities to python functions!
With `pywebagent`, you can automate complex tasks on websites, like filling forms, buying products, and more.  
It is especially useful for performing tasks that require multiple steps, such as buying a product online, booking a flight, etc.

## Highlights

👁️ Web navigation using OpenAI's GPT-4 Vision technology  
📝 Fill in forms  
💳 Buy products  
📁 Upload Files

## Installation

Ensure you have Python version 3.6 or later installed. Then run this command in the terminal:

```bash
pip install pywebagent
```

## Usage

### Example 1: Order a plush bunny on Amazon
```python
from pywebagent import act

# sometimes you'll need to help the agent bypass the captcha, sometimes it will succeed by itself
act(
    "https://amazon.com", 
    "Order a plush bunny", 
    email="<your amazon email>", 
    password="<your amazon password>"
)
```


### Example 2: Order your photo prints from Mixtiles
Here is an example of how to use `pywebagent` to print some images on [mixtiles.com:](https://mixtiles.com/)

```python
act(
    "https://mixtiles.com/",
    "Order these as Mixtiles",
    name="John Doe",
    email="johndoe208909@gmail.com",
    photos=[
        "omnnitool/demo/mixtiles/1.jpg",
        "omnnitool/demo/mixtiles/2.jpg",
        "omnnitool/demo/mixtiles/3.jpg"
    ],
    payment_info={
        "card_number": "4242424242424242",
        "expiry_date": "12/22",
        "cvc": "123"
    },
    address="123 Main St, San Francisco, CA 94105"
)
```

<b>Note: OPENAI_API_KEY should be set as an environment variable.</b>

## Upcoming Features
* Add return values from `act` (e.g, order number of purchase, ...)
* Add support for more types of interaction (including scrolling, swiping, ..)
* Add caching to speed everything up
* Support open source vision models
* Support more complicated actions

## How It Works
The concept is extremely simple. Detect all elements that have an event handler (which means they can be interacted with), highlight them, take a screenshot, and ask GPT 4 Vision what to do. The results are surprisingly good.

## Contributing
Contributions are more than welcome! In fact, we're looking for people who want to develop this further.  
If you have any suggestions, features requests or want to report bugs, kindly open an issue first to discuss what you would like to change. For changes, please open a pull request.

## Community
Feel free to join our discord at https://discord.gg/5eJkjMMa.

## License

`pywebagent` is licensed under the MIT License. See `LICENSE` for more information.

## Disclaimer

`pywebagent` is an experimental project, and is not officially affiliated with OpenAI.

## Contact 

If you have specific questions about using the `pywebagent`, feel free to email us at maximkgn@gmail.com or ori.kabeli@gmail.com

