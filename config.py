###
# Copyright (c) 2014, as4
###

import supybot.conf as conf


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    conf.registerPlugin('Ex', True)


Ex = conf.registerPlugin('Ex')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Ex, 'someConfigVariableName',
#     registry.Boolean(False, """Help for someConfigVariableName."""))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
