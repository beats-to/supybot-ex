###
# Copyright (c) 2014, as4
###
from supybot.commands import wrap, optional
import supybot.callbacks as callbacks
import urllib2


class Ex(callbacks.Plugin):
    """
    Load the plugin, issue ex command to use google currency converter
    """
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Ex, self)
        self.__parent.__init__(irc)

    def ex(self, irc, msg, args, a, ic, oc):
        """<amount> <from> <to>

        Converts currencies using http://www.google.com/finance/converter.
        Type \'ex info\' for the disclaimer url.
        """

        # public page:  http://www.google.com/finance/converter, e.g. :
        # 'http://www.google.com/finance/converter?a=310.93&from=USD&to=EUR'
        url = 'http://www.google.com/finance/converter?'

        # show disclaimer URL if called
        if a == 'info' and ic is None and oc is None:
            irc.reply('Disclaimer: https://www.google.com/help/'
                      + 'currency_disclaimer.html')
            return

        # reply command syntax if missing arguments
        if a and ic is None or oc is None:
            raise callbacks.ArgumentError
            return

        # process items (happy path)
        if a:
            url += 'a=' + a
        if ic:
            ic = ic.upper()
            url += '&from=' + ic
        if oc:
            oc = oc.upper()
            url += '&to=' + oc

        timeout = 10

        # build opener for html data
        opener = urllib2.build_opener()
        # add user-agent
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(url, None, timeout)

        # grab the data and tidy up
        try:
            response = opener.open(url, None, timeout)
        except urllib2.HTTPError, s:
            irc.reply('HTTP Error - (' + str(s) + ')')
            return
        except urllib2.URLError, s:
            irc.reply('Url Error - (' + str(s) + ')')
            return
        page = response.read()
        response.close()
        opener.close()

        # Trim
        page = page[page.find(r'<div id=currency_converter_result>'):]
        page = page[:page.find(r'<input')-1]

        # if the tag is present but contains no data, its length will be 34
        if len(page) == 34:
            page = 'Invalid Currency.'
        # in the event of a conversion failure, '\nCould not convert.' appears
        elif page.find(r'Could not convert.') != -1:
            page = 'Could not convert.'
        else:
            # remove tags and use the data
            page = page.replace(r'<div id=currency_converter_result>', '', 1)
            page = page.replace(r'<span class=bld>', '', 1)
            page = page.replace(r'</span>', '', 1)

        irc.reply(page)
        del page, url, timeout

    ex = wrap(ex, ['somethingWithoutSpaces',
              optional('somethingWithoutSpaces'),
              optional('somethingWithoutSpaces')])

Class = Ex

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
