
def navbuttons(user):
    buttons = {}
    if user.is_active:
        for role_buttons in user.roles:
            for button in role_buttons.navbarbutton:
                if button.navbarcat.name not in buttons:
                    buttons[button.navbarcat.name] = []
                new_tab = '_self'
                if button.new_tab == True:
                    new_tab = '_blank'
                bn = {'name':button.name,'new_tab':new_tab,'href':button.href,}
                buttons[button.navbarcat.name].append(bn)

    return buttons