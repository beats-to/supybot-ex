#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2

def ex(a, ic, oc):
    """<amount> <from> <to>

    Converts currencies using http://www.google.com/finance/converter.
    """

    # public page:  http://www.google.com/finance/converter, e.g. :
    # 'http://www.google.com/finance/converter?a=310.93&from=USD&to=EUR'
    url = 'http://www.google.com/finance/converter?'

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

    # grab the data and tidy up
    try:
        response = opener.open(url, None, timeout)
    except urllib2.HTTPError, s:
        page = 'HTTP Error - (' +str(s) +')'
    except urllib2.URLError, s:
        page = 'URL Error - (' +str(s) +')'
    else:
        page = response.read()
        response.close()
        opener.close()

        # Trim
        page = page[page.find(r'<div id=currency_converter_result>'):]
        page = page[:page.find(r'<input')-1]

        # if the tag is present but contains no data, its length will be 34
        if len(page) == 34:
            page =  'Invalid Currency.'
        # in the event of a conversion failure, '\nCould not convert.' appears
        elif page.find(r'Could not convert.') != -1:
            page =  'Could not convert.'
        else:
            # remove tags and use the data
            page = page.replace(r'<div id=currency_converter_result>', '', 1)
            page = page.replace(r'<span class=bld>', '', 1)
            page = page.replace(r'</span>', '', 1)

    print page
    del page, url, timeout


if len(sys.argv) == 4:
    ex(sys.argv[1], sys.argv[2], sys.argv[3])
elif len(sys.argv) == 2 and sys.argv[1] == 'info':
    print 'Disclaimer: https://www.google.com/help/currency_disclaimer.html'
else:
    print 'usage: ex [AMOUNT] [FROM] [TO]'
    print '       ex [info]'

exit(0)
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
