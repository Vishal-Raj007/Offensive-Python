
# ChangeMAC for linux - spoof/fake MAC Address

changemac is a script written in Python3

![](https://github.com/Vishal-Raj007/Offensive-Python/blob/master/MAC_Address/changemac.jpg)

## Deployment

To deploy this project run

```bash
  git clone https://github.com/Vishal-Raj007/Offensive-Python.git
```


## Usage/Examples

```Type sudo changemac.py

    Usage: sudo changemac [options]
    options:
    -h, --help                  show this help message and exit
    -i, --interface INTERFACE   Interface to change MAC Address
    -m, --mac NEW_MAC           Set new MAC Address XX:XX:XX:XX:XX:XX
    -r, --random                Set fully random MAC
    -s, --show                  Print the MAC Address and exit
```
### Set custom MAC
`sudo changemac -i eth0 -m xx:xx:xx:xx:xx:xx`

### Set random MAC
`sudo changemac -i eth0 -r`

## Authors

- [@Vishal-Raj007](https://www.github.com/Vishal-Raj007)

## Feedback

If you have any feedback, please reach out to us at vishalraj1522dehri@gmail.com

