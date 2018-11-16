import json

hyper = [
    "right_shift",
    "right_command",
    "right_control",
    "right_option",
]


def manipulator(from_key,
                to_key,
                from_modifiers=None,
                to_modifiers=None,
                from_modifier_kind='mandatory',
                passthrough_modifiers=None,
                manipulator_type='basic',
                ):
    from_modifiers = from_modifiers or []
    to_modifiers = to_modifiers or []
    passthrough_modifiers = passthrough_modifiers or []

    from_ = {
        "key_code": from_key,
        "modifiers": {
            from_modifier_kind: passthrough_modifiers + from_modifiers
        }
    }

    to = {"key_code": to_key}
    if passthrough_modifiers or to_modifiers:
        to["modifiers"] = passthrough_modifiers + to_modifiers

    return {'from': from_, 'to': [to], 'type': manipulator_type}


def add_hyper(*args, **kwargs):
    from_modifiers = kwargs.get('from_modifiers', [])
    kwargs['from_modifiers'] = from_modifiers + hyper

    return manipulator(*args, **kwargs)


pok3r_map = [
    ('i', 'up_arrow'),
    ('j', 'left_arrow'),
    ('k', 'down_arrow'),
    ('l', 'right_arrow'),
    ('h', 'home'),
    ('n', 'end'),
    ('u', 'page_up'),
    ('o', 'page_down'),
    *[(f"{n}", f"f{n}") for n in range(1, 10)],
    ('0', 'f10'),
    ('hyphen', 'f11'),
    ('equal_sign', 'f12'),
]

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
ESC = 'escape'

passthrough_modfiers = [
    [],
    [CTRL],
    [SHIFT],
    [OPTION],
    [CTRL, SHIFT],
    [SHIFT, OPTION],
    [CTRL, OPTION],
    [CTRL, SHIFT, OPTION],
]

hyper_ = manipulator(CAPS, hyper[:1], from_modifiers=['any'], from_modifier_kind='optional', to_modifiers=hyper[1:])


delete = add_hyper(BACKSPACE, DELETE, to_modifiers=[FN])
grave = add_hyper(GRAVE, GRAVE)
esc = manipulator(GRAVE, ESC)

keys_with_modifiers = [(f, t, ms) for f, t in pok3r_map for ms in passthrough_modfiers]
mappings = [add_hyper(fkey, tkey, passthrough_modifiers=mods) for fkey, tkey, mods in keys_with_modifiers]


def write_to_file():
    with open('boilerplate.json') as fd:
        boilerplate = json.load(fd)

    boilerplate['profiles'][0]['complex_modifications']['rules'][0]['manipulators'] = [delete, grave, esc, *mappings]

    with open('output_karabiner.json', 'w') as fd:
        json.dump(boilerplate, fd, indent=2)


if __name__ == '__main__':
    write_to_file()
