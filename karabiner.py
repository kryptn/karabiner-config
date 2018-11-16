import json

hyper = [
    "right_shift"
    "right_command",
    "right_control",
    "right_option",
]


def add_hyper(from_key_code, to_key_code,
              passthrough_modifiers=None,
              from_modifiers=None,
              to_modifiers=None,
              type_='basic'):
    passthrough_modifiers = passthrough_modifiers or []
    from_modifiers = from_modifiers or []
    to_modifiers = to_modifiers or []

    from_ = {
        "key_code": from_key_code,
        "modifiers": {
            "mandatory": hyper + passthrough_modifiers + from_modifiers
        }
    }

    to = {"key_code": to_key_code}
    if passthrough_modifiers or to_modifiers:
        to["modifiers"] = passthrough_modifiers + to_modifiers

    return {'from': from_, 'to': to, 'type': type_}


ijkl = ('i', 'j', 'k', 'l')
arrow_key_codes = ['up_arrow', 'left_arrow', 'down_arrow', 'right_arrow']
arrow_keys = zip(ijkl, arrow_key_codes)

keys = ('h', 'n', 'u', 'o')
other_things = ('home', 'end', 'page_up', 'page_down')
other_keys = zip(keys, other_things)

CAPS = 'caps_lock'
SHIFT = 'left_shift'
OPTION = 'left_option'
CTRL = 'left_control'
CMD = 'left_command'
BACKSPACE = 'delete_or_backspace'
DELETE = 'delete_forward'
FN = 'fn'
HOME = 'home'
END = 'end'
GRAVE = 'grave_accent_and_tilde'

passthrough_modfiers = [
    [],
    [SHIFT],
    [OPTION],
    [SHIFT, OPTION],
]

delete = add_hyper(BACKSPACE, DELETE, to_modifiers=[FN])
grave = add_hyper(GRAVE, GRAVE)

ijkl_keys_and_modifiers = [(f, t, ms) for f, t in arrow_keys for ms in passthrough_modfiers]
ijkls = [add_hyper(fkey, tkey, passthrough_modifiers=mods) for fkey, tkey, mods in ijkl_keys_and_modifiers]

other_keys_and_modifiers = [(f, t, ms) for f, t in other_keys for ms in passthrough_modfiers]
others = [add_hyper(fkey, tkey, passthrough_modifiers=mods) for fkey, tkey, mods in other_keys_and_modifiers]


def write_to_file():
    with open('boilerplate.json') as fd:
        boilerplate = json.load(fd)

    boilerplate['profiles'][0]['complex_modifications']['rules'][0]['manipulators'] = [delete, grave, *ijkls, *others]

    with open('output_karabiner.json', 'w') as fd:
        json.dump(boilerplate, fd, indent=2)


if __name__ == '__main__':
    write_to_file()
