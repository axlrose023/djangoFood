def detectUser(user):
    if user.role == 1:
        redirecturl = 'vendorDashboard'
        return redirecturl

    elif user.role == 2:
        redirecturl = 'custDashboard'
        return redirecturl
    elif user.role == None and user.is_superadmin:
        redirecturl = '/admin'
        return redirecturl
