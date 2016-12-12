def verifyCaptcha(context):
    """
    da mettere in un campo plomino dedicato con il relativo template
    """
    # Verify the user input against the captcha.
    # Get captcha type (static or dynamic)
    try:
        from quintagroup.captcha.core.utils import decrypt, parseKey, encrypt1, getWord
    except ImportError:
        return "manca il prodotto quintagroup.captcha.core"

    portal_url = getToolByName(context, "portal_url")
    portal = portal_url.getPortalObject()
    captcha_type = portal.getCaptchaType()

    request = context.REQUEST

    test_key = request.get('key', '')
    hashkey = request.get('hashkey', '')
    decrypted_key = decrypt(portal.captcha_key, hashkey)
    parsed_key = parseKey(decrypted_key)

    index = parsed_key['key']
    date = parsed_key['date']

    if captcha_type == 'static':
        img = getattr(portal, '%s.jpg' % index)
        solution = img.title
        enc = encrypt1(test_key)
    else:
        enc = test_key
        solution = getWord(int(index))

    captcha_tool = getToolByName(portal, 'portal_captchas')
    if (enc != solution) or (decrypted_key in captcha_tool.keys()) or \
       (DateTime().timeTime() - float(date) > 3600):
        return 'Il testo immesso non corrisponde. Riprova'
    else:
        return ''
        #da vedere come fare .. se chiama diverse volte il validate input 
        #captcha_tool.addExpiredKey(decrypted_key)